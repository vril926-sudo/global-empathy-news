# Global Empathy News

世界のニュースの中から「視点の偏り（論争）」が激しいトピックを自動抽出し、比較表示するWebサイト。

## 概要

Global Empathy Newsは、CNN（西洋/米国）、Al Jazeera（中東）、Global Times（中国）の3つの国際ニュースソースからニュースを収集し、Gemini AIを使用して「視点の乖離度（Gap Score）」を分析します。

## 機能

- **自動ニュース収集**: RSSフィードを使用して3つのソースからニュースを収集
- **AI分析**: Gemini APIを使用してトピックを抽出し、視点の違いを分析
- **Gap Score**: 0-100のスコアで視点の乖離度を数値化
- **定期実行**: GitHub Actionsで6時間ごとに自動更新
- **Webサイト**: Next.js（App Router）を使用した静的サイト

## Gap Scoreの基準

| スコア | レベル | 説明 |
|--------|--------|------|
| 0-20 | Minimal | 最小限の視点差（事実報道、類似のフレーミング） |
| 21-40 | Low | 低い差（強調点の軽微な違い） |
| 41-60 | Moderate | 中程度の差（フレーミングや焦点の顕著な違い） |
| 61-80 | High | 高い差（重大な視点の違い、潜在的なバイアス） |
| 81-100 | Extreme | 極端な差（完全に対立する物語や解釈） |

## プロジェクト構造

```
global-empathy-news/
├── .github/
│   └── workflows/
│       └── main.yml          # GitHub Actions ワークフロー
├── data/
│   ├── latest_analysis.json  # 最新の分析結果
│   ├── latest_news.json      # 最新のニュースデータ
│   └── latest_report.txt     # 最新のレポート
├── web/                      # Next.js Webサイト
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx
│   │   │   └── globals.css
│   │   ├── components/
│   │   │   └── TopicCard.tsx
│   │   └── types/
│   │       └── analysis.ts
│   ├── next.config.ts
│   └── package.json
├── .gitignore
├── news_analyzer.py          # メインスクリプト
├── requirements.txt          # Python依存関係
└── README.md
```

## セットアップ

### 1. Pythonスクリプトの実行

```bash
# 依存関係のインストール
pip install -r requirements.txt

# 環境変数の設定
export GEMINI_API_KEY="your-api-key"

# スクリプトの実行
python news_analyzer.py
```

### 2. Webサイトの開発

```bash
cd web

# 依存関係のインストール
pnpm install

# 開発サーバーの起動
pnpm dev

# 静的サイトのビルド
pnpm build
```

### 3. GitHub Actionsの設定

1. リポジトリの Settings > Secrets and variables > Actions
2. 「New repository secret」をクリック
3. Name: `GEMINI_API_KEY`
4. Value: Gemini APIキー

## 技術スタック

### バックエンド
- Python 3.11
- feedparser（RSSフィード解析）
- google-generativeai（Gemini API）

### フロントエンド
- Next.js 16（App Router）
- TypeScript
- Tailwind CSS
- 静的サイト生成（SSG）

### インフラ
- GitHub Actions（6時間ごとの自動実行）

## ライセンス

MIT License
