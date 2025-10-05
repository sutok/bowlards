import React from 'react';
import {
  Box,
  Button,
  Typography,
  Card,
  CardContent,
  Grid,
  Container,
  Paper,
  Chip
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { User } from 'firebase/auth';
import SportsIcon from '@mui/icons-material/Sports';
import HistoryIcon from '@mui/icons-material/History';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';

interface DashboardProps {
  user: User;
  onSignOut: () => void;
}

export default function Dashboard({ user, onSignOut }: DashboardProps) {
  const navigate = useNavigate();

  const handleStartNewGame = () => {
    navigate('/game');
  };

  const handleViewHistory = () => {
    navigate('/history');
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        {/* ヘッダー */}
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
          <Box>
            <Typography variant="h4" component="h1" gutterBottom>
              ようこそ、{user.displayName || 'ユーザー'}さん
            </Typography>
          </Box>
          <Button
            variant="outlined"
            onClick={onSignOut}
            sx={{ ml: 2 }}
          >
            ログアウト
          </Button>
        </Box>

        {/* クイックアクション */}
        <Paper sx={{ p: 3, mb: 4 }}>
          <Typography variant="h6" gutterBottom>
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6} md={4}>
              <Button
                fullWidth
                variant="contained"
                size="large"
                startIcon={<SportsIcon />}
                onClick={handleStartNewGame}
                sx={{ py: 2 }}
              >
                新しいゲームを開始
              </Button>
            </Grid>
            <Grid item xs={12} sm={6} md={4}>
              <Button
                fullWidth
                variant="outlined"
                size="large"
                startIcon={<HistoryIcon />}
                onClick={handleViewHistory}
                sx={{ py: 2 }}
              >
                ゲーム履歴を見る
              </Button>
            </Grid>
          </Grid>
        </Paper>

        {/* 統計情報カード */}
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <SportsIcon color="primary" sx={{ mr: 1 }} />
                  <Typography variant="h6">総ゲーム数</Typography>
                </Box>
                <Typography variant="h4" color="primary">
                  0
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  記録されたゲーム数
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <TrendingUpIcon color="secondary" sx={{ mr: 1 }} />
                  <Typography variant="h6">平均スコア</Typography>
                </Box>
                <Typography variant="h4" color="secondary">
                  -
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  過去のゲーム平均
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <HistoryIcon color="success" sx={{ mr: 1 }} />
                  <Typography variant="h6">最高スコア</Typography>
                </Box>
                <Typography variant="h4" color="success.main">
                  -
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  記録された最高スコア
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

      </Box>
    </Container>
  );
}
