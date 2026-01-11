import streamlit as st
import pandas as pd
from src.data_loader import load_gsheet_data, get_filter_options
from src.search_engine import fuzzy_search
from src.ui import (
    apply_filters, display_results, 
    load_custom_css, render_entrance_screen, render_random_card,
    render_filter_panel, render_theme_list_page,
    render_archive_video, render_result_count_badge
)
from src.auth import check_password

# ページ設定
st.set_page_config(
    page_title="語る会Library",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def main():
    # パスワード認証チェック
    # secrets.tomlからパスワードハッシュを取得（設定されていない場合は認証をスキップ）
    try:
        password_hash = st.secrets.get("app", {}).get("password_hash", None)
        if password_hash:
            if not check_password(password_hash):
                return  # 認証失敗時は処理を中断
    except Exception:
        # secrets.tomlにappセクションがない場合は認証をスキップ
        pass
    # カスタムCSSの適用
    load_custom_css()

    st.markdown('<h1 class="main-title">語る会Library</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-text">〜 語り合った、心躍るゲーム音楽の図鑑 〜</p>', unsafe_allow_html=True)

    # データの読み込み
    if 'data_load_retry' not in st.session_state:
        st.session_state['data_load_retry'] = False
    
    if st.session_state.get('data_load_retry', False):
        st.session_state['data_load_retry'] = False
    
    with st.spinner("データを読み込んでいます..."):
        df = load_gsheet_data()

    if df.empty:
        st.error("データの読み込みに失敗しました。認証情報やスプレッドシートの設定を確認してください。")
        if st.button("🔄 再試行", key="btn_retry_load"):
            st.session_state['data_load_retry'] = True
            st.rerun()
        return

    # フィルターオプションの取得
    filter_options = get_filter_options(df)

    # 配信テーマの初期選択（初回実行時のみセット）
    # ウィジェットが作成される前に実行される必要がある
    if 'selected_themes' not in st.session_state:
        if filter_options['テーマ']:
            st.session_state['selected_themes'] = [filter_options['テーマ'][0]]
        else:
            st.session_state['selected_themes'] = []

    # タブの作成
    tab_search, tab_themes, tab_all = st.tabs(["🔍 楽曲検索", "📺 配信テーマ一覧", "📚 全曲リスト"])

    with tab_search:
        # キーワード検索の入力
        col_search1, col_search2 = st.columns([8, 2])
        with col_search1:
            search_query = st.text_input("キーワード検索 (曲名, ゲーム名, シリーズ...)", placeholder="例: マリオ", key="main_search", label_visibility="collapsed")
        with col_search2:
            search_clicked = st.button("🔍 検索", key="btn_search_keyword", use_container_width=True)

        # 詳細検索パネル
        filters = render_filter_panel(filter_options)

        # 最新のテーマを取得
        latest_theme = filter_options['テーマ'][0] if filter_options['テーマ'] else None

        # フィルタ変更の検知（前回のフィルタ状態と比較）
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

        # 検索とフィルタリング
        processed_df = apply_filters(df, filters)
        
        if search_query:
            processed_df = fuzzy_search(processed_df, search_query)

        # ユーザーが何か操作をしたか判定
        is_active = any(filters.values()) or (bool(search_query) and search_query != " ")

        # 検索ボタンがクリックされた場合のフィードバック
        if search_clicked and search_query:
            st.success("🔍 検索を実行しました")
        
        # フィルタ変更時のフィードバック
        if filters_changed and is_active:
            st.success(f"🔍 検索結果を更新しました ({len(processed_df)}件)")

        if is_active:
            # 検索結果件数の視覚的強調（カード/バッジ形式、色分け）
            result_count = len(processed_df)
            st.markdown(render_result_count_badge(result_count), unsafe_allow_html=True)
            
            # 適用中のフィルタをタグ形式で表示
            from src.ui import render_active_filters
            render_active_filters(filters, search_query)
            
            display_results(processed_df, key="ag_search_results")

        # アーカイブ動画の表示
        if filters['テーマ']:
            render_archive_video(df, filters['テーマ'])

        # --- ランダム表示のカード ---
        if 'random_song' not in st.session_state:
            st.session_state['random_song'] = df.sample(1)
        
        # 常時全曲から選ぶように変更
        if render_random_card(st.session_state['random_song'].iloc[0], df, key_suffix="top"):
            st.session_state['random_song'] = df.sample(1)
            st.rerun()

        if not is_active:
            # 初期表示画面（エントランス）
            render_entrance_screen(latest_theme)

    with tab_themes:
        render_theme_list_page(df)

    with tab_all:
        st.subheader(f"📚 全曲リスト ({len(df)}件)")
        display_results(df, mode="all", key="ag_all_list")

if __name__ == "__main__":
    main()
