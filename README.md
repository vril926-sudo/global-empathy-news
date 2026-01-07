# Global Empathy News

世界のニュースの中から「視点の偏り（論争）」が激しいトピックを自動抽出し、比較表示するWebサイトの土台となるMVPプロジェクトです。

## 概要

このプロジェクトは、異なる地域・視点を持つ複数のニュースソースから記事を収集し、Gemini AIを使用してトピックごとの「視点の乖離度（Gap Score）」を分析します。

### 対象ニュースソース

| ソース | 地域 | 傾向 |
|--------|------|------|
| CNN | 西洋（米国） | 中道左派 |
| Al Jazeera | 中東（カタール） | 中道 |
| Global Times | 東アジア（中国） | 国家寄り |

### Gap Score（乖離度スコア）

- **0-20**: 最小限の視点差（事実報道、類似のフレーミング）
- **21-40**: 低い差（強調点の軽微な違い）
- **41-60**: 中程度の差（フレーミングや焦点の顕著な違い）
- **61-80**: 高い差（重大な視点の違い、潜在的なバイアス）
- **81-100**: 極端な差（完全に対立するナラティブや解釈）

## セットアップ

### 必要条件

- Python 3.9以上
- Gemini API キー

### インストール

```bash
# リポジトリをクローン
git clone https://github.com/YOUR_USERNAME/global-empathy-news.git
cd global-empathy-news

# 依存関係をインストール
pip install -r requirements.txt

# 環境変数を設定
export GEMINI_API_KEY="your-api-key-here"
```

### 実行

```bash
python news_analyzer.py
```

## 出力

スクリプトは `output/` ディレクトリに以下のファイルを生成します：

- `analysis_YYYYMMDD_HHMMSS.json` - 分析結果（JSON形式）
- `news_data_YYYYMMDD_HHMMSS.json` - 収集したニュースデータ
- `report_YYYYMMDD_HHMMSS.txt` - 人間が読みやすいレポート
- `latest_analysis.json` - 最新の分析結果
- `latest_report.txt` - 最新のレポート

## GitHub Actions

このリポジトリは6時間ごとに自動実行されるよう設定されています。

### 必要なシークレット

GitHub リポジトリの Settings > Secrets and variables > Actions で以下を設定してください：

- `GEMINI_API_KEY`: Google Gemini API キー

## プロジェクト構造

```
global-empathy-news/
├── .github/
│   └── workflows/
│       └── main.yml          # GitHub Actions ワークフロー
├── output/                    # 分析結果の出力先
├── news_analyzer.py          # メインスクリプト
├── requirements.txt          # Python依存関係
└── README.md                 # このファイル
```

## ライセンス

MIT License

## 今後の開発予定

- [ ] Webフロントエンドの実装
- [ ] より多くのニュースソースの追加
- [ ] 時系列での視点変化の追跡
- [ ] トピックごとの詳細分析ページ
