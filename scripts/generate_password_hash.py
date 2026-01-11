"""
パスワードのハッシュ値を生成するスクリプト

使い方:
    python scripts/generate_password_hash.py <パスワード>

例:
    python scripts/generate_password_hash.py mypassword123

生成されたハッシュ値を.secrets.tomlまたはStreamlit CloudのSecretsに設定してください。
"""
import sys
import hashlib

def hash_password(password):
    """パスワードをハッシュ化"""
    return hashlib.sha256(password.encode()).hexdigest()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用方法: python scripts/generate_password_hash.py <パスワード>")
        sys.exit(1)
    
    password = sys.argv[1]
    hashed = hash_password(password)
    
    print("\n" + "="*60)
    print("パスワードハッシュ値（以下をsecrets.tomlに設定してください）")
    print("="*60)
    print(f"\n[app]")
    print(f'password_hash = "{hashed}"\n')
    print("="*60)
    print("\n⚠️  注意: このパスワードを忘れないようにしてください！")
    print("="*60 + "\n")

