# 語る会Library (Game-Music-Library)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://app021game-music-library-fcbmaj5eielz8b5ijmr2k4.streamlit.app/)

**🌐 公開URL**: [https://app021game-music-library-fcbmaj5eielz8b5ijmr2k4.streamlit.app/](https://app021game-music-library-fcbmaj5eielz8b5ijmr2k4.streamlit.app/)

Googleスプレッドシートをデータベースとした、ゲーム音楽の検索・閲覧Webアプリケーション。

過去に紹介された楽曲を、キーワード検索やフィルター機能（ジャンル、プラットフォーム、発表者、配信テーマ）を使って簡単に探すことができます。

> **注意**: Streamlit Cloudの無料プランでは、7日間アクセスがないとアプリがスリープします。
> 
> ✅ **自動Wake Up設定済み**: [UptimeRobot](https://uptimerobot.com/)で12時間ごとに自動モニタリングを実行しています。これにより、24時間365日いつでもアクセス可能な状態を維持しています。
> - **監視サービス**: UptimeRobot（無料プラン）
> - **監視間隔**: 12時間ごと
> - **稼働率**: 過去30日間で100%稼働
> 
> 💡 同様の設定を行いたい場合は、[自動Wake Up設定手順](docs/Streamlit_Cloud自動Wake_Up設定手順.md)を参照してください。

## 特徴

- 🔍 **あいまい検索**: 曲名、ゲーム名、シリーズ名などを柔軟に検索
- 🎯 **詳細フィルター**: ジャンル、プラットフォーム、発表者、配信テーマで絞り込み
- 📊 **楽曲詳細表示**: AgGridで行を選択すると、詳細情報をカード形式で表示
- 🎲 **ランダム表示**: ルーレット演出付きランダムシャッフル機能
- 📺 **配信テーマ一覧**: 配信回ごとの楽曲一覧とアーカイブ動画の表示
- 🔐 **パスワード保護**: 公開時にもアクセスを制御可能

## 技術スタック

- **Frontend/Backend**: [Streamlit](https://streamlit.io/)
- **Data Source**: Google Sheets API (v4)
- **Search Engine**: [thefuzz](https://github.com/seatgeek/thefuzz) (Fuzzy String Matching)
- **UI Components**: [st-aggrid](https://github.com/Pablocasas/st-aggrid)
- **Design**: Neon Library Mode（ダークテーマ）

## インストール

```bash
# リポジトリをクローン
git clone https://github.com/YOUR_USERNAME/App_021_Game-Music-Library.git
cd App_021_Game-Music-Library

# 依存関係をインストール
pip install -r requirements.txt
```

## セットアップ

### 1. Google Sheets API の設定

1. [Google Cloud Console](https://console.cloud.google.com/)でプロジェクトを作成
2. Google Sheets API を有効化
3. サービスアカウントを作成し、JSONキーをダウンロード
4. 使用するスプレッドシートにサービスアカウントのメールアドレスを「閲覧者」として共有

Google Sheets APIの設定については、Google Cloud Consoleのドキュメントを参照してください。

### 2. 認証情報の設定

`.streamlit/secrets.toml` を作成し、以下の形式で認証情報を設定します：

```toml
[connections.gsheets]
type = "service_account"
project_id = "YOUR_PROJECT_ID"
private_key_id = "YOUR_PRIVATE_KEY_ID"
private_key = """-----BEGIN PRIVATE KEY-----
YOUR_PRIVATE_KEY
-----END PRIVATE KEY-----"""
client_email = "YOUR_SERVICE_ACCOUNT_EMAIL"
client_id = "YOUR_CLIENT_ID"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "YOUR_CLIENT_X509_CERT_URL"

[spreadsheet]
id = "YOUR_SPREADSHEET_ID"
sheet_name = "紹介順"
```

### 3. パスワード保護の設定（オプション）

アプリを公開する際にパスワード保護を有効にできます。

```bash
# パスワードハッシュを生成
python scripts/generate_password_hash.py <あなたのパスワード>
```

生成されたハッシュ値を`.streamlit/secrets.toml`に追加：

```toml
[app]
password_hash = "生成されたハッシュ値"
```

## 使用方法

```bash
streamlit run app.py
```

ブラウザで `http://localhost:8501` にアクセスします。

## ディレクトリ構成

```
.
├── app.py                          # メインエントリーポイント
├── requirements.txt                # 依存関係
├── README.md                       # このファイル
├── src/
│   ├── data_loader.py             # スプレッドシート読み込み & 前処理
│   ├── search_engine.py           # あいまい検索ロジック
│   ├── ui.py                      # UIコンポーネント & CSS
│   └── auth.py                    # パスワード認証機能
├── scripts/
│   └── generate_password_hash.py  # パスワードハッシュ生成スクリプト
└── .streamlit/
    └── secrets.toml               # 認証情報（.gitignoreで除外）
```

## Streamlit Cloudへの公開

このアプリをStreamlit Cloudで公開できます。

### 前提条件

- GitHubリポジトリを公開にする必要があります（Streamlit Cloudの無料プランでは公開リポジトリのみ対応）

### 公開手順

1. コードをGitHubにプッシュ
2. [Streamlit Cloud](https://share.streamlit.io/)にログイン
3. 「New app」をクリックしてリポジトリを選択
4. Secretsに認証情報を設定（Google Sheets API認証情報 + パスワードハッシュ（オプション））
5. 「Deploy!」をクリック

Streamlit Cloudでの公開方法については、[Streamlit Cloudの公式ドキュメント](https://docs.streamlit.io/streamlit-community-cloud)を参照してください。

## 機能

### 楽曲検索タブ

- **キーワード検索**: 曲名、ゲーム名、シリーズ名などをあいまい検索
- **詳細フィルター**: 配信テーマ、ジャンル、プラットフォーム、発表者で絞り込み
- **検索結果表示**: AgGridで表示、行を選択すると詳細情報を表示
- **ランダムシャッフル**: ルーレット演出付きでランダムに楽曲を表示

### 配信テーマ一覧タブ

- **ドロップダウン選択**: 配信回を選択して楽曲一覧を表示
- **アーカイブ動画**: 該当する配信回のアーカイブ動画を自動表示
- **最新回ジャンプ**: ワンクリックで最新の配信回に移動

### 全曲リストタブ

- **全データ表示**: すべての楽曲を一覧表示
- **ソート・フィルター**: AgGridの機能で自由にソート・フィルター

## データ構造

スプレッドシートには以下の列が必要です：

- `通算`: 通算番号
- `DISC`: 配信回番号
- `テーマ`: 配信テーマ名
- `曲名`: 楽曲名
- `ゲーム名`: ゲーム名
- `ジャンル`: ジャンル（例: `01_RPG`）
- `プラットフォーム`: プラットフォーム（カンマ区切り可）
- `発表者`: 発表者名

詳細はコード内の `src/data_loader.py` を参照してください。

## ライセンス

このプロジェクトのライセンスは明記されていません。

## 作者

作成者情報は明記されていません。

## 謝辞

このアプリは、ゲーム音楽を紹介する配信番組「語る会」の楽曲を管理・検索するために作成されました。
