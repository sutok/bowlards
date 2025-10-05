#!/usr/bin/env python3
"""
Firebase IDトークン取得スクリプト

Swagger UIでのテスト用にFirebase IDトークンを取得します。

使用方法:
    python scripts/get_firebase_token.py

または環境変数で指定:
    export FIREBASE_API_KEY="your-api-key"
    export TEST_USER_EMAIL="test@example.com"
    export TEST_USER_PASSWORD="password"
    python scripts/get_firebase_token.py
"""

import os
import sys
import json
import requests
from getpass import getpass


def get_firebase_token(api_key: str, email: str, password: str) -> dict:
    """Firebase Authentication REST APIを使用してIDトークンを取得"""
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
    
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        error_data = response.json()
        error_message = error_data.get("error", {}).get("message", "Unknown error")
        raise Exception(f"Firebase API Error: {error_message}")
    except Exception as e:
        raise Exception(f"Request failed: {str(e)}")


def main():
    """メイン処理"""
    print("=" * 80)
    print("Firebase IDトークン取得ツール")
    print("=" * 80)
    print()
    
    # Firebase API Keyを取得
    api_key = os.getenv("FIREBASE_API_KEY") or os.getenv("VITE_FIREBASE_API_KEY")
    
    if not api_key:
        print("❌ Firebase API Keyが見つかりません")
        print()
        print("以下のいずれかの方法でAPI Keyを設定してください:")
        print("1. 環境変数 FIREBASE_API_KEY を設定")
        print("2. .env ファイルに VITE_FIREBASE_API_KEY を設定")
        print()
        api_key = input("Firebase API Keyを入力してください: ").strip()
        
        if not api_key:
            print("❌ API Keyが入力されませんでした")
            sys.exit(1)
    
    # ユーザー認証情報を取得
    email = os.getenv("TEST_USER_EMAIL")
    password = os.getenv("TEST_USER_PASSWORD")
    
    if not email:
        print()
        email = input("メールアドレス: ").strip()
    else:
        print(f"\n📧 メールアドレス: {email}")
    
    if not password:
        password = getpass("🔒 パスワード: ")
    
    if not email or not password:
        print("❌ メールアドレスとパスワードは必須です")
        sys.exit(1)
    
    print()
    print("🔄 Firebase認証中...")
    print()
    
    try:
        # トークンを取得
        result = get_firebase_token(api_key, email, password)
        
        id_token = result.get("idToken")
        refresh_token = result.get("refreshToken")
        expires_in = result.get("expiresIn")
        user_id = result.get("localId")
        user_email = result.get("email")
        
        # 結果を表示
        print("✅ 認証成功！")
        print()
        print("-" * 80)
        print("ユーザー情報:")
        print("-" * 80)
        print(f"User ID: {user_id}")
        print(f"Email: {user_email}")
        print(f"有効期限: {expires_in}秒 (約{int(expires_in)//60}分)")
        print()
        print("-" * 80)
        print("Firebase ID Token (Swagger UIで使用):")
        print("-" * 80)
        print(id_token)
        print("-" * 80)
        print()
        
        # クリップボードにコピーを試みる（オプション）
        try:
            import pyperclip
            pyperclip.copy(id_token)
            print("✅ トークンがクリップボードにコピーされました！")
        except ImportError:
            print("💡 ヒント: pyperclipをインストールすると自動的にクリップボードにコピーされます")
            print("   pip install pyperclip")
        
        print()
        print("-" * 80)
        print("Swagger UIでの使用方法:")
        print("-" * 80)
        print("1. http://localhost:18080/docs にアクセス")
        print("2. 右上の 'Authorize' ボタンをクリック")
        print("3. HTTPBearer の入力欄に上記のトークンを貼り付け")
        print("4. 'Authorize' をクリック")
        print()
        print("⚠️  トークンは約1時間で期限切れになります")
        print("=" * 80)
        
        # 環境変数として使用するための出力
        print()
        print("環境変数として設定する場合:")
        print(f"export FIREBASE_ID_TOKEN='{id_token}'")
        print()
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {str(e)}")
        print()
        print("よくあるエラー:")
        print("- INVALID_EMAIL: メールアドレスの形式が正しくありません")
        print("- INVALID_PASSWORD: パスワードが間違っています")
        print("- EMAIL_NOT_FOUND: ユーザーが見つかりません")
        print("- TOO_MANY_ATTEMPTS_TRY_LATER: ログイン試行回数が多すぎます")
        print()
        sys.exit(1)


if __name__ == "__main__":
    main()

