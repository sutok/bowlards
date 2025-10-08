import React from 'react';
import {
  Box,
  Button,
  Typography,
  Grid,
  Container,
  Paper,
  Chip
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { User } from 'firebase/auth';
import SportsIcon from '@mui/icons-material/Sports';
import HistoryIcon from '@mui/icons-material/History';

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


      </Box>
    </Container>
  );
}
