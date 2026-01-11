import streamlit as st
import pandas as pd
import time
import json
import random
from st_aggrid import AgGrid, GridOptionsBuilder, ColumnsAutoSizeMode, DataReturnMode

def load_custom_css():
    """
    アプリ全体の見た目を整えるカスタムCSSを注入
    """
    st.markdown("""
        <style>
        /* =========================================
           1. 全体レイアウト & 背景
           ========================================= */
        .stApp {
            background: linear-gradient(135deg, #0f0c29 0%, #1a1a2e 50%, #0f0c29 100%);
            color: #f0f0f0;
        }

        .main .block-container {
            background-color: rgba(0, 0, 0, 0.3);
            border-radius: 20px;
            padding: 2rem 3rem;
            margin-top: 1rem;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }

        /* =========================================
           2. タイトル & サブテキスト
           ========================================= */
        .main-title {
            background: linear-gradient(to right, #ffffff, #00dbde);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 3rem !important;
            font-weight: 900 !important;
            text-align: center;
            margin-bottom: 0.2rem;
            filter: drop-shadow(0 2px 4px rgba(0,0,0,0.5));
        }
        .sub-text {
            text-align: center;
            color: rgba(255, 255, 255, 0.7) !important; /* コントラスト比改善 */
            font-size: 1rem !important; /* 本文と同じサイズに */
            margin-bottom: 2rem;
            font-weight: 500;
            opacity: 0.8; /* 重要度を視覚的に下げる */
        }

        /* 見出しの階層化 */
        h2 {
            font-size: 2rem !important; /* 32px */
            font-weight: 700 !important;
            color: #00dbde !important;
            margin-top: 2rem !important;
            margin-bottom: 1rem !important;
        }

        h3 {
            font-size: 1.5rem !important; /* 24px */
            font-weight: 600 !important;
            color: #ffffff !important;
            margin-top: 1.5rem !important;
            margin-bottom: 0.75rem !important;
        }

        /* =========================================
           3. フォーム・入力関連
           ========================================= */
        label {
            color: #ffffff !important;
            font-weight: 600 !important;
        }
        .stTextInput > div > div > input {
            background-color: #ffffff !important;
            color: #1a1a2e !important;
            border: 2px solid rgba(0, 219, 222, 0.5) !important;
            border-radius: 8px !important;
            height: 3rem;
            font-weight: 600 !important;
            transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
        }
        
        /* テキスト入力のフォーカス状態 */
        .stTextInput > div > div > input:focus {
            outline: 3px solid rgba(0, 219, 222, 0.8) !important;
            outline-offset: 2px !important;
            border-color: #00dbde !important;
            box-shadow: 0 0 0 4px rgba(0, 219, 222, 0.2) !important;
        }

        /* =========================================
           4. ボタン & タブ
           ========================================= */
        .stButton > button {
            background-color: rgba(255, 255, 255, 0.08) !important;
            color: #ffffff !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            min-height: 44px !important; /* タッチターゲットの最小サイズ */
            min-width: 44px !important;
            padding: 0.75rem 1.5rem !important;
            /* 最適化されたtransition */
            transition: background-color 0.2s ease, 
                        color 0.2s ease, 
                        box-shadow 0.2s ease,
                        transform 0.1s ease !important;
            will-change: background-color, transform; /* GPUアクセラレーションを促す */
        }
        .stButton > button:hover {
            background-color: #00dbde !important;
            color: #000000 !important;
            box-shadow: 0 0 15px rgba(0, 219, 222, 0.4) !important;
        }
        
        /* ボタンのフォーカス状態 */
        .stButton > button:focus {
            outline: 3px solid rgba(0, 219, 222, 0.8) !important;
            outline-offset: 2px !important;
            box-shadow: 0 0 0 4px rgba(0, 219, 222, 0.3) !important;
        }
        
        /* ボタンのアクティブ状態（クリック時） */
        .stButton > button:active {
            transform: scale(0.98) !important;
            box-shadow: 0 0 8px rgba(0, 219, 222, 0.3) !important;
            transition: transform 0.1s ease, box-shadow 0.1s ease !important;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: rgba(0, 0, 0, 0.2) !important;
            padding: 8px;
            border-radius: 12px;
            margin-bottom: 2rem;
        }
        /* 選択されていないタブの基本スタイル */
        .stTabs [data-baseweb="tab"] {
            color: #ffffff !important;
            background-color: transparent !important;
        }
        /* 選択されているタブ */
        .stTabs [aria-selected="true"],
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background-color: #00dbde !important;
            color: #000000 !important;
        }
        /* タブのホバー状態（選択されていないタブ） */
        .stTabs [data-baseweb="tab"]:not([aria-selected="true"]):hover {
            background-color: rgba(255, 255, 255, 0.1) !important;
            color: #ffffff !important;
        }
        /* タブ内のテキストのスタイルも確実に適用 */
        .stTabs [data-baseweb="tab"] p,
        .stTabs [data-baseweb="tab"] span {
            color: inherit !important;
        }

        /* =========================================
           5. 特殊コンポーネント (Expander, Cards, etc.)
           ========================================= */
        .stExpander {
            border: 1px solid rgba(0, 219, 222, 0.3) !important;
            background-color: #1a1a2e !important;
            border-radius: 12px !important;
            margin-bottom: 1.5rem !important;
        }
        
        .random-card {
            background: rgba(255, 255, 255, 0.05);
            padding: 24px;
            border-radius: 16px;
            border-left: 6px solid #fc00ff;
            margin-bottom: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }

        /* セレクトボックスのカスタマイズ（モバイルでの視認性向上） */
        .stSelectbox > div {
            background-color: #ffffff !important;
            color: #1a1a2e !important;
            border-radius: 8px !important;
            border: 2px solid rgba(0, 219, 222, 0.5) !important;
            transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
        }
        
        /* セレクトボックスのホバー状態 */
        .stSelectbox > div:hover {
            border-color: rgba(0, 219, 222, 0.6) !important;
            box-shadow: 0 0 8px rgba(0, 219, 222, 0.2) !important;
        }
        
        /* セレクトボックスのフォーカス状態 */
        .stSelectbox > div:focus-within {
            outline: 3px solid rgba(0, 219, 222, 0.8) !important;
            outline-offset: 2px !important;
            border-color: #00dbde !important;
            box-shadow: 0 0 0 4px rgba(0, 219, 222, 0.2) !important;
        }
        
        .stSelectbox p {
            color: #ffffff !important;
            font-weight: 600 !important;
        }
        
        /* マルチセレクトのスタイル */
        .stMultiSelect > div > div {
            background-color: #ffffff !important;
            color: #1a1a2e !important;
            border-radius: 8px !important;
            border: 2px solid rgba(0, 219, 222, 0.5) !important;
            transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
        }

        .stMultiSelect > div > div:hover,
        .stMultiSelect > div > div:focus-within {
            border-color: #00dbde !important;
            box-shadow: 0 0 0 4px rgba(0, 219, 222, 0.2) !important;
        }

        /* 詳細コンテナの余白調整 */
        .theme-detail-container {
            background-color: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 1.5rem;
            margin: 0;
        }

        /* 楽曲詳細カード */
        .song-detail-card {
            background: rgba(255, 255, 255, 0.05);
            border: 2px solid rgba(0, 219, 222, 0.3);
            border-radius: 16px;
            padding: 24px;
            margin-top: 20px;
            box-shadow: 0 4px 20px rgba(0, 219, 222, 0.2);
        }
        .song-detail-title {
            color: #00dbde;
            font-size: 2rem;
            font-weight: 900;
            margin-bottom: 10px;
        }
        .song-detail-subtitle {
            color: #ffffff;
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 20px;
        }
        .song-detail-info {
            color: #e0e0e0;
            font-size: 1rem;
            margin: 8px 0;
        }
        .song-detail-label {
            color: #00dbde;
            font-weight: 600;
            display: inline-block;
            min-width: 100px;
        }

        /* =========================================
           6. データテーブル (AgGrid)
           ========================================= */
        .ag-theme-streamlit {
            border-radius: 12px !important;
            background-color: #000000 !important;
        }
        .ag-row-odd { background-color: #000000 !important; }
        .ag-row-even { background-color: #404040 !important; }
        .ag-cell { color: #ffffff !important; }
        .ag-header { background-color: #1a1a1a !important; }
        .ag-header-cell-label { color: #00dbde !important; }
        
        /* AgGrid行のホバー状態 */
        .ag-row:hover {
            background-color: rgba(0, 219, 222, 0.1) !important;
            cursor: pointer !important;
            transition: background-color 0.15s ease !important;
        }
        
        /* AgGrid行の選択状態 */
        .ag-row-selected {
            background-color: rgba(0, 219, 222, 0.2) !important;
            border-left: 4px solid #00dbde !important;
        }
        
        /* AgGrid行のフォーカス状態（キーボード操作時） */
        .ag-row:focus {
            outline: 2px solid rgba(0, 219, 222, 0.8) !important;
            outline-offset: -2px !important;
        }

        /* =========================================
           7. ローディング状態の視覚的改善
           ========================================= */
        .stSpinner > div {
            border-color: #00dbde !important;
            border-top-color: transparent !important;
        }

        .stSpinner > div > div {
            background-color: rgba(0, 219, 222, 0.1) !important;
        }

        [data-testid="stSpinner"] {
            color: #00dbde !important;
            font-weight: 600 !important;
        }

        /* =========================================
           8. エラーメッセージ・情報メッセージのスタイル改善
           ========================================= */
        /* アラートメッセージの基本スタイル（Streamlit標準のスタイルを上書き） */
        [data-base="stAlert"],
        .stAlert {
            border-radius: 12px !important;
            border-left: 4px solid rgba(0, 219, 222, 0.5) !important;
            background-color: rgba(0, 219, 222, 0.08) !important;
            border: 1px solid rgba(0, 219, 222, 0.2) !important;
            padding: 1rem !important;
        }

        /* エラーメッセージ（st.error） - Streamlitのデフォルトクラスを使用 */
        [data-base="stAlert"].alert-danger,
        .stAlert[data-testid="stAlert"]:has(> div > div > svg[aria-label="Error"]) {
            border-left: 4px solid #ff4444 !important;
            background-color: rgba(255, 68, 68, 0.1) !important;
            border: 1px solid rgba(255, 68, 68, 0.3) !important;
        }

        /* 成功メッセージ（st.success） */
        [data-base="stAlert"].alert-success,
        .stAlert[data-testid="stAlert"]:has(> div > div > svg[aria-label="Success"]) {
            border-left: 4px solid #00dbde !important;
            background-color: rgba(0, 219, 222, 0.1) !important;
            border: 1px solid rgba(0, 219, 222, 0.3) !important;
        }

        /* 情報メッセージ（st.info） */
        [data-base="stAlert"].alert-info,
        .stAlert[data-testid="stAlert"]:has(> div > div > svg[aria-label="Info"]) {
            border-left: 4px solid #00dbde !important;
            background-color: rgba(0, 219, 222, 0.08) !important;
            border: 1px solid rgba(0, 219, 222, 0.2) !important;
        }

        /* 警告メッセージ（st.warning） */
        [data-base="stAlert"].alert-warning,
        .stAlert[data-testid="stAlert"]:has(> div > div > svg[aria-label="Warning"]) {
            border-left: 4px solid #ffaa00 !important;
            background-color: rgba(255, 170, 0, 0.1) !important;
            border: 1px solid rgba(255, 170, 0, 0.3) !important;
        }

        /* =========================================
           9. スクロールバーのスタイル（快適性向上）
           ========================================= */
        /* カスタムスクロールバー（Webkit系ブラウザ） */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }

        ::-webkit-scrollbar-track {
            background: rgba(0, 0, 0, 0.2);
            border-radius: 5px;
        }

        ::-webkit-scrollbar-thumb {
            background: rgba(0, 219, 222, 0.5);
            border-radius: 5px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: rgba(0, 219, 222, 0.8);
        }

        /* Firefox用 */
        * {
            scrollbar-width: thin;
            scrollbar-color: rgba(0, 219, 222, 0.5) rgba(0, 0, 0, 0.2);
        }

        /* =========================================
           10. 本文テキストとリンクのコントラスト改善
           ========================================= */
        .stMarkdown, p {
            color: #e0e0e0 !important; /* ダーク背景に対して読みやすく */
        }

        /* リンクのコントラスト */
        a {
            color: #00dbde !important;
            text-decoration: underline !important;
        }

        a:hover {
            color: #ffffff !important;
            text-decoration: none !important;
        }

        /* =========================================
           11. テキスト選択時のハイライト
           ========================================= */
        ::selection {
            background-color: rgba(0, 219, 222, 0.3);
            color: #ffffff;
        }

        ::-moz-selection {
            background-color: rgba(0, 219, 222, 0.3);
            color: #ffffff;
        }

        /* =========================================
           12. モバイル対応・レスポンシブデザイン
           ========================================= */
        @media (max-width: 768px) {
            .main-title {
                font-size: 2rem !important; /* 32px - モバイルでは小さく */
            }
            
            .sub-text {
                font-size: 0.9rem !important; /* 14.4px */
            }
            
            .main .block-container {
                padding: 1rem 1.5rem !important; /* パディングを減らす */
            }
            
            .song-detail-title {
                font-size: 1.5rem !important; /* 24px */
            }
            
            .song-detail-subtitle {
                font-size: 1.1rem !important; /* 17.6px */
            }
            
            .stButton > button {
                min-height: 48px !important; /* モバイルではさらに大きく */
                font-size: 1rem !important;
            }
        }

        /* =========================================
           13. ユーティリティ
           ========================================= */
        [data-testid="stSidebar"] { display: none !important; }

        .filter-tag {
            display: inline-flex;
            align-items: center;
            background-color: rgba(255, 255, 255, 0.1);
            color: #ffffff;
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 0.85rem;
            margin-right: 8px;
            margin-bottom: 8px;
            border: 1px solid rgba(0, 219, 222, 0.3);
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        .filter-tag-label {
            color: #00dbde;
            font-weight: 700;
            margin-right: 6px;
        }
        </style>
    """, unsafe_allow_html=True)

def on_theme_change():
    """セレクトボックスでテーマが変更された時の処理"""
    if 'theme_selector' in st.session_state:
        st.session_state['selected_themes'] = [st.session_state['theme_selector']]

def jump_to_latest_theme(latest_theme):
    """最新回へジャンプするためのコールバック"""
    st.session_state['selected_themes'] = [latest_theme]

def render_theme_list_page(df):
    """
    配信テーマ一覧：モバイルフレンドリーなドロップダウン形式
    """
    st.subheader("📺 配信アーカイブ・ブラウザ")
    
    # フィルターオプションからテーマ一覧を取得
    from src.data_loader import get_filter_options
    filter_options = get_filter_options(df)
    themes = filter_options['テーマ']
    
    if not themes:
        st.info("データがありません。")
        return

    # セッション状態の取得
    current_themes = st.session_state.get('selected_themes', [])
    current_selected_theme = current_themes[0] if current_themes else themes[0]

    # --- 上部操作エリア ---
    col1, col2 = st.columns([7, 3])
    with col1:
        st.selectbox(
            "表示する配信回を選択",
            options=themes,
            index=themes.index(current_selected_theme) if current_selected_theme in themes else 0,
            key="theme_selector",
            on_change=on_theme_change
        )
    with col2:
        st.markdown('<div style="margin-top: 28px;"></div>', unsafe_allow_html=True)
        # on_click コールバックを使用してエラーを回避
        st.button(
            "✨ 最新回を表示", 
            use_container_width=True, 
            on_click=jump_to_latest_theme, 
            args=(themes[0],)
        )

    st.markdown("---")

    # --- 詳細表示エリア ---
    # ここで直接 session_state を読み取る
    current_themes = st.session_state.get('selected_themes', [])
    if not current_themes:
        st.info("表示するテーマを選択してください。")
        return

    target_theme = current_themes[0]
    st.markdown(f"### 🎵 {target_theme}")
    
    with st.container():
        st.markdown('<div class="theme-detail-container">', unsafe_allow_html=True)
        
        # アーカイブ動画
        render_archive_video(df, [target_theme])
        
        # 曲一覧
        theme_filters = {
            'テーマ': [target_theme],
            'ジャンル': [],
            'プラットフォーム': [],
            '発表者': []
        }
        theme_df = apply_filters(df, theme_filters)
        st.write(f"📊 紹介曲一覧 ({len(theme_df)}件)")
        
        display_results(theme_df, mode="search", key=f"ag_theme_detail_{target_theme}")
        
        st.markdown('</div>', unsafe_allow_html=True)

def render_archive_video(df, selected_themes):
    """
    選択されたテーマに対応するアーカイブ動画を表示
    """
    if not selected_themes:
        return

    target_theme = selected_themes[0]
    
    match = df[df['表示用テーマ'] == target_theme]
    if not match.empty and 'アーカイブURL' in df.columns:
        url = match.iloc[0]['アーカイブURL']
        if url and str(url).startswith('http'):
            st.markdown(f"### 📺 {target_theme} アーカイブ動画")
            st.video(url)
            st.markdown("---")

def clear_filters():
    """検索条件をすべてリセットする"""
    for key in ["selected_themes", "selected_genres", "selected_platforms", "selected_presenters", "main_search"]:
        if key in st.session_state:
            if key == "main_search":
                st.session_state[key] = ""
            else:
                st.session_state[key] = []

def render_filter_panel(filter_options):
    """
    メインエリアに詳細検索パネルを表示
    """
    with st.expander("🔍 詳細条件で絞り込む"):
        col1, col2 = st.columns(2)
        with col1:
            selected_theme = st.multiselect(
                "配信テーマ",
                options=filter_options['テーマ'],
                key="selected_themes"
            )
            selected_genre = st.multiselect(
                "ジャンル",
                options=filter_options['ジャンル'],
                key="selected_genres"
            )
        with col2:
            selected_platform = st.multiselect(
                "プラットフォーム",
                options=filter_options['プラットフォーム'],
                key="selected_platforms"
            )
            selected_presenter = st.multiselect(
                "発表者",
                options=filter_options['発表者'],
                key="selected_presenters"
            )
        
        # フィルタ適用ボタンは削除（自動反映のため）
        st.button("🔄 検索条件をクリア", key="btn_clear_filter", on_click=clear_filters, use_container_width=True)
    
    return {
        'テーマ': selected_theme,
        'ジャンル': selected_genre,
        'プラットフォーム': selected_platform,
        '発表者': selected_presenter
    }

def _platform_match(val, platform_filters):
    """
    プラットフォーム文字列がフィルタ条件に一致するかチェック
    （複数プラットフォームをカンマ区切りで含む場合に対応）
    """
    if not val:
        return False
    parts = [p.strip() for p in str(val).replace('，', ',').replace('/', ',').split(',')]
    return any(p in platform_filters for p in parts)

@st.cache_data(ttl=300, show_spinner=False)
def _apply_filters_impl(df, filters_tuple):
    """
    フィルタ適用の内部実装（キャッシュ用）
    filtersをタプル形式に変換してキャッシュ効率を向上
    
    Args:
        df: フィルタリング対象のDataFrame
        filters_tuple: フィルタ条件のタプル (テーマ, ジャンル, プラットフォーム, 発表者)
    
    Returns:
        フィルタリングされたDataFrame
    """
    try:
        # タプルを辞書に戻す
        filters = {
            'テーマ': list(filters_tuple[0]) if filters_tuple[0] else [],
            'ジャンル': list(filters_tuple[1]) if filters_tuple[1] else [],
            'プラットフォーム': list(filters_tuple[2]) if filters_tuple[2] else [],
            '発表者': list(filters_tuple[3]) if filters_tuple[3] else []
        }
    except (IndexError, TypeError) as e:
        # タプルの形式が不正な場合、フィルタなしとして返す
        return df.copy()
    
    filtered_df = df.copy()
    
    try:
        if filters['テーマ']:
            filtered_df = filtered_df[filtered_df['表示用テーマ'].isin(filters['テーマ'])]
            
        if filters['ジャンル']:
            filtered_df = filtered_df[filtered_df['ジャンル'].isin(filters['ジャンル'])]
            
        if filters['プラットフォーム']:
            filtered_df = filtered_df[filtered_df['プラットフォーム'].apply(
                lambda val: _platform_match(val, filters['プラットフォーム'])
            )]
            
        if filters['発表者']:
            filtered_df = filtered_df[filtered_df['発表者グループ'].isin(filters['発表者'])]
    except Exception:
        # フィルタ適用中にエラーが発生した場合、元のDataFrameを返す
        return df.copy()
    
    return filtered_df

def apply_filters(df, filters):
    """
    データにフィルターを適用（パフォーマンス最適化: フィルタ条件が同じ場合はキャッシュを使用）
    
    Args:
        df: フィルタリング対象のDataFrame
        filters: フィルタ条件の辞書
            - 'テーマ': 配信テーマのリスト
            - 'ジャンル': ジャンルのリスト
            - 'プラットフォーム': プラットフォームのリスト
            - '発表者': 発表者のリスト
    
    Returns:
        フィルタリングされたDataFrame
    """
    if df.empty:
        return df.copy()
    
    # フィルタがすべて空の場合は、そのまま返す
    if not any(filters.values()):
        return df.copy()
    
    try:
        # フィルタ条件をタプルに変換（キャッシュキーとして使用）
        filters_tuple = (
            tuple(sorted(filters.get('テーマ', []))),
            tuple(sorted(filters.get('ジャンル', []))),
            tuple(sorted(filters.get('プラットフォーム', []))),
            tuple(sorted(filters.get('発表者', [])))
        )
        
        # キャッシュされた関数を使用
        return _apply_filters_impl(df, filters_tuple)
    except Exception:
        # エラーが発生した場合、フィルタなしとして返す
        return df.copy()

def render_song_detail(selected_row, df):
    """
    選択された楽曲の詳細情報をカード形式で表示
    """
    if selected_row is None or (hasattr(selected_row, 'empty') and selected_row.empty):
        return
    
    # selected_rowを辞書形式に変換
    if hasattr(selected_row, 'to_dict'):
        row_dict = selected_row.to_dict()
    else:
        row_dict = dict(selected_row) if selected_row else {}
    
    # 元のDataFrameから全情報を取得（表示用に非表示になっている列も含む）
    # 選択された行の通算番号または曲名で元のDataFrameから検索
    song_name = row_dict.get('曲名', '')
    game_name = row_dict.get('ゲーム名', '')
    
    # 元のDataFrameから該当する行を取得
    match = pd.DataFrame()
    if '通算' in row_dict and row_dict['通算']:
        match = df[df['通算'] == row_dict['通算']]
    elif song_name:
        match = df[(df['曲名'] == song_name) & (df['ゲーム名'] == game_name)]
    
    if not match.empty:
        song_data = match.iloc[0].to_dict()
    else:
        # フォールバック: 選択された行のデータをそのまま使用
        song_data = row_dict
    
    # 配信回の整形
    try:
        disc_val = int(float(str(song_data.get('DISC', '')).strip()))
        ep_str = f"第{disc_val:03d}回"
    except (ValueError, TypeError):
        ep_str = str(song_data.get('DISC', '不明'))
    
    # 詳細カードの表示
    st.markdown('<div class="song-detail-card">', unsafe_allow_html=True)
    
    # 曲名
    st.markdown(f'<div class="song-detail-title">{song_data.get("曲名", "曲名不明")}</div>', unsafe_allow_html=True)
    
    # ゲーム名
    st.markdown(f'<div class="song-detail-subtitle">出典: {song_data.get("ゲーム名", "ゲーム名不明")}</div>', unsafe_allow_html=True)
    
    # 基本情報
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div class="song-detail-info"><span class="song-detail-label">通算番号:</span> {song_data.get("通算", "不明")}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="song-detail-info"><span class="song-detail-label">配信回:</span> {ep_str}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="song-detail-info"><span class="song-detail-label">テーマ:</span> {song_data.get("テーマ", "不明")}</div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="song-detail-info"><span class="song-detail-label">ジャンル:</span> {song_data.get("ジャンル", "不明")}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="song-detail-info"><span class="song-detail-label">プラットフォーム:</span> {song_data.get("プラットフォーム", "不明")}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="song-detail-info"><span class="song-detail-label">発表者:</span> {song_data.get("発表者", "不明")}</div>', unsafe_allow_html=True)
    
    # アーカイブ動画リンク
    archive_url = song_data.get('アーカイブURL', '') or song_data.get('Archive_URL', '')
    if archive_url and str(archive_url).startswith('http'):
        st.markdown("---")
        st.markdown("### 📺 アーカイブ動画")
        st.video(archive_url)
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_results(df, mode="search", key=None):
    """
    検索結果を st-aggrid で表示し、選択された行の詳細情報を表示
    （パフォーマンス最適化: カラム構成が同じ場合はGridOptionsBuilderの設定をキャッシュ）
    """
    if df.empty:
        st.info("該当する楽曲が見つかりませんでした。")
        st.markdown("""
            <div style="background-color: rgba(0, 219, 222, 0.1); border: 1px solid rgba(0, 219, 222, 0.3); border-radius: 12px; padding: 1.5rem; margin-top: 1rem;">
                <p style="color: #e0e0e0; margin-bottom: 1rem;">💡 検索条件を変更してみてください：</p>
                <ul style="color: #b0b0b0; margin-left: 1.5rem;">
                    <li>キーワードを変更する</li>
                    <li>フィルタ条件を緩和する</li>
                    <li>検索条件をクリアして最初からやり直す</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        return

    if mode == "all":
        display_order = ['通算', 'DISC', 'テーマ', '曲名', 'ゲーム名', '発表者', 'ジャンル', 'プラットフォーム']
    else:
        display_order = ['曲名', 'ゲーム名', 'DISC', 'テーマ', '発表者', '通算']

    cols_to_use = [c for c in display_order if c in df.columns]
    other_cols = [c for c in df.columns if c not in cols_to_use]
    df_display = df[cols_to_use + other_cols]

    # カラム構成のキャッシュキーを生成
    cols_tuple = tuple(sorted(df_display.columns))
    cache_key = f"grid_options_{mode}_{cols_tuple}"
    
    # セッション状態でGridOptionsBuilderの設定をキャッシュ
    if cache_key not in st.session_state:
        gb = GridOptionsBuilder.from_dataframe(df_display)
        gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=50)
        gb.configure_side_bar()
        gb.configure_selection('single')
        
        if '通算' in df_display.columns:
            gb.configure_column("通算", sort="desc")

        hidden_cols = ['発表者グループ', '表示用テーマ', 'ジャンルID', 'アーカイブURL', 'Archive_URL'] + other_cols
        
        for col in df_display.columns:
            if col in hidden_cols:
                gb.configure_column(col, hide=True)
            else:
                if col == '曲名':
                    gb.configure_column(col, pinned='left', width=200)
                elif col == 'ゲーム名':
                    gb.configure_column(col, width=200)
                elif col == '通算':
                    gb.configure_column(col, headerName="通算No.", width=80)
                elif col == 'DISC':
                    gb.configure_column(col, headerName="配信回", width=80)
                elif col == 'テーマ':
                    gb.configure_column(col, width=200)
                elif col == '発表者':
                    gb.configure_column(col, width=120)

        st.session_state[cache_key] = gb.build()
    
    grid_options = st.session_state[cache_key]

    # AgGridの戻り値から選択された行を取得
    grid_response = AgGrid(
        df_display,
        gridOptions=grid_options,
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
        allow_unsafe_jscode=True, 
        theme='streamlit',
        key=key,
        update_mode='SELECTION_CHANGED',
        return_mode=DataReturnMode.FILTERED
    )
    
    # 選択された行がある場合、詳細情報を表示
    selected_rows = grid_response.get('selected_rows', [])
    # selected_rowsがリストかDataFrameかをチェック
    if isinstance(selected_rows, pd.DataFrame):
        if not selected_rows.empty:
            render_song_detail(selected_rows.iloc[0], df)
    elif isinstance(selected_rows, list) and len(selected_rows) > 0:
        selected_df = pd.DataFrame(selected_rows)
        if not selected_df.empty:
            render_song_detail(selected_df.iloc[0], df)

def render_result_count_badge(result_count):
    """
    検索結果件数をバッジ形式で表示（色分け対応）
    
    Args:
        result_count: 検索結果の件数
    
    Returns:
        HTML文字列（st.markdownで使用可能）
    """
    if result_count == 0:
        badge_color = "#808080"  # グレー
        badge_text = "0件"
    elif result_count <= 10:
        badge_color = "#ff8800"  # オレンジ
        badge_text = f"{result_count}件"
    else:
        badge_color = "#00dbde"  # シアン（緑系）
        badge_text = f"{result_count}件"
    
    return f"""
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 0.5rem;">
            <h2 style="margin: 0; color: #00dbde; font-size: 2rem;">🔍 検索結果</h2>
            <span style="background-color: {badge_color}; color: #ffffff; padding: 6px 16px; border-radius: 20px; font-weight: 700; font-size: 1.1rem; box-shadow: 0 2px 8px rgba(0,0,0,0.3);">
                {badge_text}
            </span>
        </div>
    """

def render_active_filters(filters, search_query=""):
    """
    現在適用されている検索条件をタグ形式で表示する
    """
    tags_html = '<div style="display: flex; flex-wrap: wrap; margin-bottom: 1.5rem;">'
    has_any_filter = False

    # キーワード検索
    if search_query and search_query.strip():
        tags_html += f'<div class="filter-tag"><span class="filter-tag-label">キーワード:</span> {search_query}</div>'
        has_any_filter = True

    # フィルタ条件
    filter_labels = {
        'テーマ': 'テーマ',
        'ジャンル': 'ジャンル',
        'プラットフォーム': 'ハード',
        '発表者': '発表者'
    }

    for key, label in filter_labels.items():
        selected_items = filters.get(key, [])
        if selected_items:
            has_any_filter = True
            for item in selected_items:
                tags_html += f'<div class="filter-tag"><span class="filter-tag-label">{label}:</span> {item}</div>'
    
    tags_html += '</div>'

    if has_any_filter:
        st.markdown(tags_html, unsafe_allow_html=True)

def render_entrance_screen(latest_theme):
    """
    初期表示のエントランス画面を描画（簡略化版）
    """
    st.markdown(f"""
        <div style="text-align: center; padding: 40px 20px;">
            <div style="font-size: 5rem; margin-bottom: 10px;">🎧</div>
            <h2 style="color: #00dbde; font-weight: 700;">語る会Libraryへようこそ</h2>
            <p style="color: #b0b0b0; font-size: 1.1rem; max-width: 600px; margin: 0 auto 20px auto;">
                🔍 キーワード検索 または 📋 詳細条件で絞り込んで、<br>
                思い出の曲を見つけましょう。
            </p>
        </div>
    """, unsafe_allow_html=True)

def render_random_card(song, df_candidates, key_suffix=""):
    """
    ランダム表示された曲をカード形式で描画（ルーレット演出対応）
    
    Args:
        song: 表示する楽曲データ（Series）
        df_candidates: ルーレット演出用の候補楽曲リスト（DataFrame）
        key_suffix: キー識別用のサフィックス
    """
    try:
        ep_val = int(float(str(song['DISC']).strip()))
        ep_str = f"第{ep_val:03d}回"
    except (ValueError, TypeError, KeyError):
        ep_str = "配信回不明"

    # ルーレット演出用の候補データをJSON形式で準備（最大30曲）
    candidates = []
    if not df_candidates.empty:
        sample_df = df_candidates.sample(min(30, len(df_candidates)))
        for _, row in sample_df.iterrows():
            try:
                cand_ep = int(float(str(row['DISC']).strip()))
                cand_ep_str = f"第{cand_ep:03d}回"
            except (ValueError, TypeError, KeyError):
                cand_ep_str = "配信回不明"
            
            candidates.append({
                'song': str(row.get('曲名', '')),
                'game': str(row.get('ゲーム名', '')),
                'ep': cand_ep_str,
                'theme': str(row.get('テーマ', 'なし')),
                'number': str(row.get('通算', '???'))
            })
    
    # 次の楽曲データも事前に準備（候補からランダムに選択）
    next_song_data = None
    if candidates:
        next_song_data = random.choice(candidates)
    else:
        next_song_data = {
            'song': str(song.get('曲名', '')),
            'game': str(song.get('ゲーム名', '')),
            'ep': ep_str,
            'theme': str(song.get('テーマ', 'なし')),
            'number': str(song.get('通算', '???'))
        }

    # 現在の楽曲データもJSON形式で
    current_data = {
        'song': str(song.get('曲名', '')),
        'game': str(song.get('ゲーム名', '')),
        'ep': ep_str,
        'theme': str(song.get('テーマ', 'なし')),
        'number': str(song.get('通算', '???'))
    }

    # ルーレット演出用のJavaScriptを含むHTML
    candidates_json = json.dumps(candidates, ensure_ascii=False)
    current_json = json.dumps(current_data, ensure_ascii=False)
    next_json = json.dumps(next_song_data, ensure_ascii=False)
    
    # シャッフルフラグをセッション状態で管理
    shuffle_flag_key = f'shuffle_trigger_{key_suffix}'
    if shuffle_flag_key not in st.session_state:
        st.session_state[shuffle_flag_key] = 0
    
    # シャッフルトリガーのカウンターをチェック
    should_start_roulette = st.session_state.get(shuffle_flag_key, 0) > 0
    if should_start_roulette:
        st.session_state[shuffle_flag_key] = 0  # リセット
    
    st.markdown(f"""
        <div class="random-card" id="random-card-{key_suffix}">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px;">
                <span style="color: #fc00ff; font-weight: bold; font-size: 0.9rem;">✨ ランダム表示</span>
                <span style="color: #00dbde; font-size: 0.8rem; background: rgba(0,219,222,0.1); padding: 2px 10px; border-radius: 10px;" id="random-number-{key_suffix}">No.{song.get('通算', '???')}</span>
            </div>
            <h3 style="margin: 5px 0 10px 0; font-size: 1.8rem; line-height: 1.2; color: #ffffff;" id="random-song-{key_suffix}">{song['曲名']}</h3>
            <p style="margin: 0; color: #e0e0e0; font-size: 1.1rem; font-weight: 500;" id="random-game-{key_suffix}">出典: {song['ゲーム名']}</p>
            <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(255,255,255,0.1); display: flex; gap: 20px; margin-bottom: 20px;">
                <div>
                    <p style="margin: 0; color: #b0b0b0; font-size: 0.8rem;">放送回</p>
                    <p style="margin: 0; color: #ffffff; font-weight: bold;" id="random-ep-{key_suffix}">{ep_str}</p>
                </div>
                <div>
                    <p style="margin: 0; color: #b0b0b0; font-size: 0.8rem;">テーマ</p>
                    <p style="margin: 0; color: #ffffff; font-weight: bold;" id="random-theme-{key_suffix}">{song.get('テーマ', 'なし')}</p>
                </div>
            </div>
        </div>
        
        <script>
        (function() {{
            const candidates = {candidates_json};
            const currentData = {current_json};
            const nextData = {next_json};
            const keySuffix = '{key_suffix}';
            let isRouletteRunning = false;
            
            // ルーレット演出関数
            function startRoulette(finalData) {{
                if (isRouletteRunning) return; // 既に実行中の場合はスキップ
                isRouletteRunning = true;
                
                const songEl = document.getElementById('random-song-' + keySuffix);
                const gameEl = document.getElementById('random-game-' + keySuffix);
                const epEl = document.getElementById('random-ep-' + keySuffix);
                const themeEl = document.getElementById('random-theme-' + keySuffix);
                const numberEl = document.getElementById('random-number-' + keySuffix);
                
                if (!songEl || !gameEl || !epEl || !themeEl || !numberEl) {{
                    isRouletteRunning = false;
                    return;
                }}
                
                const duration = 500; // 0.5秒
                const interval = 25; // 25msごとに切り替え（約20回/0.5秒で高速切り替え）
                let elapsed = 0;
                
                const rouletteInterval = setInterval(() => {{
                    elapsed += interval;
                    
                    // 候補からランダムに選んで表示（高速に切り替え）
                    if (candidates.length > 0) {{
                        const randomIndex = Math.floor(Math.random() * candidates.length);
                        const candidate = candidates[randomIndex];
                        
                        songEl.textContent = candidate.song;
                        gameEl.textContent = '出典: ' + candidate.game;
                        epEl.textContent = candidate.ep;
                        themeEl.textContent = candidate.theme;
                        numberEl.textContent = 'No.' + candidate.number;
                    }}
                    
                    // 0.3秒経過したら最終データを表示して停止
                    if (elapsed >= duration) {{
                        clearInterval(rouletteInterval);
                        songEl.textContent = finalData.song;
                        gameEl.textContent = '出典: ' + finalData.game;
                        epEl.textContent = finalData.ep;
                        themeEl.textContent = finalData.theme;
                        numberEl.textContent = 'No.' + finalData.number;
                        isRouletteRunning = false;
                    }}
                }}, interval);
            }}
            
            // ボタンクリックイベントをリッスン
            function setupButtonListener() {{
                const checkButton = setInterval(() => {{
                    const buttons = document.querySelectorAll('button');
                    buttons.forEach(btn => {{
                        if (btn.textContent.includes('🎲 ランダムシャッフル') && !btn.dataset.rouletteSetup) {{
                            btn.dataset.rouletteSetup = 'true';
                            btn.addEventListener('click', function(e) {{
                                // ルーレット演出を開始
                                startRoulette(nextData);
                            }}, {{ once: true }});
                        }}
                    }});
                }}, 100);
                
                setTimeout(() => clearInterval(checkButton), 3000);
            }}
            
            // ページロード時にセットアップ
            if (document.readyState === 'loading') {{
                document.addEventListener('DOMContentLoaded', setupButtonListener);
            }} else {{
                setupButtonListener();
            }}
            
            // シャッフルトリガーが設定されている場合は即座にルーレットを開始
            const shouldStart = {1 if should_start_roulette else 0};
            if (shouldStart === 1) {{
                setTimeout(() => {{
                    startRoulette(nextData);
                }}, 100); // DOM更新を待つ
            }}
        }})();
        </script>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([7, 3])
    with col2:
        st.markdown('<div style="margin-top: -45px;"></div>', unsafe_allow_html=True)
        shuffle_clicked = st.button("🎲 ランダムシャッフル", key=f"next_random_{key_suffix}", use_container_width=True)
        if shuffle_clicked:
            # ボタンがクリックされたら、シャッフルフラグを立てて新しい楽曲を選択
            st.session_state[shuffle_flag_key] = 1
            return True
    
    st.markdown('<div style="margin-bottom: 40px;"></div>', unsafe_allow_html=True)
    return False
