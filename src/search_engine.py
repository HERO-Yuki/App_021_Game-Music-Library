import pandas as pd
import streamlit as st
from thefuzz import fuzz

@st.cache_data(ttl=300, show_spinner=False)
def fuzzy_search(df, keyword, threshold=60):
    """
    キーワードに基づいて曲名、ゲーム名、シリーズなどを対象にあいまい検索を行う
    （パフォーマンス最適化: 同じキーワードとDataFrameの組み合わせはキャッシュを使用）
    
    Args:
        df: 検索対象のDataFrame
        keyword: 検索キーワード（文字列）
        threshold: 類似度のしきい値（0-100、デフォルト: 60）
    
    Returns:
        検索結果のDataFrame（search_score列は削除済み）
    """
    if df.empty:
        return df
    
    if not keyword or not keyword.strip():
        return df
    
    try:
        keyword_lower = keyword.lower().strip()
        
        # 検索対象のカラム
        search_targets = ['曲名', 'ゲーム名', 'シリーズ']
        # 実際に存在する列のみを対象にする
        available_targets = [c for c in search_targets if c in df.columns]
        
        if not available_targets:
            # 代替として最低限の列を対象にする
            available_targets = [c for c in ['曲名', 'ゲーム名'] if c in df.columns]
        
        if not available_targets:
            # 検索対象列が存在しない場合は元のDataFrameを返す
            return df

        def calculate_max_score(row):
            """各行の最大スコアを計算"""
            scores = []
            for col in available_targets:
                try:
                    val = str(row[col]) if pd.notna(row[col]) else ''
                    if not val:
                        continue
                    # 部分一致スコアを計算
                    score = fuzz.partial_ratio(keyword_lower, val.lower())
                    scores.append(score)
                except Exception:
                    continue
            return max(scores) if scores else 0

        # スコア計算
        df_with_scores = df.copy()
        df_with_scores['search_score'] = df_with_scores.apply(calculate_max_score, axis=1)
        
        # スコアでフィルタリングして降順にソート
        results = df_with_scores[df_with_scores['search_score'] >= threshold]
        results = results.sort_values(by='search_score', ascending=False)
        
        # search_score列を削除して返す
        if 'search_score' in results.columns:
            results = results.drop(columns=['search_score'])
        
        return results
    except Exception:
        # エラーが発生した場合、元のDataFrameを返す
        return df
