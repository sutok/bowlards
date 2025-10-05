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
  CircularProgress
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import VisibilityIcon from '@mui/icons-material/Visibility';
import DeleteIcon from '@mui/icons-material/Delete';
import SportsIcon from '@mui/icons-material/Sports';

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

  // モックデータ（実際の実装ではAPIから取得）
  useEffect(() => {
    const mockGames: GameSummary[] = [
      {
        id: '1',
        gameDate: '2024-01-15T10:30:00Z',
        totalScore: 180,
        strikes: 3,
        spares: 2,
        status: 'completed',
        duration: 45
      },
      {
        id: '2',
        gameDate: '2024-01-14T15:20:00Z',
        totalScore: 165,
        strikes: 2,
        spares: 4,
        status: 'completed',
        duration: 50
      },
      {
        id: '3',
        gameDate: '2024-01-13T09:15:00Z',
        totalScore: 195,
        strikes: 5,
        spares: 1,
        status: 'completed',
        duration: 40
      }
    ];

    setTimeout(() => {
      setGames(mockGames);
      setTotalPages(1);
      setLoading(false);
    }, 1000);
  }, []);

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

  const confirmDelete = () => {
    if (gameToDelete) {
      setGames(games.filter(game => game.id !== gameToDelete));
      setGameToDelete(null);
      setDeleteDialogOpen(false);
    }
  };

  const handlePageChange = (event: React.ChangeEvent<unknown>, page: number) => {
    setCurrentPage(page);
    // 実際の実装ではAPIを呼び出してページデータを取得
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
