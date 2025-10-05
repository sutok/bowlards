# 画面設計書

## 1. 概要

### 1.1 アプリケーション名
Scoring Bawlards/Bowling

### 1.2 画面設計の目的
ユーザーが直感的に操作できるボーリングスコア記録アプリケーションの画面設計を定義し、一貫性のあるUI/UXを提供する。

### 1.3 対象システム
- **フロントエンド**: React + Redux
- **UIライブラリ**: Material-UI (MUI) v5
- **レスポンシブデザイン**: モバイルファースト

## 2. 画面一覧

### 2.1 主要画面
1. **ログイン画面** (`/login`)
2. **新規登録画面** (`/signup`)
3. **ダッシュボード** (`/`)
4. **ゲーム記録作成画面** (`/game`)
5. **ゲーム履歴画面** (`/history`)

### 2.2 共通レイアウト
- **ヘッダー**: ナビゲーション、ユーザー情報
- **サイドバー**: メニュー（モバイルではドロワー）
- **メインコンテンツ**: 各画面の内容
- **フッター**: アプリケーション情報

## 3. 画面詳細設計

### 3.1 ログイン画面

#### 3.1.1 画面構成
```typescript
interface LoginPageProps {}

const LoginPage: React.FC<LoginPageProps> = () => {
  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      }}
    >
      <Card sx={{ p: 4, maxWidth: 400, width: '100%', mx: 2 }}>
        <Box sx={{ textAlign: 'center', mb: 3 }}>
          <SportsIcon sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
          <Typography variant="h4" component="h1" gutterBottom>
            Scoring Bawlards
          </Typography>
          <Typography variant="body1" color="text.secondary">
            ボーリングスコアを記録しましょう
          </Typography>
        </Box>
        
        <LoginForm 
          onGoogleLogin={handleGoogleLogin}
          onEmailLogin={handleEmailLogin}
          onSignUp={() => navigate('/signup')}
          isLoading={isLoading}
          error={error}
        />
        
        <Box sx={{ mt: 3, textAlign: 'center' }}>
          <Typography variant="body2" color="text.secondary">
            アカウントをお持ちでない方は
          </Typography>
          <Link 
            component={RouterLink} 
            to="/signup" 
            variant="body2"
            sx={{ ml: 1 }}
          >
            こちらから登録
          </Link>
        </Box>
      </Card>
    </Box>
  );
};
```

#### 3.1.2 LoginFormコンポーネント
```typescript
interface LoginFormProps {
  onGoogleLogin: () => void;
  onEmailLogin: (email: string, password: string) => void;
  onSignUp: () => void;
  isLoading: boolean;
  error: string | null;
}

const LoginForm: React.FC<LoginFormProps> = ({
  onGoogleLogin,
  onEmailLogin,
  onSignUp,
  isLoading,
  error,
}) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showEmailForm, setShowEmailForm] = useState(false);
  
  const handleEmailSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onEmailLogin(email, password);
  };
  
  return (
    <Box>
      {/* Google認証ボタン */}
      <Button
        fullWidth
        variant="outlined"
        size="large"
        startIcon={<GoogleIcon />}
        onClick={onGoogleLogin}
        disabled={isLoading}
        sx={{ mb: 2 }}
      >
        Googleでログイン
      </Button>
      
      {/* 区切り線 */}
      <Box sx={{ display: 'flex', alignItems: 'center', my: 2 }}>
        <Divider sx={{ flexGrow: 1 }} />
        <Typography variant="body2" color="text.secondary" sx={{ px: 2 }}>
          または
        </Typography>
        <Divider sx={{ flexGrow: 1 }} />
      </Box>
      
      {/* メール/パスワードフォーム */}
      {showEmailForm ? (
        <form onSubmit={handleEmailSubmit}>
          <TextField
            fullWidth
            label="メールアドレス"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            margin="normal"
            required
            disabled={isLoading}
          />
          <TextField
            fullWidth
            label="パスワード"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            margin="normal"
            required
            disabled={isLoading}
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            size="large"
            disabled={isLoading}
            sx={{ mt: 2, mb: 1 }}
          >
            {isLoading ? <CircularProgress size={24} /> : 'ログイン'}
          </Button>
          <Button
            fullWidth
            variant="text"
            onClick={() => setShowEmailForm(false)}
            disabled={isLoading}
          >
            キャンセル
          </Button>
        </form>
      ) : (
        <Button
          fullWidth
          variant="outlined"
          size="large"
          onClick={() => setShowEmailForm(true)}
          disabled={isLoading}
        >
          メールでログイン
        </Button>
      )}
      
      {/* エラーメッセージ */}
      {error && (
        <Alert severity="error" sx={{ mt: 2 }}>
          {error}
        </Alert>
      )}
    </Box>
  );
};
```

#### 3.1.3 レイアウト仕様
- **背景**: グラデーション（青紫系）
- **カード**: 中央配置、最大幅400px
- **ロゴ**: ボーリングアイコン + アプリ名
- **フォーム**: Google認証ボタン、メール/パスワード入力
- **認証方式**: Google認証（プライマリ）、メール/パスワード（セカンダリ）

### 3.2 新規登録画面

#### 3.2.1 画面構成

##### 3.2.1.1 パーツ
- ダッシュボードに戻るリンク

###### 3.2.1.2 スコア入力
- 現在どのフレームに対するフォーカスが当たっているか
- フォーカスが当たっているフレームの前後のフレーム番号を表示（MUI Pagenation）
- フォーカスが当たっているフレームの前後のフレームを表示(MUI)
- 投球スコア入力ボタン
- フレーム間を移動するボタンをフレーム番号の両脇に置くこと

###### 3.2.1.3 フレーム間を移動可能とするルール

####### 3.2.1.3.1 Prev
- フレーム番号が2から10の時に表示すること

####### 3.2.1.3.2 Next
- フレーム番号が1から9の時に表示すること
- 現在のフレームにスコアが2投分または10点であれば表示すること

###### 3.2.1.4 ゲームスコアの保持
- ゲームスコアは1ゲームのみ保持されること
- 1ゲームには10フレームが含まれること
- ゲーム終了ボタンを押さない限り、いつでも再開できる
- 誤ってアプリ終了やTOPページに戻った場合には「ゲーム再開」「新規ゲーム」ボタンが表示されること

###### 3.2.1.5 ゲーム終了ボタン
- 画面下部に表示
- ゲーム終了ボタンを押したら以後編集はできないこと

###### 3.2.1.6 ゲーム得点表示に関して
- 各フレーム1投目に0点だった場合は「G」と表示されること
- 各フレーム1投目に10点だった場合は「X」と表示されること
- 各フレーム2投目に0点だった場合は「-」と表示されること
- 各フレーム2投目に1投目と合わせて10点だった場合は「/」と表示されること
- 10フレームは最大3投できること
- 10フレーム目の1投目で10点だった場合は3投できること
- 10フレーム目の1投目と2投目で合計10点だった場合は3投できること
- 10フレームは最大30点得点できること


#### 3.2.2 SignUpFormコンポーネント
```typescript
interface SignUpFormProps {
  onGoogleSignUp: () => void;
  onEmailSignUp: (email: string, password: string, displayName: string) => void;
  onLogin: () => void;
  isLoading: boolean;
  error: string | null;
}

const SignUpForm: React.FC<SignUpFormProps> = ({
  onGoogleSignUp,
  onEmailSignUp,
  onLogin,
  isLoading,
  error,
}) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [displayName, setDisplayName] = useState('');
  const [showEmailForm, setShowEmailForm] = useState(false);
  const [passwordError, setPasswordError] = useState('');
  
  const handleEmailSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    // パスワード確認
    if (password !== confirmPassword) {
      setPasswordError('パスワードが一致しません');
      return;
    }
    
    // パスワード強度チェック
    if (password.length < 6) {
      setPasswordError('パスワードは6文字以上で入力してください');
      return;
    }
    
    setPasswordError('');
    onEmailSignUp(email, password, displayName);
  };
  
  return (
    <Box>
      {/* Google認証ボタン */}
      <Button
        fullWidth
        variant="outlined"
        size="large"
        startIcon={<GoogleIcon />}
        onClick={onGoogleSignUp}
        disabled={isLoading}
        sx={{ mb: 2 }}
      >
        Googleで登録
      </Button>
      
      {/* 区切り線 */}
      <Box sx={{ display: 'flex', alignItems: 'center', my: 2 }}>
        <Divider sx={{ flexGrow: 1 }} />
        <Typography variant="body2" color="text.secondary" sx={{ px: 2 }}>
          または
        </Typography>
        <Divider sx={{ flexGrow: 1 }} />
      </Box>
      
      {/* メール/パスワードフォーム */}
      {showEmailForm ? (
        <form onSubmit={handleEmailSubmit}>
          <TextField
            fullWidth
            label="表示名"
            value={displayName}
            onChange={(e) => setDisplayName(e.target.value)}
            margin="normal"
            required
            disabled={isLoading}
            helperText="ボーリングスコアに表示される名前です"
          />
          <TextField
            fullWidth
            label="メールアドレス"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            margin="normal"
            required
            disabled={isLoading}
          />
          <TextField
            fullWidth
            label="パスワード"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            margin="normal"
            required
            disabled={isLoading}
            helperText="6文字以上で入力してください"
          />
          <TextField
            fullWidth
            label="パスワード（確認）"
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            margin="normal"
            required
            disabled={isLoading}
            error={!!passwordError}
            helperText={passwordError}
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            size="large"
            disabled={isLoading}
            sx={{ mt: 2, mb: 1 }}
          >
            {isLoading ? <CircularProgress size={24} /> : 'アカウント作成'}
          </Button>
          <Button
            fullWidth
            variant="text"
            onClick={() => setShowEmailForm(false)}
            disabled={isLoading}
          >
            キャンセル
          </Button>
        </form>
      ) : (
        <Button
          fullWidth
          variant="outlined"
          size="large"
          onClick={() => setShowEmailForm(true)}
          disabled={isLoading}
        >
          メールで登録
        </Button>
      )}
      
      {/* エラーメッセージ */}
      {error && (
        <Alert severity="error" sx={{ mt: 2 }}>
          {error}
        </Alert>
      )}
      
      {/* 利用規約・プライバシーポリシー */}
      <Box sx={{ mt: 2, textAlign: 'center' }}>
        <Typography variant="caption" color="text.secondary">
          アカウント作成により、
          <Link href="/terms" target="_blank">
            利用規約
          </Link>
          および
          <Link href="/privacy" target="_blank">
            プライバシーポリシー
          </Link>
          に同意したものとみなされます。
        </Typography>
      </Box>
    </Box>
  );
};
```

#### 3.2.3 レイアウト仕様
- **背景**: ログイン画面と同じグラデーション（青紫系）
- **カード**: 中央配置、最大幅400px
- **ロゴ**: ボーリングアイコン + アプリ名
- **フォーム**: Google認証ボタン、メール/パスワード入力
- **認証方式**: Google認証（プライマリ）、メール/パスワード（セカンダリ）
- **バリデーション**: パスワード強度、確認入力、表示名必須

### 3.3 ダッシュボード画面

#### 3.2.1 画面構成
```typescript
const Dashboard: React.FC = () => {
  const { user } = useSelector((state: RootState) => state.auth);
  const { games, statistics } = useSelector((state: RootState) => state.history);
  
  return (
    <Container maxWidth="lg">
      {/* ウェルカムセクション */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          ようこそ、{user?.displayName}さん
        </Typography>
        <Typography variant="body1" color="text.secondary">
          今日もボーリングを楽しみましょう！
        </Typography>
      </Box>
      
      {/* クイックアクション */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={4}>
          <QuickActionCard
            title="新しいゲーム"
            description="ボーリングゲームを開始"
            icon={<PlayArrowIcon />}
            color="primary"
            href="/game"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <QuickActionCard
            title="履歴を見る"
            description="過去のゲーム記録"
            icon={<HistoryIcon />}
            color="secondary"
            href="/history"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <QuickActionCard
            title="統計情報"
            description="スコアの分析"
            icon={<AnalyticsIcon />}
            color="success"
            href="/statistics"
          />
        </Grid>
      </Grid>
      
      {/* 統計カード */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={6}>
          <StatCard
            title="今月のゲーム数"
            value={statistics.gamesThisMonth}
            icon={<CalendarMonthIcon />}
            color="primary"
          />
        </Grid>
        <Grid item xs={12} md={6}>
          <StatCard
            title="平均スコア"
            value={Math.round(statistics.averageScore)}
            icon={<TrendingUpIcon />}
            color="success"
          />
        </Grid>
      </Grid>
      
      {/* 最近のゲーム */}
      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          最近のゲーム
        </Typography>
        <RecentGamesList games={games.slice(0, 5)} />
      </Paper>
    </Container>
  );
};
```

#### 3.2.2 レイアウト仕様
- **ヘッダー**: ユーザー名、ウェルカムメッセージ
- **クイックアクション**: 3つの主要機能へのショートカット
- **統計カード**: 重要な数値を視覚的に表示
- **最近のゲーム**: 最新5件のゲーム履歴

### 3.3 ゲーム記録作成画面

#### 3.3.1 画面構成
```typescript
const GameRecordPage: React.FC = () => {
  const { currentGame, isRecording } = useSelector((state: RootState) => state.game);
  
  return (
    <Container maxWidth="lg">
      {/* ゲームヘッダー */}
      <GameHeader 
        game={currentGame}
        isRecording={isRecording}
      />
      
      {/* スコアボード */}
      <ScoreBoard 
        frames={currentGame?.frames || []}
        totalScore={currentGame?.totalScore || 0}
      />
      
      {/* 投球入力 */}
      <RollInput 
        currentFrame={getCurrentFrame(currentGame?.frames)}
        onRollInput={handleRollInput}
        disabled={!isRecording}
      />
      
      {/* ゲームコントロール */}
      <GameControls 
        isRecording={isRecording}
        onStartGame={handleStartGame}
        onFinishGame={handleFinishGame}
        canFinish={canFinishGame(currentGame?.frames)}
      />
    </Container>
  );
};
```

#### 3.3.2 レイアウト仕様
- **ゲームヘッダー**: ゲーム状態、日時、進行状況
- **スコアボード**: 10フレーム + 合計スコアの表示
- **投球入力**: ピン選択、投球ボタン
- **ゲームコントロール**: 開始、終了、リセットボタン

### 3.4 ゲーム履歴画面

#### 3.4.1 画面構成
```typescript
const GameHistoryPage: React.FC = () => {
  const { games, pagination, statistics } = useSelector(
    (state: RootState) => state.history
  );
  
  return (
    <Container maxWidth="lg">
      {/* ページヘッダー */}
      <Box sx={{ mb: 3 }}>
        <Typography variant="h4" gutterBottom>
          ゲーム履歴
        </Typography>
        <Typography variant="body1" color="text.secondary">
          過去のゲーム記録と統計情報
        </Typography>
      </Box>
      
      {/* 統計情報 */}
      <StatisticsCard statistics={statistics} />
      
      {/* フィルター */}
      <FilterControls 
        filters={filters}
        onFilterChange={handleFilterChange}
      />
      
      {/* ゲーム一覧 */}
      <GameList 
        games={games}
        onDeleteGame={handleDeleteGame}
        isLoading={isLoading}
      />
      
      {/* ページング */}
      <PaginationControls 
        pagination={pagination}
        onPageChange={handlePageChange}
      />
    </Container>
  );
};
```

#### 3.4.2 レイアウト仕様
- **ページヘッダー**: タイトル、説明
- **統計情報**: 4つの主要統計をカード表示
- **フィルター**: 日付範囲、スコア範囲での絞り込み
- **ゲーム一覧**: 10件ずつのページング表示
- **ページング**: 前後ページナビゲーション

## 4. 共通コンポーネント設計

### 4.1 レイアウトコンポーネント

#### 4.1.1 メインレイアウト
```typescript
const Layout: React.FC<LayoutProps> = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  
  return (
    <Box sx={{ display: 'flex' }}>
      {/* サイドバー */}
      <Sidebar 
        open={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
      />
      
      {/* メインコンテンツ */}
      <Box component="main" sx={{ flexGrow: 1 }}>
        <Header 
          onMenuClick={() => setSidebarOpen(true)}
        />
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      </Box>
    </Box>
  );
};
```

#### 4.1.2 ヘッダー
```typescript
const Header: React.FC<HeaderProps> = ({ onMenuClick }) => {
  const { user } = useSelector((state: RootState) => state.auth);
  
  return (
    <AppBar position="static" sx={{ mb: 2 }}>
      <Toolbar>
        <IconButton
          edge="start"
          color="inherit"
          onClick={onMenuClick}
          sx={{ mr: 2, display: { md: 'none' } }}
        >
          <MenuIcon />
        </IconButton>
        
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          Scoring Bawlards
        </Typography>
        
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <Typography variant="body2">
            {user?.displayName}
          </Typography>
          <Avatar 
            src={user?.photoURL} 
            alt={user?.displayName}
            sx={{ width: 32, height: 32 }}
          />
          <IconButton color="inherit" onClick={handleLogout}>
            <LogoutIcon />
          </IconButton>
        </Box>
      </Toolbar>
    </AppBar>
  );
};
```

#### 4.1.3 サイドバー
```typescript
const Sidebar: React.FC<SidebarProps> = ({ open, onClose }) => {
  const location = useLocation();
  
  const menuItems = [
    { text: 'ダッシュボード', icon: <DashboardIcon />, path: '/' },
    { text: 'ゲーム記録', icon: <SportsIcon />, path: '/game' },
    { text: '履歴', icon: <HistoryIcon />, path: '/history' },
  ];
  
  return (
    <>
      {/* デスクトップサイドバー */}
      <Drawer
        variant="permanent"
        sx={{
          display: { xs: 'none', md: 'block' },
          '& .MuiDrawer-paper': {
            boxSizing: 'border-box',
            width: 240,
          },
        }}
      >
        <Toolbar>
          <Typography variant="h6" noWrap>
            Menu
          </Typography>
        </Toolbar>
        <Divider />
        <List>
          {menuItems.map((item) => (
            <ListItem key={item.text} disablePadding>
              <ListItemButton
                selected={location.pathname === item.path}
                component={Link}
                to={item.path}
              >
                <ListItemIcon>{item.icon}</ListItemIcon>
                <ListItemText primary={item.text} />
              </ListItemButton>
            </ListItem>
          ))}
        </List>
      </Drawer>
      
      {/* モバイルドロワー */}
      <Drawer
        variant="temporary"
        open={open}
        onClose={onClose}
        ModalProps={{ keepMounted: true }}
        sx={{
          display: { xs: 'block', md: 'none' },
          '& .MuiDrawer-paper': {
            boxSizing: 'border-box',
            width: 240,
          },
        }}
      >
        {/* モバイルメニュー内容 */}
      </Drawer>
    </>
  );
};
```

### 4.2 カードコンポーネント

#### 4.2.1 クイックアクションカード
```typescript
interface QuickActionCardProps {
  title: string;
  description: string;
  icon: React.ReactNode;
  color: 'primary' | 'secondary' | 'success';
  href: string;
}

const QuickActionCard: React.FC<QuickActionCardProps> = ({
  title,
  description,
  icon,
  color,
  href,
}) => {
  return (
    <Card
      component={Link}
      to={href}
      sx={{
        p: 3,
        textAlign: 'center',
        textDecoration: 'none',
        transition: 'transform 0.2s',
        '&:hover': {
          transform: 'translateY(-4px)',
        },
      }}
    >
      <Box
        sx={{
          width: 60,
          height: 60,
          borderRadius: '50%',
          backgroundColor: `${color}.light`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          mx: 'auto',
          mb: 2,
        }}
      >
        {icon}
      </Box>
      <Typography variant="h6" gutterBottom>
        {title}
      </Typography>
      <Typography variant="body2" color="text.secondary">
        {description}
      </Typography>
    </Card>
  );
};
```

#### 4.2.2 統計カード
```typescript
interface StatCardProps {
  title: string;
  value: number;
  icon: React.ReactNode;
  color: 'primary' | 'secondary' | 'success' | 'warning';
}

const StatCard: React.FC<StatCardProps> = ({ title, value, icon, color }) => {
  return (
    <Card sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
        <Box
          sx={{
            width: 48,
            height: 48,
            borderRadius: '50%',
            backgroundColor: `${color}.light`,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            mr: 2,
          }}
        >
          {icon}
        </Box>
        <Box>
          <Typography variant="h4" color={`${color}.main`}>
            {value}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {title}
          </Typography>
        </Box>
      </Box>
    </Card>
  );
};
```

## 5. レスポンシブデザイン

### 5.1 ブレークポイント
```typescript
const theme = createTheme({
  breakpoints: {
    values: {
      xs: 0,
      sm: 600,
      md: 900,
      lg: 1200,
      xl: 1536,
    },
  },
});
```

### 5.2 レスポンシブ対応
- **モバイル (xs)**: 320px以上
  - サイドバーをドロワーに変更
  - カードを縦並びに配置
  - フォントサイズを調整
  
- **タブレット (sm)**: 600px以上
  - 2列レイアウト
  - サイドバー表示
  
- **デスクトップ (md以上)**: 900px以上
  - 3列レイアウト
  - 固定サイドバー
  - 最大幅コンテナ

## 6. カラーパレット

### 6.1 テーマカラー
```typescript
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
      light: '#42a5f5',
      dark: '#1565c0',
    },
    secondary: {
      main: '#dc004e',
      light: '#ff5983',
      dark: '#9a0036',
    },
    success: {
      main: '#2e7d32',
      light: '#4caf50',
      dark: '#1b5e20',
    },
    warning: {
      main: '#ed6c02',
      light: '#ff9800',
      dark: '#e65100',
    },
    error: {
      main: '#d32f2f',
      light: '#ef5350',
      dark: '#c62828',
    },
  },
});
```

### 6.2 セマンティックカラー
- **ストライク**: 金色系 (#ffd700)
- **スペア**: 銀色系 (#c0c0c0)
- **通常スコア**: 青色系
- **エラー**: 赤色系
- **成功**: 緑色系

## 7. タイポグラフィ

### 7.1 フォント設定
```typescript
const theme = createTheme({
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontSize: '2.5rem',
      fontWeight: 500,
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 500,
    },
    h3: {
      fontSize: '1.75rem',
      fontWeight: 500,
    },
    h4: {
      fontSize: '1.5rem',
      fontWeight: 500,
    },
    h5: {
      fontSize: '1.25rem',
      fontWeight: 500,
    },
    h6: {
      fontSize: '1rem',
      fontWeight: 500,
    },
    body1: {
      fontSize: '1rem',
    },
    body2: {
      fontSize: '0.875rem',
    },
  },
});
```

## 8. アニメーション

### 8.1 トランジション
```typescript
const transitions = {
  duration: {
    shortest: 150,
    shorter: 200,
    short: 250,
    standard: 300,
    complex: 375,
    enteringScreen: 225,
    leavingScreen: 195,
  },
  easing: {
    easeInOut: 'cubic-bezier(0.4, 0, 0.2, 1)',
    easeOut: 'cubic-bezier(0.0, 0, 0.2, 1)',
    easeIn: 'cubic-bezier(0.4, 0, 1, 1)',
    sharp: 'cubic-bezier(0.4, 0, 0.6, 1)',
  },
};
```

### 8.2 カスタムアニメーション
```typescript
const fadeInUp = keyframes`
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
`;

const slideIn = keyframes`
  from {
    transform: translateX(-100%);
  }
  to {
    transform: translateX(0);
  }
`;
```

## 9. アクセシビリティ

### 9.1 キーボードナビゲーション
- **Tab**: フォーカス移動
- **Enter/Space**: ボタンアクティベート
- **Escape**: モーダル閉じる
- **Arrow Keys**: メニューナビゲーション

### 9.2 スクリーンリーダー対応
```typescript
// ARIA属性の設定例
<Button
  aria-label="ゲームを開始する"
  aria-describedby="game-start-description"
>
  ゲーム開始
</Button>
<Typography id="game-start-description" variant="caption">
  新しいボーリングゲームを開始します
</Typography>
```

## 10. パフォーマンス最適化

### 10.1 画像最適化
- **WebP形式**: 対応ブラウザで使用
- **遅延読み込み**: Intersection Observer API
- **レスポンシブ画像**: デバイスサイズに応じた画像

### 10.2 コード分割
```typescript
const LoginPage = lazy(() => import('./pages/LoginPage'));
const SignUpPage = lazy(() => import('./pages/SignUpPage'));
const Dashboard = lazy(() => import('./pages/Dashboard'));
const GameRecord = lazy(() => import('./pages/GameRecord'));
const GameHistory = lazy(() => import('./pages/GameHistory'));
const NotFound = lazy(() => import('./pages/NotFound'));

const AppRoutes = () => {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignUpPage />} />
        <Route path="/" element={
          <ProtectedRoute>
            <Layout />
          </ProtectedRoute>
        }>
          <Route index element={<Dashboard />} />
          <Route path="game" element={<GameRecord />} />
          <Route path="history" element={<GameHistory />} />
        </Route>
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Suspense>
  );
};
```

## 11. 変更履歴

| バージョン | 日付 | 変更内容 | 担当者 |
|-----------|------|----------|--------|
| 1.0.0 | 2024-01-01 | 初版作成 | システムエンジニア |

---

**注意事項**:
- レスポンシブデザインは必ずモバイルファーストで設計すること
- アクセシビリティガイドラインに準拠すること
- パフォーマンス要件を満たすこと
