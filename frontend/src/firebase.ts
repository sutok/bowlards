import { initializeApp } from 'firebase/app';
import { getAuth, connectAuthEmulator } from 'firebase/auth';
import { getFirestore, connectFirestoreEmulator } from 'firebase/firestore';

// 環境変数から設定を読み込み
const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY || "AIzaSyBtRfo39zhagvkyrNgevvAdxL3kcTNtPvA",
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN || "bowlards-dev.firebaseapp.com",
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID || "bowlards-dev",
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET || "bowlards-dev.firebasestorage.app",
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID || "710931509835",
  appId: import.meta.env.VITE_FIREBASE_APP_ID || "1:710931509835:web:c049a1fdbc1e33404ad3ce"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase services
export const auth = getAuth(app);
export const db = getFirestore(app);

// Firebase Emulator接続（開発環境のみ）
const useEmulator = import.meta.env.VITE_USE_FIREBASE_EMULATOR === 'true';

if (useEmulator) {
  const firestoreHost = import.meta.env.VITE_FIRESTORE_EMULATOR_HOST || 'localhost';
  const firestorePort = parseInt(import.meta.env.VITE_FIRESTORE_EMULATOR_PORT || '8080');
  const authHost = import.meta.env.VITE_AUTH_EMULATOR_HOST || 'localhost';
  const authPort = parseInt(import.meta.env.VITE_AUTH_EMULATOR_PORT || '9099');

  connectFirestoreEmulator(db, firestoreHost, firestorePort);
  connectAuthEmulator(auth, `http://${authHost}:${authPort}`, { disableWarnings: true });

  console.log('🔧 Firebase Emulator Mode');
  console.log(`  Firestore: ${firestoreHost}:${firestorePort}`);
  console.log(`  Auth: ${authHost}:${authPort}`);
  console.log(`  Project: ${firebaseConfig.projectId}`);
} else {
  console.log('✅ Firebase Production Mode');
  console.log(`  Project: ${firebaseConfig.projectId}`);
  console.log(`  Auth Domain: ${firebaseConfig.authDomain}`);
}

export default app;
