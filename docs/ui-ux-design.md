# UI/UX設計書

## 1. 概要

### 1.1 アプリケーション名
Scoring Bawlards/Bowling

### 1.2 UI/UX設計の目的
ユーザーが直感的で快適にボーリングスコアを記録・管理できるUI/UXを設計し、一貫性のあるユーザー体験を提供する。

### 1.3 設計原則
1. **シンプルさ**: 直感的で分かりやすいインターフェース
2. **一貫性**: 統一されたデザインシステム
3. **アクセシビリティ**: 誰でも使いやすい設計
4. **レスポンシブ**: あらゆるデバイスで最適な体験
5. **パフォーマンス**: 高速でスムーズな操作

## 2. デザインシステム

### 2.1 カラーパレット

#### 2.1.1 プライマリカラー
```typescript
const primaryColors = {
  main: '#1976d2',      // メインブルー
  light: '#42a5f5',     // ライトブルー
  dark: '#1565c0',      // ダークブルー
  contrast: '#ffffff',  // コントラスト（白）
};
```

#### 2.1.2 セカンダリカラー
```typescript
const secondaryColors = {
  main: '#dc004e',      // メインピンク
  light: '#ff5983',     // ライトピンク
  dark: '#9a0036',      // ダークピンク
  contrast: '#ffffff',  // コントラスト（白）
};
```

#### 2.1.3 セマンティックカラー
```typescript
const semanticColors = {
  success: '#2e7d32',   // 成功（緑）
  warning: '#ed6c02',   // 警告（オレンジ）
  error: '#d32f2f',     // エラー（赤）
  info: '#0288d1',      // 情報（青）
  
  // ボーリング専用カラー
  strike: '#ffd700',    // ストライク（金）
  spare: '#c0c0c0',     // スペア（銀）
  gutter: '#8d6e63',    // ガター（茶）
};
```

#### 2.1.4 ニュートラルカラー
```typescript
const neutralColors = {
  white: '#ffffff',
  black: '#000000',
  grey50: '#fafafa',
  grey100: '#f5f5f5',
  grey200: '#eeeeee',
  grey300: '#e0e0e0',
  grey400: '#bdbdbd',
  grey500: '#9e9e9e',
  grey600: '#757575',
  grey700: '#616161',
  grey800: '#424242',
  grey900: '#212121',
};
```

### 2.2 タイポグラフィ

#### 2.2.1 フォントファミリー
```typescript
const typography = {
  fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
  fontFamilyMono: '"Roboto Mono", "Courier New", monospace',
};
```

#### 2.2.2 フォントサイズ
```typescript
const fontSize = {
  xs: '0.75rem',    // 12px
  sm: '0.875rem',   // 14px
  base: '1rem',     // 16px
  lg: '1.125rem',   // 18px
  xl: '1.25rem',    // 20px
  '2xl': '1.5rem',  // 24px
  '3xl': '1.875rem', // 30px
  '4xl': '2.25rem', // 36px
  '5xl': '3rem',    // 48px
};
```

#### 2.2.3 フォントウェイト
```typescript
const fontWeight = {
  light: 300,
  normal: 400,
  medium: 500,
  semibold: 600,
  bold: 700,
};
```

### 2.3 スペーシング

#### 2.3.1 スペーシングスケール
```typescript
const spacing = {
  0: '0',
  1: '0.25rem',   // 4px
  2: '0.5rem',    // 8px
  3: '0.75rem',   // 12px
  4: '1rem',      // 16px
  5: '1.25rem',   // 20px
  6: '1.5rem',    // 24px
  8: '2rem',      // 32px
  10: '2.5rem',   // 40px
  12: '3rem',     // 48px
  16: '4rem',     // 64px
  20: '5rem',     // 80px
  24: '6rem',     // 96px
};
```

### 2.4 ボーダーラディウス

#### 2.4.1 角丸設定
```typescript
const borderRadius = {
  none: '0',
  sm: '0.125rem',   // 2px
  base: '0.25rem',  // 4px
  md: '0.375rem',   // 6px
  lg: '0.5rem',     // 8px
  xl: '0.75rem',    // 12px
  '2xl': '1rem',    // 16px
  '3xl': '1.5rem',  // 24px
  full: '9999px',   // 完全な円
};
```

### 2.5 シャドウ

#### 2.5.1 ボックスシャドウ
```typescript
const boxShadow = {
  sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
  base: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
  md: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
  lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
  xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
  '2xl': '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
  inner: 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)',
};
```

## 3. コンポーネントデザイン

### 3.1 ボタン

#### 3.1.1 ボタンバリエーション
```typescript
const buttonVariants = {
  primary: {
    backgroundColor: 'primary.main',
    color: 'primary.contrast',
    '&:hover': {
      backgroundColor: 'primary.dark',
    },
  },
  secondary: {
    backgroundColor: 'secondary.main',
    color: 'secondary.contrast',
    '&:hover': {
      backgroundColor: 'secondary.dark',
    },
  },
  outline: {
    backgroundColor: 'transparent',
    color: 'primary.main',
    border: '1px solid',
    borderColor: 'primary.main',
    '&:hover': {
      backgroundColor: 'primary.light',
      color: 'primary.contrast',
    },
  },
  text: {
    backgroundColor: 'transparent',
    color: 'primary.main',
    '&:hover': {
      backgroundColor: 'grey.100',
    },
  },
};
```

#### 3.1.2 ボタンサイズ
```typescript
const buttonSizes = {
  small: {
    padding: '0.5rem 1rem',
    fontSize: '0.875rem',
    minHeight: '32px',
  },
  medium: {
    padding: '0.75rem 1.5rem',
    fontSize: '1rem',
    minHeight: '40px',
  },
  large: {
    padding: '1rem 2rem',
    fontSize: '1.125rem',
    minHeight: '48px',
  },
};
```

### 3.2 カード

#### 3.2.1 カードデザイン
```typescript
const cardStyles = {
  base: {
    backgroundColor: 'white',
    borderRadius: '0.5rem',
    boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
    padding: '1.5rem',
    transition: 'box-shadow 0.2s ease-in-out',
    '&:hover': {
      boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
    },
  },
  elevated: {
    backgroundColor: 'white',
    borderRadius: '0.75rem',
    boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
    padding: '2rem',
  },
  outlined: {
    backgroundColor: 'transparent',
    borderRadius: '0.5rem',
    border: '1px solid',
    borderColor: 'grey.300',
    padding: '1.5rem',
  },
};
```

### 3.3 フォーム要素

#### 3.3.1 入力フィールド
```typescript
const inputStyles = {
  base: {
    width: '100%',
    padding: '0.75rem 1rem',
    border: '1px solid',
    borderColor: 'grey.300',
    borderRadius: '0.375rem',
    fontSize: '1rem',
    transition: 'border-color 0.2s ease-in-out',
    '&:focus': {
      outline: 'none',
      borderColor: 'primary.main',
      boxShadow: '0 0 0 3px rgba(25, 118, 210, 0.1)',
    },
    '&:disabled': {
      backgroundColor: 'grey.100',
      color: 'grey.500',
      cursor: 'not-allowed',
    },
  },
  error: {
    borderColor: 'error.main',
    '&:focus': {
      borderColor: 'error.main',
      boxShadow: '0 0 0 3px rgba(211, 47, 47, 0.1)',
    },
  },
};
```

### 3.4 ナビゲーション

#### 3.4.1 メニューアイテム
```typescript
const menuItemStyles = {
  base: {
    display: 'flex',
    alignItems: 'center',
    padding: '0.75rem 1rem',
    borderRadius: '0.375rem',
    color: 'grey.700',
    textDecoration: 'none',
    transition: 'all 0.2s ease-in-out',
    '&:hover': {
      backgroundColor: 'grey.100',
      color: 'primary.main',
    },
  },
  active: {
    backgroundColor: 'primary.light',
    color: 'primary.main',
    fontWeight: 'medium',
  },
};
```

## 4. レイアウトシステム

### 4.1 グリッドシステム

#### 4.1.1 ブレークポイント
```typescript
const breakpoints = {
  xs: '0px',      // モバイル
  sm: '600px',    // タブレット
  md: '900px',    // デスクトップ
  lg: '1200px',   // 大画面デスクトップ
  xl: '1536px',   // 超大画面
};
```

#### 4.1.2 コンテナサイズ
```typescript
const containerSizes = {
  sm: '600px',
  md: '900px',
  lg: '1200px',
  xl: '1536px',
};
```

### 4.2 レスポンシブレイアウト

#### 4.2.1 モバイルファースト設計
```typescript
const responsiveLayout = {
  // モバイル（デフォルト）
  mobile: {
    container: {
      padding: '1rem',
      maxWidth: '100%',
    },
    grid: {
      columns: 1,
      gap: '1rem',
    },
    sidebar: {
      position: 'drawer',
      width: '240px',
    },
  },
  
  // タブレット
  tablet: {
    container: {
      padding: '1.5rem',
      maxWidth: '900px',
    },
    grid: {
      columns: 2,
      gap: '1.5rem',
    },
    sidebar: {
      position: 'fixed',
      width: '240px',
    },
  },
  
  // デスクトップ
  desktop: {
    container: {
      padding: '2rem',
      maxWidth: '1200px',
    },
    grid: {
      columns: 3,
      gap: '2rem',
    },
    sidebar: {
      position: 'fixed',
      width: '240px',
    },
  },
};
```

## 5. インタラクションデザイン

### 5.1 アニメーション

#### 5.1.1 トランジション
```typescript
const transitions = {
  duration: {
    fast: '150ms',
    normal: '300ms',
    slow: '500ms',
  },
  easing: {
    easeInOut: 'cubic-bezier(0.4, 0, 0.2, 1)',
    easeOut: 'cubic-bezier(0.0, 0, 0.2, 1)',
    easeIn: 'cubic-bezier(0.4, 0, 1, 1)',
  },
};
```

#### 5.1.2 ホバーエフェクト
```typescript
const hoverEffects = {
  lift: {
    transition: 'transform 0.2s ease-in-out',
    '&:hover': {
      transform: 'translateY(-2px)',
    },
  },
  scale: {
    transition: 'transform 0.2s ease-in-out',
    '&:hover': {
      transform: 'scale(1.05)',
    },
  },
  glow: {
    transition: 'box-shadow 0.2s ease-in-out',
    '&:hover': {
      boxShadow: '0 0 20px rgba(25, 118, 210, 0.3)',
    },
  },
};
```

### 5.2 フィードバック

#### 5.2.1 ローディング状態
```typescript
const loadingStates = {
  spinner: {
    animation: 'spin 1s linear infinite',
    '@keyframes spin': {
      '0%': { transform: 'rotate(0deg)' },
      '100%': { transform: 'rotate(360deg)' },
    },
  },
  skeleton: {
    backgroundColor: 'grey.200',
    borderRadius: '0.25rem',
    animation: 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
    '@keyframes pulse': {
      '0%, 100%': { opacity: 1 },
      '50%': { opacity: 0.5 },
    },
  },
};
```

#### 5.2.2 エラー状態
```typescript
const errorStates = {
  input: {
    borderColor: 'error.main',
    '&:focus': {
      borderColor: 'error.main',
      boxShadow: '0 0 0 3px rgba(211, 47, 47, 0.1)',
    },
  },
  message: {
    color: 'error.main',
    fontSize: '0.875rem',
    marginTop: '0.25rem',
  },
};
```

## 6. アクセシビリティ

### 6.1 カラーコントラスト

#### 6.1.1 WCAG準拠
```typescript
const contrastRatios = {
  normal: {
    AA: 4.5,  // 通常テキスト
    AAA: 7.0, // 高コントラスト
  },
  large: {
    AA: 3.0,  // 大きなテキスト
    AAA: 4.5, // 高コントラスト
  },
};
```

### 6.2 フォーカス管理

#### 6.2.1 フォーカススタイル
```typescript
const focusStyles = {
  visible: {
    outline: '2px solid',
    outlineColor: 'primary.main',
    outlineOffset: '2px',
  },
  keyboard: {
    '&:focus-visible': {
      outline: '2px solid',
      outlineColor: 'primary.main',
      outlineOffset: '2px',
    },
  },
};
```

### 6.3 スクリーンリーダー対応

#### 6.3.1 ARIA属性
```typescript
const ariaAttributes = {
  button: {
    role: 'button',
    tabIndex: 0,
  },
  navigation: {
    role: 'navigation',
    'aria-label': 'メインナビゲーション',
  },
  form: {
    role: 'form',
    'aria-label': 'ゲーム記録フォーム',
  },
};
```

## 7. パフォーマンス最適化

### 7.1 画像最適化

#### 7.1.1 レスポンシブ画像
```typescript
const imageOptimization = {
  formats: ['webp', 'avif', 'jpg', 'png'],
  sizes: {
    mobile: '400px',
    tablet: '800px',
    desktop: '1200px',
  },
  lazy: true,
  placeholder: 'blur',
};
```

### 7.2 アニメーション最適化

#### 7.2.1 GPU加速
```typescript
const gpuAcceleration = {
  transform: 'translateZ(0)',
  willChange: 'transform',
  backfaceVisibility: 'hidden',
  perspective: '1000px',
};
```

## 8. ダークモード対応

### 8.1 ダークテーマ

#### 8.1.1 ダークカラーパレット
```typescript
const darkTheme = {
  palette: {
    mode: 'dark',
    primary: {
      main: '#90caf9',
      light: '#e3f2fd',
      dark: '#42a5f5',
    },
    background: {
      default: '#121212',
      paper: '#1e1e1e',
    },
    text: {
      primary: '#ffffff',
      secondary: 'rgba(255, 255, 255, 0.7)',
    },
  },
};
```

### 8.2 テーマ切り替え

#### 8.2.1 テーマプロバイダー
```typescript
const ThemeProvider: React.FC<ThemeProviderProps> = ({ children }) => {
  const [darkMode, setDarkMode] = useState(false);
  
  const theme = createTheme(darkMode ? darkTheme : lightTheme);
  
  return (
    <MuiThemeProvider theme={theme}>
      <ThemeContext.Provider value={{ darkMode, setDarkMode }}>
        {children}
      </ThemeContext.Provider>
    </MuiThemeProvider>
  );
};
```

## 9. 国際化対応

### 9.1 多言語対応

#### 9.1.1 言語設定
```typescript
const languages = {
  ja: {
    code: 'ja',
    name: '日本語',
    direction: 'ltr',
  },
  en: {
    code: 'en',
    name: 'English',
    direction: 'ltr',
  },
};
```

### 9.2 日付・数値フォーマット

#### 9.2.1 ロケール設定
```typescript
const localeFormats = {
  ja: {
    date: 'YYYY/MM/DD',
    time: 'HH:mm',
    number: '0,0',
  },
  en: {
    date: 'MM/DD/YYYY',
    time: 'h:mm A',
    number: '0,0',
  },
};
```

## 10. テスト戦略

### 10.1 ビジュアルリグレッションテスト

#### 10.1.1 Storybook設定
```typescript
const storybookConfig = {
  stories: ['../src/**/*.stories.@(js|jsx|ts|tsx)'],
  addons: [
    '@storybook/addon-essentials',
    '@storybook/addon-a11y',
    '@storybook/addon-viewport',
  ],
};
```

### 10.2 アクセシビリティテスト

#### 10.2.1 axe-core統合
```typescript
const accessibilityTest = {
  rules: {
    'color-contrast': { enabled: true },
    'keyboard-navigation': { enabled: true },
    'screen-reader': { enabled: true },
  },
};
```

## 11. 変更履歴

| バージョン | 日付 | 変更内容 | 担当者 |
|-----------|------|----------|--------|
| 1.0.0 | 2024-01-01 | 初版作成 | システムエンジニア |

---

**注意事項**:
- デザインシステムは一貫性を保つこと
- アクセシビリティガイドラインに準拠すること
- パフォーマンス要件を満たすこと
- ユーザーテストを定期的に実施すること
