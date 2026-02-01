# PROJECT CONTEXT & MEMORY

> **Note**: このプロジェクトは App_005 (YouTube Comment Scraper) と連携して動作します。App_005 がスプレッドシートにデータを書き込み、App_021 がそのデータを読み取って表示します。

---

## 1. プロジェクト概要 (Overview)

* **アプリ名**: App_021 Game-Music-Library (語る会Library)
* **目的**: YouTubeライブ配信「ゲーム音楽を語る会」で紹介された楽曲を、検索・閲覧できるWebアプリケーション。
* **ターゲットユーザー**: 配信視聴者および配信者本人。
* **公開URL**: https://app021game-music-library-fcbmaj5eielz8b5ijmr2k4.streamlit.app/

---

## 2. 現在の開発状況 (Current Status)

### 現在のフェーズ
**運用中** - Streamlit Cloudで公開中。UptimeRobotによる自動監視で24時間365日稼働。

### 実装済み (Done)
- **楽曲検索**: あいまい検索（thefuzz使用）、詳細フィルター（テーマ、ジャンル、発表者）
- **配信テーマ一覧**: ドロップダウン選択でエピソードごとの楽曲リスト表示
- **全曲リスト**: AgGridによる高速表示とソート・フィルター機能
- **統計ダッシュボード**: グラフ付き統計情報（ジャンル分布、発表者ランキングなど）
- **ランダムシャッフル**: ルーレット演出付きランダム表示機能
- **パスワード保護**: Streamlit Secrets経由でアクセス制御
- **自動Wake Up**: UptimeRobotで12時間ごとに監視し、スリープを防止

### 未実装・課題 (Todo)
- [ ] 曲名のひらがな・カタカナ表記ゆれへの対応強化
- [ ] お気に入り機能（ローカルストレージ使用）
- [ ] シリーズ名による絞り込み機能
- [ ] ゲーム名の自動補完（入力中にサジェスト表示）

---

## 3. App_005 との連動 (Integration with App_005)

### データフロー

```
┌──────────────────────────────────────────────────┐
│ App_005 (YouTube Comment Scraper)                │
│  ├── Phase 5: スプレッドシート自動入力            │
│  │   └── Obsidian台本から曲情報を抽出             │
│  │       └── Google Sheets APIで書き込み          │
│  │                                                 │
│  └── Phase 6: データエンリッチャー                │
│      └── Gemini APIでメタデータを補完              │
│          └── シリーズ名、ジャンル、パブリッシャー │
└──────────────┬───────────────────────────────────┘
               │
               │ Google Sheets (データソース)
               │ - スプレッドシートID: 共有
               │ - シート名: 「紹介順」
               │
               ↓
┌──────────────────────────────────────────────────┐
│ App_021 (Game-Music-Library)                     │
│  ├── データ読み込み: Google Sheets API v4          │
│  │   └── 反映時間: 最大3分                         │
│  │                                                 │
│  ├── 検索エンジン: thefuzz (あいまい検索)          │
│  │                                                 │
│  └── UI表示: Streamlit (公開URL)                  │
│      └── AgGrid, カード表示、グラフ可視化          │
└──────────────────────────────────────────────────┘
```

### 連携のタイミング

1. **配信後**: App_005 の Phase 5 (スプレッドシート自動入力) が実行される
2. **データ書き込み**: 台本から曲情報（曲名、ゲーム名、発表者など）をスプレッドシートに追加
3. **データエンリッチャー (Phase 6)**: 必要に応じて Gemini API でメタデータ（シリーズ名、ジャンル等）を補完
4. **App_021 反映**: スプレッドシートのデータが更新されると、App_021 が自動的に読み取って表示（最大3分で反映）

### GUI通知機能

App_005 の GUI版では、Phase 5・6 完了時に以下の通知が表示されます：

- **通知内容**: 「語る会Libraryへの反映時間（最大3分）」
- **アクション**: ダイアログで App_021 の公開URLを開くか選択可能

---

## 4. 技術スタック (Tech Stack)

- **Frontend/Backend**: Streamlit
- **Data Source**: Google Sheets API (v4)
- **Search Engine**: thefuzz (Fuzzy String Matching)
- **UI Components**: st-aggrid
- **Design**: Neon Library Mode (ダークテーマ)
- **Deployment**: Streamlit Cloud (無料プラン)
- **Monitoring**: UptimeRobot (12時間ごとの自動監視)

---

## 5. 運用メモ (Operation Notes)

- **認証情報**: `.streamlit/secrets.toml` でGoogle Sheets APIのサービスアカウント認証情報を管理（Streamlit Cloud上では Secrets 設定画面から入力）。
- **スプレッドシートID**: App_005 と同じスプレッドシートIDを使用。
- **シート名**: 「紹介順」（App_005 の Phase 5 で書き込まれるシート名と一致）。
- **データ更新**: App_005 からの書き込み完了後、最大3分で App_021 に反映される（Streamlit のキャッシュ更新タイミングによる）。
- **自動Wake Up**: UptimeRobotで12時間ごとに監視し、Streamlit Cloudの7日間自動スリープを防止。

---

## 6. 作業メモ (Work Log)

### 2026-02-01: App_005連携の明確化

#### 実施内容
- `CONTEXT.md` を新規作成し、App_005 との連動フローをドキュメント化。
- データフローの図解を追加し、Phase 5・6 → App_021 の流れを明確化。

#### 今後の予定
- お気に入り機能の実装（ローカルストレージ使用）。
- シリーズ名による絞り込み機能の追加。
