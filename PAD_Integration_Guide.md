# PAD Integration Guide - Monodas AutoListing

This guide outlines how to configure Microsoft Power Automate Desktop (PAD) to work with the Python AutoList system for Phase 1.

## 1. Overview
The Python script `main.py` processes Google Sheets data, validates it, checks for VeRO keywords, prevents duplicates, and saves valid tasks to:
`logs/monodas_task_batch.json`

Your PAD flow should be scheduled to run *after* the Python script finishes, or manually triggered by the staff.

## 2. PAD Flow Steps

### Step 1: Read JSON File
- Use the **Convert JSON to custom object** action.
- Read the file located at: `<Workspace_Path>\logs\monodas_task_batch.json`
- Iterate over each task in the parsed JSON array.

### Step 2: Open Browser & Login to Monodas
- Launch a new Edge/Chrome instance and navigate to `https://monodaz.com` (or the URL from `config/api_keys.json`).
- If not logged in, use the CSS selectors found in `config/selectors_config.json` to enter credentials and click login.
  - **Email Selector:** `#email`
  - **Password Selector:** `#password`
  - **Login Button:** `#btn-login`

### Step 3: Loop Through Listings
For each item in the parsed JSON:

#### A. Navigate to "New Listing"
- Click the **New Listing** button (Selector: `#new-listing`) or navigate directly to the registration page: `https://monodaz.com/register` (or `https://monodaz.com/listing/new`).

#### B. Initialize Listing via eBay Reference ID (Stage 1 Form)
Before accessing the listing editor, Monodas requires a reference eBay Item ID to clone the category and item specifics, and the supplier URL to pull image data.
1. **Reference eBay Item ID:** Populate the **eBayアイテムID** field (Selector: `input[name='ebay_item_id']` or `#ebay-item-id`) with the category-specific reference ID from the task JSON: `%CurrentItem.ebay_ref_id%`. This ensures Monodas clones the correct category (e.g. Figures, Models, or Games).
3. **Supplier Select:** Select the supplier dropdown (Selector: `select[name='supplier']` or `#supplier-select`) and match the value from `%CurrentItem.supplier_type%` (e.g. メルカリ, ヤフーフリマ, ラクマ).
3. **Supplier URL:** Populate the URL field (Selector: `#source-url`) with the supplier URL from the JSON object: `%CurrentItem.source_url%`.
4. **Search/Import:** Click the blue **検索** (Search) button (Selector: `button[type='submit']` or `.btn-search`).
5. **Wait for Loading Spinner:** After clicking search, Monodas displays a loading spinner overlay (`取得中...`). Use the **Wait for web page content** action. Configure it to wait for the `loading_spinner` element (from `selectors_config.json`) to **disappear**.
6. **Check for Timeout Error:** Network or fetching issues can cause Monodas to show an error (`Timeout Error!! 取得できませんでした...`). Add an **If web page contains** action to check for the `timeout_error_msg` selector.
   - **If Error Exists:** Log this item as a failure or set it for retry, then use a **Next loop** action to skip to the next listing.
   - **If No Error:** Wait for the main Listing Editor page to fully load, then proceed.

#### C. Fill in Form Fields (Stage 2 Editor)
Once the Listing Editor page has loaded, use the **Populate text field on web page** actions to fill/overwrite the following values:
- **Title:** Clear the existing cloned title and write `%CurrentItem.title%` (Selector: `#item-title`).
- **Price:** Clear the existing price and write `%CurrentItem.price_usd%` (Selector: `#item-price`).
- **Quantity:** Clear the existing quantity and write `%CurrentItem.quantity%` (Selector: `input[name='quantity']`).
- **Description:** Select the description text box or description iframe (`#description-iframe`) and overwrite it with `%CurrentItem.description%`.
- **Shipping Policy:** Select the shipping policy dropdown (`#shipping-policy-select`) and match the value from `%CurrentItem.shipping_policy%`.
- **Handling Time:** Select the handling time dropdown (`#handling-time-select`) and match the value from `%CurrentItem.handling_time%`.

#### D. Save as Draft or Publish (Conditional Routing)
Now that Phase 2's staff/status logic is active, each item in the JSON will have an `%CurrentItem.automation_action%` variable set to either `"draft"` or `"publish"`.

1. **Add an If condition:**
   * **First operand:** `%CurrentItem.automation_action%`
   * **Operator:** `Equal to (=)`
   * **Second operand:** `draft`
2. **Inside the If block (Draft Path):**
   * Click the **Save Draft** button (`#btn-save-draft` or `button.save-draft`).
   * Wait for the page to load and confirm the success message.
3. **Inside the Else / Else If block (Publish Path):**
   * Click the **Publish / 出品** button (`#btn-publish`, `#btn-list`, or `button.publish` depending on the Monodas interface).
   * Wait for the page to load and confirm the success message.
4. **Capture the generated eBay Item ID:**
   * After saving/publishing, capture the generated **eBay Item ID** (`#confirmed-item-id` or `.ebay-item-id` or extract it from the post-publish URL) from the page to write it back to the Google Sheet (updates column `G: eBay_Item_ID`).

### Step 4: Output Listing Results (E2E Sheet Synchronization)
To make the system fully automated, PAD writes the generated eBay Item IDs to a results file. When you run `main.py` next, it will read this file and automatically update the Google Sheet.

#### A. Initialize the Results List (Before the Loop)
*Add this action at the very beginning of your flow, before the "For each" loop:*
1. **Action:** **Create new list**
   * **Variables produced:** `%ResultsList%`

#### B. Extract and Save the eBay Item ID (Inside the Loop, After clicking "List")
*Add these actions right after the "Wait for web page content" (waiting for the eBay ID page to appear after submission):*
1. **Action:** **Get details of element on web page**
   * **Web browser instance:** `%EditorBrowser%`
   * **UI Element:** Select the blue **商品ページを開く** (Open product page) link on the success page.
   * **Property name:** `HRef`
   * **Variables produced:** `%eBayListingURL%`
2. **Action:** **Parse text** (Regex search)
   * **Text to parse:** `%eBayListingURL%`
   * **Text to find:** `\d+` *(this searches for the 12-digit number in the URL)*
   * **Is regular expression:** `True`
   * **Variables produced:** `%eBayItemID%`
3. **Action:** **Set variable**
   * **Variable:** `%ResultText%`
   * **Value:** `{"sheet_row": %CurrentItem.sheet_row%, "ebay_item_id": "%eBayItemID%"}`
4. **Action:** **Add item to list**
   * **Item to add:** `%ResultText%`
   * **Into list:** `%ResultsList%`

#### C. Write the Results File (After the Loop)
*Add these actions at the very end of the flow, after the `End` of the "For each" loop:*
1. **Action:** **Join text**
   * **Specified list:** `%ResultsList%`
   * **Delimiter:** `Custom` (specify a comma `,`)
   * **Variables produced:** `%JoinedResults%`
2. **Action:** **Set variable**
   * **Variable:** `%FinalJSON%`
   * **Value:** `[%JoinedResults%]`
3. **Action:** **Write text to file**
   * **File path:** `<Workspace_Path>\logs\monodas_results.json`
   * **Text to write:** `%FinalJSON%`
   * **If file exists:** `Overwrite`

---

## 3. Error Handling
- If any UI element fails to load within 30 seconds, PAD should capture a screenshot, log the error, and continue to the next item in the JSON array. Use the fallback selectors defined in `selectors_config.json` if the primary selectors fail.

## 4. Maintenance
If Monodas updates its UI, simply update the CSS selectors in `config/selectors_config.json`. The PAD flow should be designed to read these selectors dynamically if possible, or manually updated in the PAD designer.
