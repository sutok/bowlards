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
  Divider
} from '@mui/material';
import { useNavigate, useParams } from 'react-router-dom';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import DeleteIcon from '@mui/icons-material/Delete';
import SportsIcon from '@mui/icons-material/Sports';
import EmojiEventsIcon from '@mui/icons-material/EmojiEvents';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';

interface Frame {
  frameNumber: number;
  firstRoll: number | null;
  secondRoll: number | null;
  thirdRoll: number | null;
  frameScore: number | null;
  isStrike: boolean;
  isSpare: boolean;
  isCompleted: boolean;
}

interface GameDetail {
  id: string;
  userId: string;
  gameDate: string;
  totalScore: number;
  frames: Frame[];
  status: 'completed' | 'in_progress';
  strikes: number;
  spares: number;
  duration?: number;
}

export default function GameDetail() {
  const navigate = useNavigate();
  const { gameId } = useParams<{ gameId: string }>();
  const [game, setGame] = useState<GameDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);

  // モックデータ（実際の実装ではAPIから取得）
  useEffect(() => {
    const mockGame: GameDetail = {
      id: gameId || '1',
      userId: 'user1',
      gameDate: '2024-01-15T10:30:00Z',
      totalScore: 180,
      frames: [
        {
          frameNumber: 1,
          firstRoll: 10,
          secondRoll: null,
          thirdRoll: null,
          frameScore: 19,
          isStrike: true,
          isSpare: false,
          isCompleted: true,
        },
        {
          frameNumber: 2,
          firstRoll: 7,
          secondRoll: 2,
          thirdRoll: null,
          frameScore: 28,
          isStrike: false,
          isSpare: false,
          isCompleted: true,
        },
        {
          frameNumber: 3,
          firstRoll: 8,
          secondRoll: 2,
          thirdRoll: null,
          frameScore: 38,
          isStrike: false,
          isSpare: true,
          isCompleted: true,
        },
        {
          frameNumber: 4,
          firstRoll: 10,
          secondRoll: null,
          thirdRoll: null,
          frameScore: 58,
          isStrike: true,
          isSpare: false,
          isCompleted: true,
        },
        {
          frameNumber: 5,
          firstRoll: 6,
          secondRoll: 3,
          thirdRoll: null,
          frameScore: 67,
          isStrike: false,
          isSpare: false,
          isCompleted: true,
        },
        {
          frameNumber: 6,
          firstRoll: 9,
          secondRoll: 1,
          thirdRoll: null,
          frameScore: 77,
          isStrike: false,
          isSpare: true,
          isCompleted: true,
        },
        {
          frameNumber: 7,
          firstRoll: 10,
          secondRoll: null,
          thirdRoll: null,
          frameScore: 97,
          isStrike: true,
          isSpare: false,
          isCompleted: true,
        },
        {
          frameNumber: 8,
          firstRoll: 4,
          secondRoll: 4,
          thirdRoll: null,
          frameScore: 105,
          isStrike: false,
          isSpare: false,
          isCompleted: true,
        },
        {
          frameNumber: 9,
          firstRoll: 7,
          secondRoll: 2,
          thirdRoll: null,
          frameScore: 114,
          isStrike: false,
          isSpare: false,
          isCompleted: true,
        },
        {
          frameNumber: 10,
          firstRoll: 8,
          secondRoll: 2,
          thirdRoll: 6,
          frameScore: 180,
          isStrike: false,
          isSpare: true,
          isCompleted: true,
        },
      ],
      status: 'completed',
      strikes: 3,
      spares: 3,
      duration: 45
    };

    setTimeout(() => {
      setGame(mockGame);
      setLoading(false);
    }, 1000);
  }, [gameId]);

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

  const formatFrameDisplay = (frame: Frame): string => {
    if (frame.isStrike && frame.frameNumber < 10) {
      return 'X';
    } else if (frame.isSpare) {
      return `${frame.firstRoll}/`;
    } else {
      return `${frame.firstRoll || 0}${frame.secondRoll !== null ? `/${frame.secondRoll}` : ''}`;
    }
  };

  const handleDelete = () => {
    setDeleteDialogOpen(true);
  };

  const confirmDelete = () => {
    // 実際の実装ではAPIを呼び出して削除
    navigate('/history');
  };

  if (loading) {
    return (
      <Container maxWidth="lg">
        <Box sx={{ my: 4, textAlign: 'center' }}>
          <Typography variant="body1">
            読み込み中...
          </Typography>
        </Box>
      </Container>
    );
  }

  if (!game) {
    return (
      <Container maxWidth="lg">
        <Box sx={{ my: 4, textAlign: 'center' }}>
          <Typography variant="h6">
            ゲームが見つかりません
          </Typography>
          <Button onClick={() => navigate('/history')} sx={{ mt: 2 }}>
            履歴に戻る
          </Button>
        </Box>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Button
          startIcon={<ArrowBackIcon />}
          onClick={() => navigate('/history')}
          sx={{ mb: 3 }}
        >
          履歴に戻る
        </Button>

        {/* ゲーム情報ヘッダー */}
        <Paper sx={{ p: 3, mb: 3 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="h4">
              ゲーム詳細
            </Typography>
            <IconButton
              onClick={handleDelete}
              color="error"
            >
              <DeleteIcon />
            </IconButton>
          </Box>
          
          <Grid container spacing={3}>
            <Grid item xs={12} sm={6} md={3}>
              <Typography variant="body2" color="text.secondary">
                日時
              </Typography>
              <Typography variant="h6">
                {formatDate(game.gameDate)}
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Typography variant="body2" color="text.secondary">
                合計スコア
              </Typography>
              <Typography variant="h4" color="primary">
                {game.totalScore}
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Typography variant="body2" color="text.secondary">
                ストライク
              </Typography>
              <Typography variant="h6" color="primary">
                {game.strikes}回
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Typography variant="body2" color="text.secondary">
                スペア
              </Typography>
              <Typography variant="h6" color="secondary">
                {game.spares}回
              </Typography>
            </Grid>
          </Grid>
        </Paper>

        {/* スコアボード */}
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            スコアボード
          </Typography>
          
          <Grid container spacing={1}>
            {game.frames.map((frame) => (
              <Grid item xs={1.2} key={frame.frameNumber}>
                <Card sx={{ p: 1, textAlign: 'center' }}>
                  <Typography variant="caption" color="text.secondary">
                    {frame.frameNumber}
                  </Typography>
                  
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5, minHeight: 20 }}>
                    <Typography variant="body2" sx={{ fontSize: '0.7rem' }}>
                      {frame.firstRoll !== null ? frame.firstRoll : ''}
                    </Typography>
                    <Typography variant="body2" sx={{ fontSize: '0.7rem' }}>
                      {frame.secondRoll !== null ? frame.secondRoll : ''}
                    </Typography>
                    {frame.frameNumber === 10 && frame.thirdRoll !== null && (
                      <Typography variant="body2" sx={{ fontSize: '0.7rem' }}>
                        {frame.thirdRoll}
                      </Typography>
                    )}
                  </Box>
                  
                  <Typography variant="body2" fontWeight="bold">
                    {frame.frameScore !== null ? frame.frameScore : ''}
                  </Typography>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Paper>

        {/* 詳細統計 */}
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  フレーム別スコア
                </Typography>
                <TableContainer>
                  <Table size="small">
                    <TableHead>
                      <TableRow>
                        <TableCell>フレーム</TableCell>
                        <TableCell align="center">1投目</TableCell>
                        <TableCell align="center">2投目</TableCell>
                        <TableCell align="center">3投目</TableCell>
                        <TableCell align="center">スコア</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {game.frames.map((frame) => (
                        <TableRow key={frame.frameNumber}>
                          <TableCell>
                            {frame.frameNumber}
                          </TableCell>
                          <TableCell align="center">
                            {frame.firstRoll !== null ? frame.firstRoll : '-'}
                          </TableCell>
                          <TableCell align="center">
                            {frame.secondRoll !== null ? frame.secondRoll : '-'}
                          </TableCell>
                          <TableCell align="center">
                            {frame.thirdRoll !== null ? frame.thirdRoll : '-'}
                          </TableCell>
                          <TableCell align="center">
                            <Typography variant="body2" fontWeight="bold">
                              {frame.frameScore !== null ? frame.frameScore : '-'}
                            </Typography>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  ゲーム統計
                </Typography>
                
                <Box sx={{ mb: 2 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                    <Typography variant="body2">ストライク率</Typography>
                    <Typography variant="body2" fontWeight="bold">
                      {Math.round((game.strikes / 10) * 100)}%
                    </Typography>
                  </Box>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                    <Typography variant="body2">スペア率</Typography>
                    <Typography variant="body2" fontWeight="bold">
                      {Math.round((game.spares / 10) * 100)}%
                    </Typography>
                  </Box>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                    <Typography variant="body2">平均フレームスコア</Typography>
                    <Typography variant="body2" fontWeight="bold">
                      {Math.round(game.totalScore / 10)}
                    </Typography>
                  </Box>
                  {game.duration && (
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                      <Typography variant="body2">ゲーム時間</Typography>
                      <Typography variant="body2" fontWeight="bold">
                        {game.duration}分
                      </Typography>
                    </Box>
                  )}
                </Box>

                <Divider sx={{ my: 2 }} />

                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <EmojiEventsIcon color="primary" sx={{ mr: 1 }} />
                  <Typography variant="body2">
                    ストライク: {game.strikes}回
                  </Typography>
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <TrendingUpIcon color="secondary" sx={{ mr: 1 }} />
                  <Typography variant="body2">
                    スペア: {game.spares}回
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

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
