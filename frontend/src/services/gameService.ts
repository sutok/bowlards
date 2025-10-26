import { apiClient } from './api';

/**
 * フレームデータの型定義
 */
export interface Frame {
  frameNumber: number;
  firstRoll: number | null;
  secondRoll: number | null;
  thirdRoll: number | null;
  frameScore: number | null;
  isStrike: boolean;
  isSpare: boolean;
  isCompleted: boolean;
}

/**
 * ゲームデータの型定義
 */
export interface Game {
  id: string;
  userId?: string;  // オプショナル: バックエンドで認証トークンから自動設定
  gameDate: string;
  totalScore: number;
  frames: Frame[];
  status: 'in_progress' | 'completed';
}

/**
 * ゲーム作成リクエストの型定義
 */
export interface CreateGameRequest {
  gameDate: string;
  frames: Frame[];
  totalScore: number;
  status: 'in_progress' | 'completed';
}

/**
 * APIレスポンスの型定義
 */
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
  };
  meta?: {
    total?: number;
    limit?: number;
    offset?: number;
  };
}

/**
 * ゲームサービス
 */
export const gameService = {
  /**
   * ゲームを作成・保存
   * 
   * userIdは認証トークンから自動的に取得されるため、送信する必要はありません
   */
  async saveGame(game: Game): Promise<Game> {
    try {
      const requestData: CreateGameRequest = {
        gameDate: game.gameDate,
        frames: game.frames,
        totalScore: game.totalScore,
        status: game.status,
      };

      console.log('📊 送信データ詳細:', {
        gameDate: requestData.gameDate,
        totalScore: requestData.totalScore,
        status: requestData.status,
        framesCount: requestData.frames.length,
        frames: requestData.frames.map(f => ({
          frameNumber: f.frameNumber,
          rolls: [f.firstRoll, f.secondRoll, f.thirdRoll].filter(r => r !== null),
          frameScore: f.frameScore,
          isStrike: f.isStrike,
          isSpare: f.isSpare
        }))
      });

      const response = await apiClient.post<ApiResponse<Game>>('/games/', requestData);

      if (response.data.success && response.data.data) {
        console.log('✅ バックエンドレスポンス:', response.data.data);
        return response.data.data;
      } else {
        throw new Error(response.data.error?.message || 'Failed to save game');
      }
    } catch (error: any) {
      console.error('❌ Error saving game:', error);
      console.error('❌ Response data:', error.response?.data);
      throw new Error(error.response?.data?.error?.message || 'ゲームの保存に失敗しました');
    }
  },

  /**
   * ゲームを取得
   */
  async getGame(gameId: string): Promise<Game> {
    try {
      const response = await apiClient.get<ApiResponse<Game>>(`/games/${gameId}`);

      if (response.data.success && response.data.data) {
        return response.data.data;
      } else {
        throw new Error(response.data.error?.message || 'Failed to get game');
      }
    } catch (error: any) {
      console.error('Error getting game:', error);
      throw new Error(error.response?.data?.error?.message || 'ゲームの取得に失敗しました');
    }
  },

  /**
   * ゲーム履歴を取得
   */
  async getGameHistory(limit: number = 10, offset: number = 0): Promise<{ games: Game[]; total: number }> {
    try {
      const response = await apiClient.get<ApiResponse<Game[]>>('/games/history', {
        params: { limit, offset },
      });

      if (response.data.success && response.data.data) {
        return {
          games: response.data.data,
          total: response.data.meta?.total || 0,
        };
      } else {
        throw new Error(response.data.error?.message || 'Failed to get game history');
      }
    } catch (error: any) {
      console.error('Error getting game history:', error);
      throw new Error(error.response?.data?.error?.message || 'ゲーム履歴の取得に失敗しました');
    }
  },

  /**
   * ゲームを削除
   */
  async deleteGame(gameId: string): Promise<void> {
    try {
      const response = await apiClient.delete<ApiResponse<any>>(`/games/${gameId}`);

      if (!response.data.success) {
        throw new Error(response.data.error?.message || 'Failed to delete game');
      }
    } catch (error: any) {
      console.error('Error deleting game:', error);
      throw new Error(error.response?.data?.error?.message || 'ゲームの削除に失敗しました');
    }
  },
};

export default gameService;

