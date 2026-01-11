import json
from pathlib import Path

def create_secrets_from_json():
    """
    JSONキーファイルからsecrets.tomlを生成する
    
    注意: このスクリプトはローカル開発環境でのみ使用してください。
    JSONキーファイルのパスとスプレッドシートIDを環境に合わせて変更してください。
    """
    # TODO: 環境に合わせてパスを変更してください
    json_path = Path("path/to/your/service-account-key.json")
    secrets_dest = Path(".streamlit/secrets.toml")
    # TODO: 使用するスプレッドシートIDに変更してください
    spreadsheet_id = "YOUR_SPREADSHEET_ID"
    
    if not json_path.exists():
        print(f"Error: {json_path} not found")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        key_data = json.load(f)

    # secrets.toml の内容を生成
    # private_key は改行を含む形式で作成
    secrets_content = f"""[connections.gsheets]
type = "{key_data['type']}"
project_id = "{key_data['project_id']}"
private_key_id = "{key_data['private_key_id']}"
private_key = \"\"\"{key_data['private_key']}\"\"\"
client_email = "{key_data['client_email']}"
client_id = "{key_data['client_id']}"
auth_uri = "{key_data['auth_uri']}"
token_uri = "{key_data['token_uri']}"
auth_provider_x509_cert_url = "{key_data['auth_provider_x509_cert_url']}"
client_x509_cert_url = "{key_data['client_x509_cert_url']}"

[spreadsheet]
id = "{spreadsheet_id}"
sheet_name = "紹介順"
"""
    
    secrets_dest.parent.mkdir(exist_ok=True)
    with open(secrets_dest, "w", encoding="utf-8") as f:
        f.write(secrets_content)
    
    print(f"Successfully created: {secrets_dest}")

if __name__ == "__main__":
    create_secrets_from_json()
