import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  Typography,
  Card,
  CardContent,
  Grid,
  Container,
  Paper,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Pagination,
  CircularProgress,
  Alert
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import VisibilityIcon from '@mui/icons-material/Visibility';
import DeleteIcon from '@mui/icons-material/Delete';
import SportsIcon from '@mui/icons-material/Sports';
import { gameService } from '../services/gameService';
import { auth } from '../firebase/config';

interface GameSummary {
  id: string;
  gameDate: string;
  totalScore: number;
  strikes: number;
  spares: number;
  status: 'completed' | 'in_progress';
  duration?: number;
}

interface GameHistoryProps {
  onViewGameDetail: (gameId: string) => void;
}

export default function GameHistory({ onViewGameDetail }: GameHistoryProps) {
  const navigate = useNavigate();
  const [games, setGames] = useState<GameSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [gameToDelete, setGameToDelete] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const itemsPerPage = 10;

  // ゲーム履歴を取得
  useEffect(() => {
    fetchGames();
  }, [currentPage]);

  const fetchGames = async () => {
    setLoading(true);
    setError(null);

    try {
      const user = auth.currentUser;
      if (!user) {
        setError('ログインが必要です');
        setLoading(false);
        return;
      }

      const offset = (currentPage - 1) * itemsPerPage;
      const result = await gameService.getGameHistory(itemsPerPage, offset);

      console.log('📊 取得したゲーム履歴:', result);

      // バックエンドから取得したデータをGameSummary形式に変換
      const gameSummaries: GameSummary[] = result.games.map(game => ({
        id: game.id,
        gameDate: game.gameDate,
        totalScore: game.totalScore,
        strikes: game.frames?.filter(f => f.isStrike).length || 0,
        spares: game.frames?.filter(f => f.isSpare).length || 0,
        status: game.status as 'completed' | 'in_progress',
        duration: undefined
      }));

      setGames(gameSummaries);
      setTotalPages(Math.ceil(result.total / itemsPerPage));
      setLoading(false);
    } catch (error: any) {
      console.error('❌ ゲーム履歴取得エラー:', error);
      setError(error.message || 'ゲーム履歴の取得に失敗しました');
      setGames([]);
      setLoading(false);
    }
  };

  const formatDate = (dateString: string): string => {
    const date = new Date(dateString);
    return date.toLocaleDateString('ja-JP', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const handleDeleteGame = (gameId: string) => {
    setGameToDelete(gameId);
    setDeleteDialogOpen(true);
  };

  const confirmDelete = async () => {
    if (!gameToDelete) return;

    try {
      await gameService.deleteGame(gameToDelete);
      console.log('✅ ゲームを削除しました:', gameToDelete);
      
      // ゲーム一覧を更新
      await fetchGames();
      
      setGameToDelete(null);
      setDeleteDialogOpen(false);
    } catch (error: any) {
      console.error('❌ ゲーム削除エラー:', error);
      setError(error.message || 'ゲームの削除に失敗しました');
      setDeleteDialogOpen(false);
    }
  };

  const handlePageChange = (event: React.ChangeEvent<unknown>, page: number) => {
    setCurrentPage(page);
  };

  if (loading) {
    return (
      <Container maxWidth="lg">
        <Box sx={{ my: 4, textAlign: 'center' }}>
          <CircularProgress />
          <Typography variant="body1" sx={{ mt: 2 }}>
            読み込み中...
          </Typography>
        </Box>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Button
          startIcon={<ArrowBackIcon />}
          onClick={() => navigate('/')}
          sx={{ mb: 3 }}
        >
          ダッシュボードに戻る
        </Button>

        <Typography variant="h4" gutterBottom>
          ゲーム履歴
        </Typography>

        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}

        {games.length === 0 ? (
          <Paper sx={{ p: 4, textAlign: 'center' }}>
            <SportsIcon sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
            <Typography variant="h6" gutterBottom>
              ゲーム履歴がありません
            </Typography>
            <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
              新しいゲームを開始して記録を残しましょう
            </Typography>
            <Button
              variant="contained"
              startIcon={<SportsIcon />}
              onClick={() => navigate('/game')}
            >
              新しいゲームを開始
            </Button>
          </Paper>
        ) : (
          <>
            {/* 統計情報 */}
            <Grid container spacing={3} sx={{ mb: 4 }}>
              <Grid item xs={12} sm={4}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      総ゲーム数
                    </Typography>
                    <Typography variant="h4" color="primary">
                      {games.length}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} sm={4}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      平均スコア
                    </Typography>
                    <Typography variant="h4" color="secondary">
                      {Math.round(games.reduce((sum, game) => sum + game.totalScore, 0) / games.length)}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} sm={4}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      最高スコア
                    </Typography>
                    <Typography variant="h4" color="success.main">
                      {Math.max(...games.map(game => game.totalScore))}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>

            {/* ゲーム一覧テーブル */}
            <TableContainer component={Paper}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>日時</TableCell>
                    <TableCell align="center">合計スコア</TableCell>
                    <TableCell align="center">ストライク</TableCell>
                    <TableCell align="center">スペア</TableCell>
                    <TableCell align="center">ステータス</TableCell>
                    <TableCell align="center">操作</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {games.map((game) => (
                    <TableRow key={game.id}>
                      <TableCell>
                        {formatDate(game.gameDate)}
                      </TableCell>
                      <TableCell align="center">
                        <Typography variant="h6" color="primary">
                          {game.totalScore}
                        </Typography>
                      </TableCell>
                      <TableCell align="center">
                        <Chip 
                          label={game.strikes} 
                          color="primary" 
                          variant="outlined" 
                          size="small"
                        />
                      </TableCell>
                      <TableCell align="center">
                        <Chip 
                          label={game.spares} 
                          color="secondary" 
                          variant="outlined" 
                          size="small"
                        />
                      </TableCell>
                      <TableCell align="center">
                        <Chip
                          label={game.status === 'completed' ? '完了' : '進行中'}
                          color={game.status === 'completed' ? 'success' : 'warning'}
                          size="small"
                        />
                      </TableCell>
                      <TableCell align="center">
                        <IconButton
                          onClick={() => onViewGameDetail(game.id)}
                          color="primary"
                          size="small"
                        >
                          <VisibilityIcon />
                        </IconButton>
                        <IconButton
                          onClick={() => handleDeleteGame(game.id)}
                          color="error"
                          size="small"
                        >
                          <DeleteIcon />
                        </IconButton>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>

            {/* ページネーション */}
            {totalPages > 1 && (
              <Box sx={{ display: 'flex', justifyContent: 'center', mt: 3 }}>
                <Pagination
                  count={totalPages}
                  page={currentPage}
                  onChange={handlePageChange}
                  color="primary"
                />
              </Box>
            )}
          </>
        )}

        {/* 削除確認ダイアログ */}
        <Dialog open={deleteDialogOpen} onClose={() => setDeleteDialogOpen(false)}>
          <DialogTitle>ゲームを削除</DialogTitle>
          <DialogContent>
            <Typography>
              このゲームを削除してもよろしいですか？この操作は取り消せません。
            </Typography>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setDeleteDialogOpen(false)}>
              キャンセル
            </Button>
            <Button onClick={confirmDelete} color="error" variant="contained">
              削除
            </Button>
          </DialogActions>
        </Dialog>
      </Box>
    </Container>
  );
}
