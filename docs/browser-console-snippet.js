/**
 * Firebase IDトークン取得用ブラウザコンソールスニペット
 * 
 * 使用方法:
 * 1. フロントエンド (http://localhost:13000) にアクセスしてログイン
 * 2. ブラウザのDevToolsを開く (F12 または Cmd+Option+I)
 * 3. Consoleタブを選択
 * 4. このスニペット全体をコピー＆ペーストして Enter を押す
 */

(async function getFirebaseToken() {
  console.log('🔍 Firebase ID Token 取得中...\n');
  
  try {
    // Firebase Authインスタンスを取得
    const auth = window.firebase?.auth?.() || window.auth;
    
    if (!auth) {
      console.error('❌ Firebase Auth が見つかりません');
      console.log('💡 ログインしていることを確認してください');
      return;
    }
    
    // 現在のユーザーを取得
    const user = auth.currentUser;
    
    if (!user) {
      console.error('❌ ログインしていません');
      console.log('💡 まずログインしてください');
      return;
    }
    
    console.log('✅ ユーザー情報:');
    console.log(`   UID: ${user.uid}`);
    console.log(`   Email: ${user.email}`);
    console.log(`   Display Name: ${user.displayName || '(未設定)'}\n`);
    
    // IDトークンを取得
    const token = await user.getIdToken();
    
    console.log('=' .repeat(80));
    console.log('Firebase ID Token (Swagger UIで使用):');
    console.log('=' .repeat(80));
    console.log(token);
    console.log('=' .repeat(80));
    console.log('\n');
    
    // クリップボードにコピー
    try {
      await navigator.clipboard.writeText(token);
      console.log('✅ トークンがクリップボードにコピーされました！\n');
    } catch (err) {
      console.warn('⚠️  クリップボードへのコピーに失敗しました');
      console.log('💡 上記のトークンを手動でコピーしてください\n');
    }
    
    // トークンの詳細を表示（デコード）
    try {
      const parts = token.split('.');
      if (parts.length === 3) {
        const payload = JSON.parse(atob(parts[1]));
        const expirationDate = new Date(payload.exp * 1000);
        const issuedDate = new Date(payload.iat * 1000);
        
        console.log('📋 トークン情報:');
        console.log(`   発行日時: ${issuedDate.toLocaleString('ja-JP')}`);
        console.log(`   有効期限: ${expirationDate.toLocaleString('ja-JP')}`);
        console.log(`   残り時間: 約${Math.floor((expirationDate - Date.now()) / 1000 / 60)}分\n`);
      }
    } catch (err) {
      // デコードに失敗しても問題なし
    }
    
    console.log('-'.repeat(80));
    console.log('Swagger UIでの使用方法:');
    console.log('-'.repeat(80));
    console.log('1. http://localhost:18080/docs にアクセス');
    console.log('2. 右上の [Authorize] ボタンをクリック');
    console.log('3. HTTPBearer の入力欄にトークンを貼り付け');
    console.log('4. [Authorize] をクリック');
    console.log('5. APIエンドポイントをテスト！\n');
    
    console.log('⚠️  トークンは約1時間で期限切れになります');
    console.log('💡 期限切れになったら、このスニペットを再度実行してください\n');
    
    // グローバル変数として保存（デバッグ用）
    window.FIREBASE_TOKEN = token;
    console.log('💾 トークンは window.FIREBASE_TOKEN にも保存されました');
    
  } catch (error) {
    console.error('❌ エラーが発生しました:', error);
    console.log('\n💡 トラブルシューティング:');
    console.log('   - ログインしていることを確認');
    console.log('   - ページをリロードして再試行');
    console.log('   - フロントエンドが正しく動作していることを確認');
  }
})();

