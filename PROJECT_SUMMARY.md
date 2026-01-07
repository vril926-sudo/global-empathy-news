# Global Empathy News - MVP開発完了レポート

## プロジェクト概要

**リポジトリ**: https://github.com/vril926-sudo/global-empathy-news

世界のニュースの中から「視点の偏り（論争）」が激しいトピックを自動抽出し、比較表示するWebサイトの土台となるMVPを開発しました。

## 実装内容

### 1. ニュース収集機能 (`news_analyzer.py`)

以下の3つのニュースソースからRSSフィードを使用してニュースを収集します：

| ソース | 地域 | RSS URL |
|--------|------|---------|
| CNN | 西洋（米国） | http://rss.cnn.com/rss/edition_world.rss |
| Al Jazeera | 中東（カタール） | https://www.aljazeera.com/xml/rss/all.xml |
| Global Times | 東アジア（中国） | https://www.globaltimes.cn/rss/outbrain.xml |

### 2. Gemini API連携

Google Gemini API（gemini-1.5-flash）を使用して、収集したニュースを分析し：

- **トピック抽出**: 複数のソースで報道されている共通トピックを特定
- **Gap Score計算**: 各トピックの「視点の乖離度」を0-100で数値化
  - 0-20: 最小限の視点差
  - 21-40: 低い差
  - 41-60: 中程度の差
  - 61-80: 高い差
  - 81-100: 極端な差

### 3. 出力形式

スクリプトは `output/` ディレクトリに以下のファイルを生成：

- `analysis_YYYYMMDD_HHMMSS.json` - 分析結果（JSON形式）
- `news_data_YYYYMMDD_HHMMSS.json` - 収集したニュースデータ
- `report_YYYYMMDD_HHMMSS.txt` - 人間が読みやすいレポート
- `latest_analysis.json` - 最新の分析結果
- `latest_report.txt` - 最新のレポート

### 4. GitHub Actions自動実行

`.github/workflows/main.yml` により、以下のタイミングで自動実行：

- **6時間ごと**: cron式 `0 */6 * * *`
- **手動実行**: workflow_dispatch
- **コード変更時**: main/masterブランチへのpush

## ファイル構成

```
global-empathy-news/
├── .github/
│   └── workflows/
│       └── main.yml          # GitHub Actions ワークフロー
├── .gitignore                # Git除外設定
├── README.md                 # プロジェクト説明
├── news_analyzer.py          # メインスクリプト
└── requirements.txt          # Python依存関係
```

## 使用ライブラリ

- `feedparser>=6.0.0` - RSSフィード解析
- `google-generativeai>=0.3.0` - Gemini API連携

## 次のステップ（GitHub Actions有効化）

GitHub Actionsを正常に動作させるには、以下の設定が必要です：

1. **Gemini API キーの取得**
   - Google AI Studio (https://aistudio.google.com/) でAPIキーを取得

2. **GitHub Secretsの設定**
   - リポジトリの Settings > Secrets and variables > Actions
   - 「New repository secret」をクリック
   - Name: `GEMINI_API_KEY`
   - Value: 取得したAPIキー

3. **手動実行でテスト**
   - Actions タブ > 「Global Empathy News Analysis」
   - 「Run workflow」ボタンをクリック

## 動作確認済み

- ✅ RSSフィード取得（CNN: 29件, Al Jazeera: 25件, Global Times: 50件）
- ✅ Pythonスクリプト構文チェック
- ✅ GitHubリポジトリへのPush
- ✅ GitHub Actionsワークフロー設定
