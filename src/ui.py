import streamlit as st
import pandas as pd
import time
import json
import streamlit as st
import math
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, ColumnsAutoSizeMode, DataReturnMode

def load_custom_css():
    """
    アプリ全体の見た目を整えるカスタムCSSを注入（目に優しいレトロモダンVer.）
    """
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DotGothic16&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;900&display=swap');

        /* =========================================
           1. 全体レイアウト & 変数定義
           ========================================= */
        :root {
            --bg-color: #0b1021;       /* 深い群青 (Midnight Deep) */
            --card-bg: #15192b;        /* カード背景 */
            --text-main: #d4d4d8;      /* オフホワイト (目に優しい) */
            --text-sub: #9ca3af;       /* サブテキスト (グレー) */
            --accent-primary: #4ec9b0; /* ソフトミント (Teal) */
            --accent-secondary: #ce9178; /* レトロオレンジ (Warm) */
            --accent-border: #2d3748;  /* 枠線色 */
            --font-pixel: 'DotGothic16', sans-serif;
            --font-game: 'Orbitron', sans-serif;
            --font-base: 'Inter', sans-serif;
        }

        .stApp {
            background-color: var(--bg-color);
            background-image: 
                linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.1) 50%),
                linear-gradient(90deg, rgba(255, 0, 0, 0.03), rgba(0, 255, 0, 0.01), rgba(0, 0, 255, 0.03));
            background-size: 100% 2px, 3px 100%; /* 走査線風エフェクト */
            color: var(--text-main);
            font-family: var(--font-base);
        }

        /* ピクセルフォント適用箇所 */
        h2, h3, .stButton button, .pixel-font, .stat-value, .filter-tag, .stSelectbox p {
            font-family: var(--font-pixel) !important;
            letter-spacing: 0.05em;
        }

        .main .block-container {
            padding: 2rem 2rem;
            max-width: 1400px;
        }

        /* =========================================
           2. タイトルエリア
           ========================================= */
        .main-title {
            font-family: var(--font-game) !important;
            font-size: 2.8rem !important;
            font-weight: 900 !important;
            color: var(--accent-primary);
            text-shadow: 3px 3px 0px var(--accent-border), 0 0 20px rgba(78, 201, 176, 0.3);
            text-align: center;
            margin-bottom: 0.5rem;
            line-height: 1.3;
            letter-spacing: 0.05em;
        }
        .sub-text {
            text-align: center;
            color: rgba(255, 255, 255, 0.7) !important;
            font-family: var(--font-base);
            font-size: 0.9rem !important;
            margin-bottom: 1rem;
            padding-bottom: 0;
            margin-left: auto;
            margin-right: auto;
        }
        .sub-text-border {
            width: 60%;
            max-width: 600px;
            height: 2px;
            background: linear-gradient(to right, transparent, var(--accent-border) 20%, var(--accent-border) 80%, transparent);
            margin: 0 auto 2rem auto;
        }

        /* 見出しの共通化 */
        h2, h3 {
            color: var(--accent-secondary) !important;
        }

        /* =========================================
           3. ダッシュボード (RPGステータス風)
           ========================================= */
        .dashboard-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }
        .stat-box {
            background: var(--card-bg);
            border: 2px solid var(--accent-border);
            border-radius: 4px;
            padding: 1rem;
            text-align: center;
            position: relative;
            box-shadow: 4px 4px 0px rgba(0,0,0,0.3);
            transition: transform 0.2s;
        }
        .stat-box:hover {
            transform: translateY(-2px);
            border-color: var(--accent-primary);
        }
        .stat-label {
            display: block;
            color: var(--text-sub);
            font-size: 0.8rem;
            margin-bottom: 0.2rem;
            font-family: var(--font-pixel);
        }
        .stat-value {
            display: block;
            font-size: 1.8rem;
            font-weight: bold;
            color: var(--accent-secondary);
        }

        /* タブのスタイル */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            font-family: var(--font-pixel) !important;
            color: rgba(255, 255, 255, 0.75) !important;
            border-radius: 4px 4px 0 0;
            padding: 0.5rem 1rem;
            background-color: transparent;
        }
        .stTabs [aria-selected="true"] {
            background-color: var(--card-bg) !important;
            color: var(--accent-primary) !important;
            border-bottom: 3px solid var(--accent-primary) !important;
        }

        /* =========================================
           4. コンポーネント (入力、ボタン)
           ========================================= */
        .stTextInput > div > div > input {
            background-color: var(--card-bg) !important;
            color: var(--text-main) !important;
            border: 2px solid var(--accent-primary) !important;
            border-radius: 4px !important;
            font-family: var(--font-pixel) !important;
            font-size: 1.1rem;
        }
        .stTextInput > div > div > input::placeholder {
            color: rgba(255, 255, 255, 0.5) !important;
            opacity: 1 !important;
        }
        .stTextInput > div > div > input:focus {
            border-color: var(--accent-primary) !important;
            box-shadow: 0 0 0 2px rgba(78, 201, 176, 0.3) !important;
        }

        .stButton > button {
            background-color: var(--card-bg) !important;
            color: var(--accent-primary) !important;
            border: 2px solid var(--accent-primary) !important;
            border-radius: 0px !important;
            box-shadow: 3px 3px 0px var(--accent-border);
            transition: all 0.1s;
        }
        .stButton > button:hover {
            transform: translate(1px, 1px);
            box-shadow: 2px 2px 0px var(--accent-border);
            color: #fff !important;
            background-color: var(--accent-primary) !important;
        }

        /* マルチセレクトのスタイル */
        .stMultiSelect label {
            color: #ffffff !important;
            font-weight: 600 !important;
        }
        .stMultiSelect > div > div {
            background-color: var(--card-bg) !important;
            border-radius: 4px !important;
            border: 2px solid var(--accent-primary) !important;
            transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
        }
        .stMultiSelect > div > div:hover,
        .stMultiSelect > div > div:focus-within {
            border-color: var(--accent-secondary) !important;
            box-shadow: 0 0 0 3px rgba(206, 145, 120, 0.2) !important;
        }
        .stMultiSelect [data-baseweb="tag"] {
            background-color: var(--accent-primary) !important;
            color: #000000 !important;
        }
        /* セレクトボックス */
        .stSelectbox > div > div {
             background-color: var(--card-bg) !important;
             border: 2px solid var(--accent-primary) !important;
             border-radius: 4px !important;
        }
        .stSelectbox label {
            color: #ffffff !important;
            font-weight: 600 !important;
        }
        .stSelectbox [data-baseweb="select"] {
            color: rgba(255, 255, 255, 0.9) !important;
        }
        .stSelectbox [data-baseweb="select"] > div {
            color: rgba(255, 255, 255, 0.9) !important;
        }

        /* =========================================
           5. カード型リスト
           ========================================= */
        .song-card-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1rem;
            padding: 1rem 0;
        }
        .song-card {
            background-color: var(--card-bg);
            border: 2px solid var(--accent-border);
            border-radius: 4px;
            padding: 0.8rem;
            position: relative;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            min-height: 120px;
            transition: all 0.2s ease;
        }
        .song-card:hover {
            border-color: var(--accent-secondary);
            box-shadow: 0 0 15px rgba(206, 145, 120, 0.1);
            transform: translateY(-2px);
        }
        .card-header {
            border-bottom: 1px dashed var(--accent-border);
            padding-bottom: 0.4rem;
            margin-bottom: 0.5rem;
        }
        .card-song-title {
            font-family: var(--font-pixel);
            font-size: 1rem;
            color: var(--accent-primary);
            margin: 0;
            line-height: 1.3;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }
        .card-game-title {
            font-size: 0.8rem;
            color: var(--text-main);
            margin-top: 0.3rem;
            font-weight: 500;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .card-meta {
            font-size: 0.75rem;
            color: var(--text-sub);
            margin-top: auto;
            padding-top: 0.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .card-tag {
            display: inline-block;
            background: rgba(255,255,255,0.05);
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 0.7rem;
            border: 1px solid var(--accent-border);
        }

        /* =========================================
           6. その他UI
           ========================================= */
        .stExpander {
            border: 2px solid var(--accent-border) !important;
            background-color: var(--card-bg) !important;
            border-radius: 4px !important;
        }
        
        .filter-tag {
            background-color: rgba(78, 201, 176, 0.1);
            color: var(--accent-primary);
            border: 1px solid var(--accent-primary);
            border-radius: 0px; 
            padding: 4px 12px;
            margin-right: 8px;
            display: inline-block;
        }
        /* AgGrid のカスタマイズ（レトロ調） */
        .ag-theme-streamlit {
            --ag-background-color: var(--card-bg) !important;
            --ag-header-background-color: #1a1f35 !important;
            --ag-odd-row-background-color: #1a1f35 !important;
            --ag-row-hover-color: rgba(78, 201, 176, 0.1) !important;
            --ag-border-color: var(--accent-border) !important;
            --ag-header-foreground-color: var(--accent-primary) !important;
            --ag-foreground-color: var(--text-main) !important;
            font-family: var(--font-base) !important;
        }
        .ag-header-cell-text {
            font-family: var(--font-pixel) !important;
            font-weight: 600 !important;
        }
        /* モバイル対応：列幅の最適化 */
        @media (max-width: 768px) {
            .ag-theme-streamlit .ag-header-cell,
            .ag-theme-streamlit .ag-cell {
                min-width: 80px !important;
            }
        }

        /* スクロールバー */
        ::-webkit-scrollbar {
            width: 12px;
        }
        ::-webkit-scrollbar-track {
            background: var(--bg-color);
        }
        ::-webkit-scrollbar-thumb {
            background: var(--accent-border);
            border: 2px solid var(--bg-color);
            border-radius: 6px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: var(--accent-secondary);
        }
        </style>
    """, unsafe_allow_html=True)

def render_result_count_badge(count):
    """検索結果数を表示するHTML（レトロ調）"""
    return f"""
    <div style="font-family: 'DotGothic16'; color: var(--accent-secondary); margin-bottom: 1rem; font-size: 1.2rem;">
        検索結果: {count} 件
    </div>
    """

def render_dashboard(df):
    """
    データ全体の統計情報を表示するダッシュボード
    """
    total_songs = len(df)
    total_games = df['ゲーム名'].nunique() if 'ゲーム名' in df.columns else 0
    # ユニークな配信回数
    try:
        total_eps = df['DISC'].nunique() if 'DISC' in df.columns else 0
    except:
        total_eps = 0

    st.markdown(f"""
    <div class="dashboard-container">
        <div class="stat-box">
            <span class="stat-label">総楽曲数</span>
            <span class="stat-value">{total_songs}</span>
        </div>
        <div class="stat-box">
            <span class="stat-label">ゲーム数</span>
            <span class="stat-value">{total_games}</span>
        </div>
        <div class="stat-box">
            <span class="stat-label">配信回数</span>
            <span class="stat-value">{total_eps}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_genre_distribution_chart(df):
    """
    ジャンル分布をドーナツチャートで表示
    """
    import plotly.graph_objects as go
    
    if 'ジャンル' not in df.columns or df.empty:
        return
    
    # ジャンル別の曲数を集計（空文字を除外）
    genre_counts = df[df['ジャンル'] != '']['ジャンル'].value_counts()
    
    if genre_counts.empty:
        return
    
    # レトロカラーパレット
    colors = ['#4ec9b0', '#ce9178', '#569cd6', '#c586c0', '#dcdcaa', '#9cdcfe']
    
    fig = go.Figure(data=[go.Pie(
        labels=genre_counts.index,
        values=genre_counts.values,
        hole=0.4,  # ドーナツ型
        marker=dict(
            colors=colors,
            line=dict(color='#2d3748', width=2)
        ),
        textfont=dict(
            family='DotGothic16, sans-serif',
            size=14,
            color='#d4d4d8'
        )
    )])
    
    fig.update_layout(
        title=dict(
            text='ジャンル分布',
            font=dict(family='DotGothic16, sans-serif', size=20, color='#4ec9b0'),
            x=0.5,
            xanchor='center'
        ),
        paper_bgcolor='#15192b',
        plot_bgcolor='#15192b',
        font=dict(family='DotGothic16, sans-serif', color='#d4d4d8'),
        showlegend=True,
        legend=dict(
            font=dict(size=12),
            bgcolor='rgba(0,0,0,0)',
            bordercolor='#2d3748',
            borderwidth=1
        ),
        height=400,
        margin=dict(t=60, b=20, l=20, r=20)
    )
    
    st.plotly_chart(fig, use_container_width=True, key="genre_chart")

def render_top_games_chart(df, top_n=10):
    """
    人気ゲームTOP10を横長カードで表示
    上位3位: 1列フル幅、4位以下: 2列表示
    """
    if 'ゲーム名' not in df.columns or df.empty:
        return
    
    # ゲーム別の曲数を集計してTOP N取得（空文字を除外）
    game_counts = df[df['ゲーム名'] != '']['ゲーム名'].value_counts().head(top_n)
    
    if game_counts.empty:
        return
    
    st.markdown("#### 人気ゲーム TOP 10")
    
    # 上位3位を1列で表示
    for rank, (game_name, count) in enumerate(list(game_counts.items())[:3], 1):
        # ランクに応じた色
        if rank == 1:
            rank_color = "#FFD700"  # ゴールド
            rank_icon = "🥇"
        elif rank == 2:
            rank_color = "#C0C0C0"  # シルバー
            rank_icon = "🥈"
        elif rank == 3:
            rank_color = "#CD7F32"  # ブロンズ
            rank_icon = "🥉"
        
        card_html = f"""
        <div style="
            background: linear-gradient(135deg, var(--card-bg) 0%, #1a1f35 100%);
            border: 2px solid var(--accent-border);
            border-left: 4px solid {rank_color};
            border-radius: 6px;
            padding: 1rem 1.5rem;
            margin-bottom: 0.8rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.2s ease;
        " onmouseover="this.style.borderColor='var(--accent-primary)'; this.style.transform='translateX(5px)';" 
           onmouseout="this.style.borderColor='var(--accent-border)'; this.style.transform='translateX(0)';">
            <div style="display: flex; align-items: center; gap: 1rem; flex: 1;">
                <div style="
                    font-family: var(--font-pixel);
                    font-size: 1.5rem;
                    color: {rank_color};
                    min-width: 40px;
                    text-align: center;
                ">{rank_icon}</div>
                <div style="
                    font-family: var(--font-base);
                    font-size: 1.1rem;
                    color: var(--text-main);
                    font-weight: 600;
                ">{game_name}</div>
            </div>
            <div style="
                font-family: var(--font-pixel);
                font-size: 1.2rem;
                color: var(--accent-primary);
                background: rgba(78, 201, 176, 0.1);
                padding: 0.5rem 1rem;
                border-radius: 4px;
                min-width: 80px;
                text-align: center;
            ">{count} 曲</div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
    
    # 4位以下を2列で表示
    remaining_games = list(game_counts.items())[3:]
    if remaining_games:
        # 2列に分割
        for i in range(0, len(remaining_games), 2):
            cols = st.columns(2)
            for col_idx, (game_name, count) in enumerate(remaining_games[i:i+2]):
                rank = i + col_idx + 4
                rank_color = "#ce9178"  # レトロオレンジ
                rank_icon = f"{rank}"
                
                with cols[col_idx]:
                    card_html = f"""
                    <div style="
                        background: linear-gradient(135deg, var(--card-bg) 0%, #1a1f35 100%);
                        border: 2px solid var(--accent-border);
                        border-left: 4px solid {rank_color};
                        border-radius: 6px;
                        padding: 0.8rem 1rem;
                        margin-bottom: 0.8rem;
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        transition: all 0.2s ease;
                        height: 100%;
                    " onmouseover="this.style.borderColor='var(--accent-primary)'; this.style.transform='translateX(5px)';" 
                       onmouseout="this.style.borderColor='var(--accent-border)'; this.style.transform='translateX(0)';">
                        <div style="display: flex; align-items: center; gap: 0.8rem; flex: 1;">
                            <div style="
                                font-family: var(--font-pixel);
                                font-size: 1.2rem;
                                color: {rank_color};
                                min-width: 30px;
                                text-align: center;
                            ">{rank_icon}</div>
                            <div style="
                                font-family: var(--font-base);
                                font-size: 0.95rem;
                                color: var(--text-main);
                                font-weight: 600;
                            ">{game_name}</div>
                        </div>
                        <div style="
                            font-family: var(--font-pixel);
                            font-size: 1rem;
                            color: var(--accent-primary);
                            background: rgba(78, 201, 176, 0.1);
                            padding: 0.4rem 0.8rem;
                            border-radius: 4px;
                            min-width: 60px;
                            text-align: center;
                        ">{count} 曲</div>
                    </div>
                    """
                    st.markdown(card_html, unsafe_allow_html=True)

def render_episode_timeline(df):
    """
    配信回ごとの楽曲数推移を折れ線グラフで表示
    """
    import plotly.graph_objects as go
    
    if 'DISC' not in df.columns:
        return
    
    try:
        # DISC列を数値に変換して集計
        df_copy = df.copy()
        df_copy['DISC_num'] = pd.to_numeric(df_copy['DISC'], errors='coerce')
        df_copy = df_copy.dropna(subset=['DISC_num'])
        
        # 配信回ごとの曲数を集計
        episode_counts = df_copy.groupby('DISC_num').size().sort_index()
        
        fig = go.Figure(data=[go.Scatter(
            x=episode_counts.index,
            y=episode_counts.values,
            mode='lines+markers',
            line=dict(color='#4ec9b0', width=3),
            marker=dict(
                color='#ce9178',
                size=8,
                line=dict(color='#2d3748', width=2)
            ),
            fill='tozeroy',
            fillcolor='rgba(78, 201, 176, 0.1)'
        )])
        
        fig.update_layout(
            title=dict(
                text='配信回ごとの楽曲数',
                font=dict(family='DotGothic16, sans-serif', size=20, color='#4ec9b0'),
                x=0.5,
                xanchor='center'
            ),
            xaxis=dict(
                title='配信回',
                titlefont=dict(family='DotGothic16, sans-serif', size=14),
                gridcolor='#2d3748',
                showgrid=True,
                color='#d4d4d8'
            ),
            yaxis=dict(
                title='楽曲数',
                titlefont=dict(family='DotGothic16, sans-serif', size=14),
                gridcolor='#2d3748',
                showgrid=True,
                color='#d4d4d8'
            ),
            paper_bgcolor='#15192b',
            plot_bgcolor='#0b1021',
            font=dict(family='DotGothic16, sans-serif', color='#d4d4d8'),
            height=400,
            margin=dict(t=60, b=60, l=60, r=40)
        )
        
        st.plotly_chart(fig, use_container_width=True, key="episode_timeline_chart")
    except Exception as e:
        st.error(f"Timeline chart error: {e}")

def render_enhanced_dashboard(df):
    """
    統計情報とグラフを含む拡張ダッシュボード
    """
    # 基本統計ボックス
    render_dashboard(df)
    
    st.markdown("---")
    
    # グラフセクション
    st.markdown("### 📊 データ分析")
    
    # 2カラムレイアウト
    col1, col2 = st.columns(2)
    
    with col1:
        render_genre_distribution_chart(df)
    
    with col2:
        render_top_games_chart(df, top_n=10)
    
    # タイムライン（フル幅）
    render_episode_timeline(df)

def render_song_cards_grid(df, key_suffix=""):
    """
    DataFrameを受け取り、カードグリッドレイアウトで描画する
    （ページネーション付き）
    """
    if df.empty:
        st.info("No Data Found.")
        return

    # 1ページあたりの表示数
    ITEMS_PER_PAGE = 8  # 2x2グリッド × 2行 = 8
    
    # ページネーションの状態管理（key_suffixで区別）
    page_key = f'card_page_{key_suffix}'
    if page_key not in st.session_state:
        st.session_state[page_key] = 0
    
    total_pages = math.ceil(len(df) / ITEMS_PER_PAGE)
    
    # ページ範囲の調整
    if st.session_state[page_key] >= total_pages:
        st.session_state[page_key] = 0

    start_idx = st.session_state[page_key] * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    
    current_page_df = df.iloc[start_idx:end_idx]

    # グリッドコンテナ開始
    st.markdown('<div class="song-card-grid">', unsafe_allow_html=True)
    
    for _, row in current_page_df.iterrows():
        # データ取得と安全なデフォルト値
        title = row.get('曲名', 'Unknown Title')
        game = row.get('ゲーム名', 'Unknown Game')
        composer = row.get('発表者', '-')
        genre = row.get('ジャンル', '-')

        card_html = f"""
        <div class="song-card">
            <div class="card-header">
                <h3 class="card-song-title">{title}</h3>
                <div class="card-game-title">{game}</div>
            </div>
            <div class="card-meta">
                <span class="card-tag">{genre}</span>
                <span style="font-size:0.75rem; opacity:0.7;">{composer}</span>
            </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

    # グリッドコンテナ終了
    st.markdown('</div>', unsafe_allow_html=True)

    # ページネーションコントロール
    if total_pages > 1:
        st.markdown("---")
        c1, c2, c3 = st.columns([1, 2, 1])
        with c1:
            if st.session_state[page_key] > 0:
                if st.button("◀ 前へ", key=f"btn_prev_page_{key_suffix}"):
                    st.session_state[page_key] -= 1
                    st.rerun()
        with c2:
            st.markdown(f"<div style='text-align:center; padding-top:10px; font-family:var(--font-pixel);'>ページ {st.session_state[page_key] + 1} / {total_pages}</div>", unsafe_allow_html=True)
        with c3:
            if st.session_state[page_key] < total_pages - 1:
                if st.button("次へ ▶", key=f"btn_next_page_{key_suffix}"):
                    st.session_state[page_key] += 1
                    st.rerun()

def render_active_filters(filters, search_query):
    """
    現在適用されているフィルターをタグ形式で表示
    """
    if not any(filters.values()) and not search_query:
        return
    
    html = '<div style="margin-bottom: 20px;">'
    
    # 検索キーワード
    if search_query:
        html += f'<span class="filter-tag"><span style="margin-right:5px;">🔍</span>"{search_query}"</span>'
    
    # 各フィルターカテゴリー
    for category, values in filters.items():
        if values:
            for val in values:
                html += f'<span class="filter-tag"><span style="margin-right:5px; opacity:0.7;">{category}:</span>{val}</span>'
                
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

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
    current_themes = st.session_state.get('selected_themes', [])
    if not current_themes:
        st.info("表示するテーマを選択してください。")
        return

    target_theme = current_themes[0]
    st.markdown(f"### 🎵 {target_theme}")
    
    with st.container():
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
        
        # ダッシュボード表示（テーマ内統計）
        st.markdown(f"**紹介曲数: {len(theme_df)}曲**")
        
        # グリッド表示に変更
        display_results(theme_df, mode="theme", key=f"theme_{target_theme}")

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
    """
    if not val:
        return False
    parts = [p.strip() for p in str(val).replace('，', ',').replace('/', ',').split(',')]
    return any(p in platform_filters for p in parts)

@st.cache_data(ttl=300, show_spinner=False)
def _apply_filters_impl(df, filters_tuple):
    """
    フィルタ適用の内部実装（キャッシュ用）
    """
    try:
        filters = {
            'テーマ': list(filters_tuple[0]) if filters_tuple[0] else [],
            'ジャンル': list(filters_tuple[1]) if filters_tuple[1] else [],
            'プラットフォーム': list(filters_tuple[2]) if filters_tuple[2] else [],
            '発表者': list(filters_tuple[3]) if filters_tuple[3] else []
        }
    except (IndexError, TypeError) as e:
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
        return df.copy()
    
    return filtered_df

def apply_filters(df, filters):
    """
    データにフィルターを適用
    """
    if df.empty:
        return df.copy()
    
    if not any(filters.values()):
        return df.copy()
    
    try:
        filters_tuple = (
            tuple(sorted(filters.get('テーマ', []))),
            tuple(sorted(filters.get('ジャンル', []))),
            tuple(sorted(filters.get('プラットフォーム', []))),
            tuple(sorted(filters.get('発表者', [])))
        )
        return _apply_filters_impl(df, filters_tuple)
    except Exception:
        return df.copy()

def render_entrance_screen(latest_theme):
    """
    初期表示画面（ダッシュボード含む）
    """
    st.markdown("<div style='text-align:center; margin: 4rem 0;'>", unsafe_allow_html=True)
    st.markdown("<h3>Welcome to the Library</h3>", unsafe_allow_html=True)
    st.markdown("<p style='opacity:0.6; font-family:var(--font-pixel);'>SELECT A KEYWORD OR THEME TO START</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def render_random_card(row, df, key_suffix=""):
    """
    ランダム表示カード（互換性のため残存、CSS変更に伴いスタイル調整）
    """
    pass 

def display_results(df, mode="search", key=None):
    """
    検索結果を表示（グリッド表示のみ）
    """
    if df.empty:
        st.info("該当する楽曲が見つかりませんでした。")
        return

    # ソート機能
    col_label, col_sort = st.columns([0.8, 5])
    with col_label:
        st.markdown('<div style="padding-top: 8px; color: rgba(255, 255, 255, 0.7); font-weight: 600;">並び替え:</div>', unsafe_allow_html=True)
    with col_sort:
        sort_option = st.selectbox(
            "並び順",
            ["デフォルト（紹介順）", "曲名（あいうえお順）", "ゲーム名（あいうえお順）", "配信回（新しい順）", "配信回（古い順）"],
            key=f"sort_{key}",
            label_visibility="collapsed"
        )
    
    # ソート処理
    df_sorted = df.copy()
    if sort_option == "曲名（あいうえお順）":
        df_sorted = df_sorted.sort_values('曲名')
    elif sort_option == "ゲーム名（あいうえお順）":
        df_sorted = df_sorted.sort_values('ゲーム名')
    elif sort_option == "配信回（新しい順）":
        if 'DISC' in df_sorted.columns:
            df_sorted['_disc_num'] = pd.to_numeric(df_sorted['DISC'], errors='coerce')
            df_sorted = df_sorted.sort_values('_disc_num', ascending=False)
            df_sorted = df_sorted.drop(columns=['_disc_num'])
    elif sort_option == "配信回（古い順）":
        if 'DISC' in df_sorted.columns:
            df_sorted['_disc_num'] = pd.to_numeric(df_sorted['DISC'], errors='coerce')
            df_sorted = df_sorted.sort_values('_disc_num', ascending=True)
            df_sorted = df_sorted.drop(columns=['_disc_num'])
    
    # グリッド表示のみ
    gb = GridOptionsBuilder.from_dataframe(df_sorted[['曲名', 'ゲーム名', 'ジャンル', 'プラットフォーム', '発表者', 'テーマ']])
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=20)
    gb.configure_selection('single', use_checkbox=False)
    gb.configure_default_column(resizable=True, filterable=True, sortable=True)
    gridOptions = gb.build()

    AgGrid(
        df_sorted,
        gridOptions=gridOptions,
        fit_columns_on_grid_load=True,
        height=600,
        theme='streamlit',
        key=f"grid_{key}"
    )

