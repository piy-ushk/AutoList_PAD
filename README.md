# AutoList — eBay出品自動化システム セットアップ手順

## 必要なもの

- Windows パソコン
- Python 3.9 以上（なければ https://www.python.org/downloads/ からインストール）
- OpenAI APIキー（ChatGPTを使うため。https://platform.openai.com/api-keys で作成）
- Googleアカウント（GmailでOK）

---

## ステップ1: api_keys.json を作る

`config/api_keys.json.template` をコピーして `config/api_keys.json` にリネームしてください。

**コマンドでやる場合:**
```bash
cd AutoList_PAD
copy config\api_keys.json.template config\api_keys.json
```

**エクスプローラでやる場合:**
`config` フォルダを開き、`api_keys.json.template` を右クリック → コピー → 右クリック → 名前を付けて貼り付け → `api_keys.json` にリネーム

次に、`config/api_keys.json` をメモ帳で開き、以下を設定します:

```json
{
  "openai": {
    "api_key": "sk-ここに実際のOpenAI APIキーを入れる",
    "model": "gpt-4o"
  },
  "google": {
    "access_token": "（当面は空欄でOK。ステップ4で使う）"
  }
}
```

---

## ステップ2: Googleスプレッドシートの準備

### 2-a. Google Cloud でサービスアカウントを作る（初回のみ）

1. https://console.cloud.google.com にアクセス
2. 左上のプロジェクト選択 → 「新しいプロジェクト」→ 名前を入れて作成
3. APIとサービス → ライブラリ → 「Google Sheets API」を検索して有効化
4. 認証情報 → 「認証情報を作成」→ 「サービスアカウント」
   - 名前: `autolist`（任意）
   - ロール: 「編集者」
   - 「完了」をクリック
5. 作成したサービスアカウントをクリック → 「キー」タブ → 「鍵を追加」→ 「JSON」
   - 自動的にJSONファイルがダウンロードされるので、`AutoList_PAD/credentials/` フォルダを作って保存
6. ダウンロードしたJSONファイルをメモ帳で開き、以下のように `config/api_keys.json` を編集:

```json
{
  "openai": {
    "api_key": "sk-あなたのOpenAIキー",
    "model": "gpt-4o"
  },
  "google": {
    "service_account_key_file": "credentials/ダウンロードしたファイル名.json",
    "access_token": "（空欄のままでOK）"
  }
}
```

### 2-b. Googleスプレッドシートを自動作成

```bash
python setup_sheets.py
```

成功すると、次のようなメッセージが表示されます:
```
[SETUP] Created spreadsheet: https://docs.google.com/spreadsheets/d/1abc123def456...
[SETUP]   出品管理表: 55 cells written
[SETUP]   重複チェックDB: 10 cells written
...
```

自動的に `config/sheet_config.json` にスプレッドシートIDが書き込まれます。

**エラーになる場合:**
- `[SETUP] ERROR: No Google access token configured.` → 一度ブラウザでGoogle Sheets APIを有効にしたか確認
- その場合は、上記のサービスアカウントJSONファイルを使う方式を試すか、スプレッドシートを手動で作成:
  1. Google Sheetsで新しいスプレッドシートを作成
  2. URLの `https://docs.google.com/spreadsheets/d/XXXXXXXXX/edit` の `XXXXXXXXX` の部分をコピー
  3. `config/sheet_config.json` の `"spreadsheet_id"` に貼り付け
  4. 手動でタブ名と列名を追加（prompt.mdのSection 5参照）

### 2-c. スプレッドシートの権限設定

作成したスプレッドシートを開き、右上の「共有」→ サービスアカウントのメールアドレス（`autolist@XXXX.iam.gserviceaccount.com` のような形式）を追加 → 「編集者」権限を付与

---

## ステップ3: 出品データを入力

Googleスプレッドシートの「出品管理表」タブを開き、1行目に見出しが自動入力されています。
2行目以降に商品データを入力します。

**最低限必要な列:**

| 列 | 項目名 | 入力例 | 説明 |
|---|---|---|---|
| A | 管理ID_SKU | `2026-06-01-1500` | 重複しない管理番号（日付-価格がおすすめ） |
| E | 商品名_JP | `ポケモンカード リザードンVMAX` | 日本語の商品名 |
| J | 仕入URL | `https://jp.mercari.com/item/...` | メルカリなどの仕入元URL（必須） |
| N | Category | `Pokemon Cards` | eBayカテゴリ名 |
| O | Condition | `Used` または `New` | 商品状態 |
| P | 出品価格_USD | `25.00` | 米ドルでの販売価格 |
| AE | 担当者 | `山田太郎` | この商品を担当するスタッフ名 |
| AI | Listing_Status | `pending_ai` | **必ず `pending_ai` と入力してください** |

他の列（Brand, JAN_Code, 画像URLs など）は任意ですが、入力すると検出精度が上がります。

---

## ステップ4: 実行する

```bash
python main.py
```

**実行結果の見方:**

```
[2026-06-01 10:00:00] ============================================================
[2026-06-01 10:00:00] AutoList - eBay Listing Automation System
[2026-06-01 10:00:00] Step 1/5: Connecting to Google Sheets...
[2026-06-01 10:00:00]   Connected.
[2026-06-01 10:00:00] Step 2/5: Loading VeRO keyword dictionary...
[2026-06-01 10:00:00]   Loaded 52 keywords.
[2026-06-01 10:00:00] Step 3/5: Processing AI content generation...
[2026-06-01 10:00:00]   Found 2 rows.
[2026-06-01 10:00:00]   [1/2] Generating for SKU: 2026-06-01-1500
[2026-06-01 10:00:00]     OK: AI content generated.
[2026-06-01 10:00:00] Step 5/5: Preparing Monodas draft tasks...
[2026-06-01 10:00:00]   Saved 2 draft tasks to logs\monodas_task_batch.json.
[2026-06-01 10:00:00] Cycle complete.
```

処理が完了すると:
- ChatGPTで生成されたタイトル・説明文がスプレッドシートのY～AD列に書き込まれる
- `AI_Status` 列が `ai_complete` に変わる
- 検証後、`Validation_Status` が `validated` になる
- Monodasに送信するデータが `logs/monodas_task_batch.json` に保存される（PADで読み込んで下書き保存）

---

## エラーが出た場合

**`OPENAI_API_KEY not configured` が出る:**
→ `config/api_keys.json` の `api_key` に正しいキーが入っているか確認

**`spreadsheet_id` が設定されていない:**
→ `config/sheet_config.json` を開き、`spreadsheet_id` に実際のIDが入っているか確認

**行が処理されない:**
→ スプレッドシートの `AI` 列（Listing_Status）が `pending_ai` になっているか確認
→ `AE` 列（担当者）に名前が入っているか確認

---

## 全体の処理の流れ

```
① スタッフがスプレッドシートに商品データを入力（Listing_Status = pending_ai）
② python main.py を実行
③ → ChatGPT API がタイトル・説明文を自動生成
④ → VeRO禁止キーワードをチェック（該当する場合はそこで停止）
⑤ → 重複出品をチェック（該当する場合はそこで停止）
⑥ → すべて通過したら logs/monodas_task_batch.json に出力
⑦ Power Automate Desktop がこのJSONを読み込み、Monodasで下書き保存
⑧ 管理者がeBay Seller Hubで内容を確認、承認
⑨ 公開後、Monodasが自動で在庫監視・価格監視・自動終了
```