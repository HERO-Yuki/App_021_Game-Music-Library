import pandas as pd
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
import urllib.parse
import re

@st.cache_data(ttl=600)
def load_gsheet_data():
    """
    Google Sheetsからデータを読み込み、アーカイブ対応表と結合する
    """
    try:
        # secretsから認証情報を取得
        creds_info = st.secrets["connections"]["gsheets"]
        spreadsheet_id = st.secrets["spreadsheet"]["id"]
        main_sheet_name = st.secrets["spreadsheet"]["sheet_name"]
        archive_sheet_name = "アーカイブ対応表" # 固定のシート名

        # 認証
        creds = service_account.Credentials.from_service_account_info(creds_info)
        service = build('sheets', 'v4', credentials=creds)

        # 1. メインデータの取得（紹介順）
        main_range = f"{main_sheet_name}!A:M"
        main_result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=main_range).execute()
        main_values = main_result.get('values', [])

        if not main_values:
            return pd.DataFrame()

        df_main = pd.DataFrame(main_values[1:], columns=main_values[0])

        # 2. アーカイブ対応表の取得
        try:
            archive_range = f"{archive_sheet_name}!A:B"
            archive_result = service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id, range=archive_range).execute()
            archive_values = archive_result.get('values', [])
            
            if archive_values:
                df_archive = pd.DataFrame(archive_values[1:], columns=archive_values[0])
                # 結合のために型を合わせる（DISCは文字列として扱うのが安全）
                df_main['DISC'] = df_main['DISC'].astype(str).str.strip()
                df_archive['DISC'] = df_archive['DISC'].astype(str).str.strip()
                
                # 左結合（mainにarchiveのURLを紐付ける）
                df_merged = pd.merge(df_main, df_archive, on='DISC', how='left')
            else:
                df_merged = df_main
                df_merged['アーカイブURL'] = ""
        except Exception:
            # アーカイブ対応表がない、またはエラーの場合は、空の列を作成して続行
            df_merged = df_main
            df_merged['アーカイブURL'] = ""

        # 前処理
        df = preprocess_data(df_merged)

        return df
    except Exception as e:
        import traceback
        st.error(f"データの読み込み中にエラーが発生しました: {e}")
        st.code(traceback.format_exc())
        return pd.DataFrame()

def preprocess_data(df):
    """
    データの前処理と整形
    """
    # 欠損値を空文字に置換
    df = df.fillna("")
    
    # ジャンルの正規化（「01_ロールプレイング」などを「RPG」に統合、頭の番号を削除）
    def normalize_genre(val):
        if not val:
            return ("", 999) # 空データは最後に
        val = str(val).strip()
        
        # 頭の2桁数字をIDとして抽出
        match = re.match(r'^(\d{2})_', val)
        genre_id = int(match.group(1)) if match else 999
        
        # ID+アンダーバーを削除
        genre_name = re.sub(r'^\d{2}_', '', val)
        
        # 統合ルール
        if "ロールプレイング" in genre_name or "RPG" in genre_name:
            genre_name = "RPG"
            genre_id = 1 # RPGは1番に固定
        
        return (genre_name, genre_id)
    
    if 'ジャンル' in df.columns:
        # 名前とIDのタプルを一時的に保存
        genre_tuples = df['ジャンル'].apply(normalize_genre)
        df['ジャンル'] = genre_tuples.apply(lambda x: x[0])
        df['ジャンルID'] = genre_tuples.apply(lambda x: x[1])

    # 発表者のグループ化（指定された5項目に集約）
    def group_presenter(val):
        if not val:
            return ""
        val = str(val).strip()
        
        # 指定された固定メンバー
        main_members = ["夕樹陽彩", "焔幽気", "松足楽瞬"]
        if val in main_members:
            return val
        
        # 「視聴者」を含む場合は「視聴者」
        if "視聴者" in val:
            return "視聴者"
        
        # それ以外（主、ゲストなど）はすべて「ゲスト」に集約
        return "ゲスト"
    
    df['発表者グループ'] = df['発表者'].apply(group_presenter)
    
    # 配信テーマの表示用文字列生成（第XX回 テーマ名）
    def make_display_theme(row):
        # DISC（配信回）を3桁に整形
        try:
            ep_val = int(float(str(row['DISC']).strip()))
            ep = f"{ep_val:03d}"
        except (ValueError, TypeError):
            ep = str(row['DISC']).strip() if 'DISC' in row else "???"
            
        theme = str(row['テーマ']).strip() if 'テーマ' in row else ""
        if ep and theme:
            return f"第{ep}回 {theme}"
        elif ep:
            return f"第{ep}回"
        return theme
    
    df['表示用テーマ'] = df.apply(make_display_theme, axis=1)
    
    # 通算の0埋め処理（最大桁数に合わせて）
    if '通算' in df.columns:
        # 通算列の最大値を取得して桁数を決定
        def get_max_digits(series):
            """通算列の最大桁数を取得"""
            max_val = 0
            for val in series:
                if pd.notna(val) and val != "":
                    try:
                        num_val = int(float(str(val).strip()))
                        max_val = max(max_val, num_val)
                    except (ValueError, TypeError):
                        continue
            return len(str(max_val)) if max_val > 0 else 4  # デフォルト4桁
        
        max_digits = get_max_digits(df['通算'])
        
        def pad_通算(val):
            """通算を0埋めして文字列として返す"""
            if not val or (isinstance(val, str) and val.strip() == ""):
                return ""
            try:
                num_val = int(float(str(val).strip()))
                return f"{num_val:0{max_digits}d}"
            except (ValueError, TypeError):
                return str(val).strip()
        
        df['通算'] = df['通算'].apply(pad_通算)
    
    # 表示用の列選択と型変換
    display_cols = ['通算', 'DISC', 'テーマ', '表示用テーマ', '曲名', 'ゲーム名', 'ジャンル', 'プラットフォーム', '発表者', '発表者グループ', 'アーカイブURL']
    existing_cols = [c for c in display_cols if c in df.columns]
    
    return df[existing_cols]

@st.cache_data(ttl=600)
def get_filter_options(df):
    """
    フィルター用のユニーク値リストを取得
    キャッシュ: 10分間有効（データが変更されない限り、再計算を回避）
    """
    # 配信テーマを数値（DISC）で降順（新しい順）にソートして取得
    themes = []
    if '表示用テーマ' in df.columns and 'DISC' in df.columns:
        temp_df = df[['DISC', '表示用テーマ']].copy()
        def to_numeric(val):
            try:
                return float(str(val).strip())
            except (ValueError, TypeError):
                return -1.0
        
        temp_df['num_ep'] = temp_df['DISC'].apply(to_numeric)
        # 降順（ascending=False）でソート
        themes = temp_df.sort_values('num_ep', ascending=False)['表示用テーマ'].unique().tolist()

    # ジャンルを元のID順に並べるためのロジック
    genre_list = []
    if 'ジャンル' in df.columns and 'ジャンルID' in df.columns:
        # ID順に並べてユニークな名前を取得
        genre_list = df.sort_values('ジャンルID')['ジャンル'].unique().tolist()

    # プラットフォームはカンマ区切りを考慮して展開
    platforms = set()
    if 'プラットフォーム' in df.columns:
        for p_str in df['プラットフォーム'].unique():
            if not p_str:
                continue
            # カンマ、全角カンマ、スラッシュなどで分割
            parts = [p.strip() for p in p_str.replace('，', ',').replace('/', ',').split(',')]
            platforms.update(parts)

    options = {
        'テーマ': themes,
        'ジャンル': genre_list,
        'プラットフォーム': sorted(list(platforms)),
        '発表者': sorted(df['発表者グループ'].unique().tolist()) if '発表者グループ' in df.columns else []
    }
    # 空文字を除去
    for key in options:
        options[key] = [opt for opt in options[key] if opt]
    return options
