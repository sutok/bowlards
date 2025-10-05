import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Container, Typography, Box } from '@mui/material';
import { onAuthStateChanged, signOut, User } from 'firebase/auth';
import { auth } from './firebase/config';
import AuthForm from './components/AuthForm';
import Dashboard from './components/Dashboard';
import GameRecord from './components/GameRecord';
import GameHistory from './components/GameHistory';
import GameDetail from './components/GameDetail';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setUser(user);
      setLoading(false);
    });

    return () => unsubscribe();
  }, []);

  const handleAuthStateChange = (user: User | null) => {
    setUser(user);
  };

  const handleSignOut = async () => {
    try {
      await signOut(auth);
      setUser(null);
      console.log('✅ ログアウトしました');
    } catch (error) {
      console.error('❌ ログアウトエラー:', error);
    }
  };

  const handleViewGameDetail = (gameId: string) => {
    // ゲーム詳細ページへのナビゲーション
    window.location.href = `/game/${gameId}`;
  };

  if (loading) {
    return (
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Container maxWidth="lg">
          <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
            <Typography variant="h6">読み込み中...</Typography>
          </Box>
        </Container>
      </ThemeProvider>
    );
  }

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Container maxWidth="lg">
          <Box sx={{ my: 4 }}>
            {/* <Typography variant="h4" component="h1" gutterBottom>
              Bawlards/Bowling
            </Typography> */}
            <Typography variant="body1">
              ボーリングスコア記録・管理アプリケーション
            </Typography>
            <Routes>
              <Route path="/" element={
                <Box sx={{ mt: 4 }}>
                  {user ? (
                    <Dashboard user={user} onSignOut={handleSignOut} />
                  ) : (
                    <AuthForm onAuthStateChange={handleAuthStateChange} />
                  )}
                </Box>
              } />
              <Route path="/game" element={
                user ? (
                  <GameRecord />
                ) : (
                  <AuthForm onAuthStateChange={handleAuthStateChange} />
                )
              } />
              <Route path="/history" element={
                user ? (
                  <GameHistory onViewGameDetail={handleViewGameDetail} />
                ) : (
                  <AuthForm onAuthStateChange={handleAuthStateChange} />
                )
              } />
              <Route path="/game/:gameId" element={
                user ? (
                  <GameDetail />
                ) : (
                  <AuthForm onAuthStateChange={handleAuthStateChange} />
                )
              } />
            </Routes>
          </Box>
        </Container>
      </Router>
    </ThemeProvider>
  );
}

export default App;
