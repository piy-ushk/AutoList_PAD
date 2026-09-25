function ExecuteScript() {
    let targetDoc = null;
    let titleInput = null;
    
    // 1. 再帰的にDOMとiframe内を検索
    function searchContext(d) {
        if (!d) return;
        let el = d.querySelector("#title, textarea[id='title'], #item-title, input[name='title'], textarea[name='title'], .title-input");
        if (el) {
            titleInput = el;
            targetDoc = d;
            return;
        }
        let iframes = d.querySelectorAll("iframe");
        for (let i = 0; i < iframes.length; i++) {
            try {
                let iframeDoc = iframes[i].contentDocument || iframes[i].contentWindow.document;
                searchContext(iframeDoc);
                if (targetDoc) return; // 見つかったら終了
            } catch(e) {
                // クロスドメインエラー等は無視
            }
        }
    }
    
    searchContext(document);

    if (!titleInput || !targetDoc) {
        let textareas = document.querySelectorAll("textarea").length;
        let iframes = document.querySelectorAll("iframe").length;
        return "WAITING | URL: " + location.href + " | Textareas: " + textareas + " | Iframes: " + iframes;
    }

    // 2. 出現したらTitleを上書き
    titleInput.value = "%CurrentItem.title%";
    titleInput.dispatchEvent(new Event('input', { bubbles: true }));
    titleInput.dispatchEvent(new Event('change', { bubbles: true }));

    // 3. Priceを上書き
    let priceInput = targetDoc.querySelector("#price, input[id='price'], input[name='price'], input[name='BuyItNowPrice'], #binPrice");
    if (priceInput) {
        priceInput.value = "%CurrentItem.price_usd%";
        priceInput.dispatchEvent(new Event('input', { bubbles: true }));
        priceInput.dispatchEvent(new Event('change', { bubbles: true }));
    }

    // 4. Quantityを上書き
    let qtyInput = targetDoc.querySelector("#quantity, input[id='quantity'], input[name='quantity'], input[name='Quantity']");
    if (qtyInput) {
        qtyInput.value = "%CurrentItem.quantity%";
        qtyInput.dispatchEvent(new Event('input', { bubbles: true }));
        qtyInput.dispatchEvent(new Event('change', { bubbles: true }));
    }

    // 5. Item Specificsを汎用的に上書き
    let specificsStr = "%CurrentItem.item_specifics%";
    if (specificsStr && specificsStr !== "Does not apply") {
        let pairs = specificsStr.split("|");
        let dict = {};
        pairs.forEach(p => {
            let parts = p.split(":");
            if (parts.length >= 2) {
                let keyText = parts[0].trim().toLowerCase();
                let val = parts.slice(1).join(":").trim();
                dict[keyText] = val;
            }
        });

        let labels = targetDoc.querySelectorAll("label, th");
        labels.forEach(label => {
            let labelText = label.innerText.trim().replace('*', '').toLowerCase();
            if (dict[labelText]) {
                let parent = label.parentElement;
                let input = label.nextElementSibling || parent.querySelector("input, select") || (parent.nextElementSibling ? parent.nextElementSibling.querySelector("input, select") : null);
                if (input && (input.tagName === "INPUT" || input.tagName === "SELECT")) {
                    input.value = dict[labelText];
                    input.dispatchEvent(new Event('input', { bubbles: true }));
                    input.dispatchEvent(new Event('change', { bubbles: true }));
                }
            }
        });
    }

    // 6. 安全確認（検証）：正しく上書きされたかチェック
    if (titleInput.value !== "%CurrentItem.title%") {
        return "ERROR: タイトルの上書きに失敗しました";
    }

    // すべて成功
    return "SUCCESS";
}
