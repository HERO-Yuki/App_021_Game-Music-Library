"""
シンプルなパスワード認証機能
"""
import streamlit as st
import hashlib

def check_password(password_hash):
    """
    パスワードをチェックする
    
    Args:
        password_hash: secrets.tomlに設定されたパスワードのハッシュ値
    
    Returns:
        認証成功時True、失敗時False
    """
    def password_entered():
        """パスワード入力時の処理"""
        # 入力されたパスワードのハッシュを計算
        input_hash = hashlib.sha256(st.session_state["password"].encode()).hexdigest()
        
        # ハッシュ値を比較
        if input_hash == password_hash:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # パスワードをセッション状態から削除
        else:
            st.session_state["password_correct"] = False

    # 認証状態のチェック
    is_authenticated = st.session_state.get("password_correct", False)
    
    if not is_authenticated:
        # パスワード入力画面を表示（認証失敗時のエラーメッセージも表示）
        _render_password_screen(password_entered)
        
        # エラーメッセージの表示（認証失敗時のみ）
        if "password_correct" in st.session_state and not st.session_state["password_correct"]:
            st.error("❌ パスワードが正しくありません")
        
        return False
    
    else:
        # パスワードが正しい場合
        return True


def _render_password_screen(password_entered_callback):
    """
    パスワード入力画面を表示する内部関数
    
    Args:
        password_entered_callback: パスワード入力時のコールバック関数
    """
    st.markdown("""
        <style>
        .password-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 60vh;
            text-align: center;
        }
        .password-title {
            font-size: 2.5rem;
            color: #00dbde;
            margin-bottom: 1rem;
            font-weight: 900;
        }
        .password-subtitle {
            color: #b0b0b0;
            font-size: 1.1rem;
            margin-bottom: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="password-container">', unsafe_allow_html=True)
    st.markdown('<div class="password-title">🔐 パスワードが必要です</div>', unsafe_allow_html=True)
    st.markdown('<div class="password-subtitle">語る会Libraryにアクセスするにはパスワードを入力してください</div>', unsafe_allow_html=True)
    
    st.text_input(
        "パスワード",
        type="password",
        on_change=password_entered_callback,
        key="password",
        label_visibility="visible"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)


def hash_password(password):
    """
    パスワードをハッシュ化する（設定用のユーティリティ関数）
    
    Args:
        password: 平文のパスワード
    
    Returns:
        ハッシュ化されたパスワード（16進数文字列）
    """
    return hashlib.sha256(password.encode()).hexdigest()

