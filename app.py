import streamlit as st
import pandas as pd
from src.data_loader import load_gsheet_data, get_filter_options
from src.search_engine import fuzzy_search
from src.ui import (
    apply_filters, display_results, 
    load_custom_css, render_entrance_screen, render_random_card,
    render_filter_panel, render_theme_list_page,
    render_archive_video, render_result_count_badge,
    render_enhanced_dashboard  # Updated to use enhanced version
)
from src.auth import check_password

# ページ設定
st.set_page_config(
    page_title="語る会Library",
    page_icon="👾",  # レトロゲームに合わせてアイコン変更
    layout="wide",
    initial_sidebar_state="collapsed"
)

def main():
    # パスワード認証チェック
    try:
        password_hash = st.secrets.get("app", {}).get("password_hash", None)
        if password_hash:
            if not check_password(password_hash):
                return
    except Exception:
        pass
        
    # カスタムCSSの適用（レトロモダンテーマ）
    load_custom_css()

    st.markdown('<h1 class="main-title">語る会LIBRARY</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-text">〜 LEGENDARY GAME MUSIC ARCHIVES 〜</p>', unsafe_allow_html=True)

    # データの読み込み
    if 'data_load_retry' not in st.session_state:
        st.session_state['data_load_retry'] = False
    
    if st.session_state.get('data_load_retry', False):
        st.session_state['data_load_retry'] = False
    
    with st.spinner("LOADING DATA..."):
        df = load_gsheet_data()

    if df.empty:
        st.error("SYSTEM ERROR: Data load failed.")
        if st.button("🔄 RETRY", key="btn_retry_load"):
            st.session_state['data_load_retry'] = True
            st.rerun()
        return

    # フィルターオプションの取得
    filter_options = get_filter_options(df)

    # 配信テーマの初期選択
    if 'selected_themes' not in st.session_state:
        if filter_options['テーマ']:
            st.session_state['selected_themes'] = [filter_options['テーマ'][0]]
        else:
            st.session_state['selected_themes'] = []

    # タブの作成（STATSタブを追加）
    tab_search, tab_themes, tab_all, tab_stats = st.tabs(["🔍 SEARCH", "📺 EPISODES", "📚 ALL RECORDS", "📊 STATS"])

    with tab_search:
        # キーワード検索の入力
        col_search1, col_search2 = st.columns([8, 2])
        with col_search1:
            # リアルタイム検索っぽく見せるため、formを使わず直書き
            search_query = st.text_input("KEYWORD SEARCH", placeholder="Input Title, Game, or Series...", key="main_search", label_visibility="collapsed")
        with col_search2:
            # 検索ボタンは念のため残すが、入力だけで動作する
            search_clicked = st.button("GO", key="btn_search_keyword", use_container_width=True)

        # 詳細検索パネル
        filters = render_filter_panel(filter_options)

        # フィルタ変更の検知
        if 'prev_filters' not in st.session_state:
            st.session_state['prev_filters'] = filters.copy()
        
        filters_changed = (
            st.session_state['prev_filters']['テーマ'] != filters['テーマ'] or
            st.session_state['prev_filters']['ジャンル'] != filters['ジャンル'] or
            st.session_state['prev_filters']['プラットフォーム'] != filters['プラットフォーム'] or
            st.session_state['prev_filters']['発表者'] != filters['発表者']
        )
        
        if filters_changed:
            st.session_state['prev_filters'] = filters.copy()
            # ページネーションリセット
            if 'card_page_ag_search_results' in st.session_state:
                st.session_state['card_page_ag_search_results'] = 0

        # データ処理
        processed_df = df.copy() # ベースは全データ
        
        # フィルタ適用
        processed_df = apply_filters(processed_df, filters)
        
        # キーワード検索
        if search_query:
            processed_df = fuzzy_search(processed_df, search_query)

        # アクティブ状態の判定
        is_active = any(filters.values()) or (bool(search_query) and search_query.strip() != "")

        if is_active:
            # 結果数表示
            st.markdown(render_result_count_badge(len(processed_df)), unsafe_allow_html=True)
            
            # 検索フィルターの表示
            from src.ui import render_active_filters
            render_active_filters(filters, search_query)
            
            # 結果表示（カード/グリッド切り替え対応版）
            display_results(processed_df, key="ag_search_results")

        # アーカイブ動画の表示（テーマ選択時）
        if filters['テーマ']:
            render_archive_video(df, filters['テーマ'])

        if not is_active:
            render_entrance_screen(filter_options['テーマ'][0] if filter_options['テーマ'] else None)

    with tab_themes:
        render_theme_list_page(df)

    with tab_all:
        st.subheader(f"📚 ALL RECORDS ({len(df)})")
        display_results(df, mode="all", key="ag_all_list")
    
    with tab_stats:
        # 統計ダッシュボード（グラフ付き）を表示
        render_enhanced_dashboard(df)

if __name__ == "__main__":
    main()
