import axios, { AxiosInstance, AxiosError } from 'axios';
import { auth } from '../firebase';

// APIベースURL
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:18080/api/v1';

// デバッグ情報をログ出力
console.log('🔧 API Configuration:');
console.log('  VITE_API_BASE_URL:', import.meta.env.VITE_API_BASE_URL);
console.log('  API_BASE_URL:', API_BASE_URL);
console.log('  Mode:', import.meta.env.MODE);

/**
 * APIクライアントの作成
 */
const createApiClient = (): AxiosInstance => {
  const client = axios.create({
    baseURL: API_BASE_URL,
    headers: {
      'Content-Type': 'application/json',
    },
    timeout: 10000, // 10秒のタイムアウト
  });

  // リクエストインターセプター（認証トークンの追加）
  client.interceptors.request.use(
    async (config) => {
      const user = auth.currentUser;
      if (user) {
        const token = await user.getIdToken();
        config.headers.Authorization = `Bearer ${token}`;
      }
      
      // デバッグ情報
      console.log('📤 API Request:', {
        method: config.method?.toUpperCase(),
        url: config.url,
        baseURL: config.baseURL,
        fullURL: `${config.baseURL}${config.url}`,
        hasAuth: !!config.headers.Authorization
      });
      
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );

  // レスポンスインターセプター（エラーハンドリング）
  client.interceptors.response.use(
    (response) => response,
    (error: AxiosError) => {
      if (error.response) {
        // サーバーからのエラーレスポンス
        console.error('API Error:', error.response.data);
      } else if (error.request) {
        // リクエストは送信されたがレスポンスがない
        console.error('Network Error:', error.message);
      } else {
        // その他のエラー
        console.error('Error:', error.message);
      }
      return Promise.reject(error);
    }
  );

  return client;
};

// APIクライアントのインスタンス
export const apiClient = createApiClient();

export default apiClient;

