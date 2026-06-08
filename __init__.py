"""
AutoList - eBay Listing Automation System

AutoList_PAD パッケージ

このパッケージは、Monodas + ChatGPT + Power Automate Desktop (PAD) + Google Spreadsheet
を統合したeBay出品自動化システムです。

メインモジュール:
  - gsheets: Google Sheets 読み書き
  - chatgpt: ChatGPT API (タイトル・説明文生成)
  - vero_checker: VeRO/特許キーワードチェック
  - duplicate_checker: 重複出品防止
  - shipping: 配送ポリシー自動選択
  - error_handler: エラーログ管理
  - validator: データ検証
"""

__version__ = "1.0.0"