import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';
import { getFirestore } from 'firebase/firestore';

const firebaseConfig = {
  apiKey: "AIzaSyBtRfo39zhagvkyrNgevvAdxL3kcTNtPvA",
  authDomain: "bowlards-dev.firebaseapp.com",
  projectId: "bowlards-dev",
  storageBucket: "bowlards-dev.firebasestorage.app",
  messagingSenderId: "710931509835",
  appId: "1:710931509835:web:c049a1fdbc1e33404ad3ce"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase services
export const auth = getAuth(app);
export const db = getFirestore(app);

export default app;
