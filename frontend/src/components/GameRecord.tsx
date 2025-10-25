import { useState, useEffect } from 'react';
import {
  Box,
  Button,
  Typography,
  Card,
  Grid,
  Container,
  Paper,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  CircularProgress,
  Alert
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import SportsIcon from '@mui/icons-material/Sports';
import CheckIcon from '@mui/icons-material/Check';
import NavigateBeforeIcon from '@mui/icons-material/NavigateBefore';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import { auth } from '../firebase/config';
import { gameService } from '../services/gameService';

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

interface Game {
  id: string;
  userId?: string;  // オプショナル: バックエンドで認証トークンから自動設定
  gameDate: string;
  totalScore: number;
  frames: Frame[];
  status: 'in_progress' | 'completed';
}

export default function GameRecord() {
  const navigate = useNavigate();
  const [game, setGame] = useState<Game | null>(null);
  const [currentFrame, setCurrentFrame] = useState<number>(1);
  const [currentRoll, setCurrentRoll] = useState<1 | 2 | 3>(1);
  const [showFinishDialog, setShowFinishDialog] = useState(false);
  const [isGameCompleted, setIsGameCompleted] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [saveError, setSaveError] = useState<string | null>(null);

  // コンポーネントマウント時に自動的にゲームを開始
  useEffect(() => {
    startNewGame();
  }, []);


  const initializeFrames = (): Frame[] => {
    return Array.from({ length: 10 }, (_, index) => ({
      frameNumber: index + 1,
      firstRoll: null,
      secondRoll: null,
      thirdRoll: null,
      frameScore: null,
      isStrike: false,
      isSpare: false,
      isCompleted: false,
    }));
  };

  const startNewGame = () => {
    const newGame: Game = {
      id: `temp_${Date.now()}`,
      gameDate: new Date().toISOString(),
      totalScore: 0,
      frames: initializeFrames(),
      status: 'in_progress',
    };
    setGame(newGame);
    setCurrentFrame(1);
    setCurrentRoll(1);
    setIsGameCompleted(false);
    setSaveError(null);
  };

  const handlePinInput = (pins: number) => {
    if (!game) return;

    const updatedFrames = [...game.frames];
    const frameIndex = currentFrame - 1;
    const frame = updatedFrames[frameIndex];

    if (currentRoll === 1) {
      frame.firstRoll = pins;
      frame.isStrike = pins === 10;
      
      if (frame.isStrike && currentFrame < 10) {
        // ストライクの場合、次のフレームへ
        frame.isCompleted = true;
        setCurrentFrame(currentFrame + 1);
        setCurrentRoll(1);
      } else if (currentFrame === 10) {
        // 10フレーム目の1投目: ストライクでも通常でも2投目へ進む
        setCurrentRoll(2);
      } else {
        setCurrentRoll(2);
      }
    } else if (currentRoll === 2) {
      frame.secondRoll = pins;
      frame.isSpare = (frame.firstRoll || 0) + pins === 10 && !frame.isStrike;
      
      if (currentFrame < 10) {
        frame.isCompleted = true;
        setCurrentFrame(currentFrame + 1);
        setCurrentRoll(1);
      } else {
        // 10フレーム目
        if (frame.isStrike || frame.isSpare) {
          setCurrentRoll(3);
        } else {
          frame.isCompleted = true;
        }
      }
    } else if (currentRoll === 3) {
      frame.thirdRoll = pins;
      frame.isCompleted = true;
    }

    // スコア計算
    calculateTotalScore(updatedFrames);
    
    // // 全フレームのデータ保持状態をconsole.logで出力
    console.log('=== 全フレームデータ ===', updatedFrames);
    
     setGame({
      ...game,
      frames: updatedFrames,
    });
  };


  const calculateTotalScore = (frames: Frame[]): Frame[] => {
    for (let i = 0; i < frames.length; i++) {
      // フレームが完了していない場合はスコアを計算しない
      if (!frames[i].isCompleted) {
        frames[i].frameScore = null;
        continue;
      }

      // Turkey（3連続ストライク）
      if (isTurkey(frames, i)) {
        console.log('Turkey', i);
        frames[i].frameScore = 30 + getLastScore(frames, i);
      }
      // Double（2連続ストライク）
      else if (isDouble(frames, i) && frames[i+1]?.firstRoll !== null && frames[i+1]?.firstRoll! < 10) {
        console.log('Double', i);
        frames[i].frameScore = 20 + (frames[i+1]?.firstRoll || 0) + getLastScore(frames, i);
      }
      // フレーム10 Single Strike + not strike 
      else if (i == 9 && isSingleStrike(frames, i)) {
        console.log('Single Strike + not strike', i);
        frames[i].frameScore = 10 + (frames[i+1]?.firstRoll || 0) + (frames[i+1]?.secondRoll || 0) + getLastScore(frames, i);
      }
      // フレーム9以前 Single Strike + not strike 
      else if (i < 9 && isSingleStrike(frames, i) && frames[(i+1)].isCompleted == true) {
        console.log('Single Strike + not strike', i);
        frames[i].frameScore = 10 + (frames[i+1]?.firstRoll || 0) + (frames[i+1]?.secondRoll || 0) + getLastScore(frames, i);
      }
      // Spare
      else if (isSpare(frames, i) && frames[(i+1)].isCompleted == true) {
        console.log('Spare', i);
        frames[i].frameScore = 10 + (frames[i+1]?.firstRoll || 0) + getLastScore(frames, i);
      }
      // 通常のフレーム（N + M）
      else if (frames[i].isCompleted == true && frames[i].isStrike == false && frames[i].isSpare == false) {
        console.log('通常のフレーム', i);
        frames[i].frameScore = (frames[i].firstRoll || 0) + (frames[i].secondRoll || 0) + getLastScore(frames, i);
      }
      
      console.log('frames', i, frames[i].isCompleted, frames[i].frameScore);
    }
    return frames;
  };

  // getLastScore
  const getLastScore = (frames: Frame[], frameIndex: number): number => {
    if (frameIndex === 0) {
      return 0;
    }
    console.log('getLastScore', frameIndex, frames[(frameIndex - 1)].frameScore);
    return frames[(frameIndex - 1)].frameScore || 0;
  };

  // Turkey（3連続ストライク）の判定（「completed」且つ「isStrike」が3つ連続）
  const isTurkey = (frames: Frame[], frameIndex: number): boolean => {
    if (frameIndex >= 7) {
      // フレーム8以降は3連続ストライク
      if (frameIndex == 7 && frames[7].isStrike == true 
        && frames[8].isStrike == true && frames[9].firstRoll == 10) {
        return true;
      }
      // フレーム9は3連続ストライク
      if (frameIndex == 8 && frames[8].isStrike == true 
        && frames[9].firstRoll == 10 && frames[9].secondRoll == 10) {
        return true;
      }
      // フレーム10は3連続ストライク
      if (frameIndex == 9 && frames[9].firstRoll == 10 
        && frames[9].secondRoll == 10 && frames[9].thirdRoll == 10) {
        return true;
      }
    }
    else if (frames[frameIndex].isCompleted && frames[frameIndex].isStrike == true 
      && frames[(frameIndex+1)].isStrike == true && frames[(frameIndex+1)].isStrike == true
        && frames[(frameIndex+2)].isCompleted == true && frames[(frameIndex+2)].isCompleted == true) {
        return true;
    }
    return false;
  };

  // Double（2連続ストライク）の判定（「completed」且つ「isStrike」が2つ連続）
  const isDouble = (frames: Frame[], frameIndex: number): boolean => {
    // フレーム10の場合
    if (frameIndex == 9 && frames[frameIndex].firstRoll == 10
      && frames[frameIndex].secondRoll == 10 && (frames[frameIndex].thirdRoll ?? 0) < 10) {
        return true;
    }
    // フレーム9の場合
    else if (frameIndex == 8 && frames[frameIndex].isCompleted && frames[frameIndex].isStrike == true
      && frames[(frameIndex+1)].firstRoll == 10 && frames[(frameIndex+1)].secondRoll == 10) {
      return true;
    }
    // フレーム8以前の場合
    else if (frameIndex < 8 && frames[frameIndex].isCompleted && frames[frameIndex].isStrike == true 
      && frames[(frameIndex+1)].isStrike == true && frames[(frameIndex+1)].isCompleted == true) {
      return true;
    }
    return false;
  };

  // Strike + N + M, Strike + Spare
  const isSingleStrike = (frames: Frame[], frameIndex: number): boolean => {
    // フレーム10の場合
    if (frameIndex == 9 && frames[frameIndex].firstRoll == 10
      && (frames[frameIndex].secondRoll ?? 0) < 10 && (frames[frameIndex].thirdRoll ?? 0) < 10) {
        return true;
    }
    // フレーム9以前の場合: 現在のフレームがストライクで、次のフレームがストライクでない
    else if (frameIndex <= 8 && frames[frameIndex].isCompleted && frames[frameIndex].isStrike == true && frames[frameIndex+1].isCompleted == true && frames[frameIndex+1].isStrike == false) {
      return true;
    }
    return false;
  };

  // Spare
  const isSpare = (frames: Frame[], frameIndex: number): boolean => {
    if (frames[frameIndex].isCompleted && frames[frameIndex].isSpare == true) {
      return true;
    }
    return false;
  };

  const canFinishGame = (): boolean => {
    if (!game) return false;
    return game.frames.every(frame => frame.isCompleted);
  };

  const handleFinishGame = async () => {
    if (!game || !canFinishGame()) return;

    // ユーザー認証チェック
    const user = auth.currentUser;
    if (!user) {
      setSaveError('ログインが必要です');
      return;
    }

    setIsSaving(true);
    setSaveError(null);

    try {
      // 最終スコアを計算（最後のフレームのframeScore）
      const lastFrame = game.frames[9];
      const finalTotalScore = lastFrame.frameScore || 0;
      
      // ゲームの状態を完了に変更
      // 注意: userIdはバックエンドで認証トークンから自動的に設定されます
      const completedGame: Game = {
        ...game,
        status: 'completed',
        totalScore: finalTotalScore,
      };

      console.log('💾 ゲーム保存リクエスト:', {
        gameDate: completedGame.gameDate,
        totalScore: completedGame.totalScore,
        frames: completedGame.frames.length,
        status: completedGame.status
      });

      // バックエンドにゲームデータを保存
      const savedGame = await gameService.saveGame(completedGame);
      
      console.log('✅ ゲームが保存されました:', savedGame);

      // 状態を更新
      setGame(savedGame);
      setIsGameCompleted(true);
      setShowFinishDialog(true);
    } catch (error: any) {
      console.error('❌ ゲーム保存エラー:', error);
      console.error('エラー詳細:', error.response?.data || error.message);
      setSaveError(error.message || 'ゲームの保存に失敗しました');
    } finally {
      setIsSaving(false);
    }
  };

  const getMaxPins = (): number => {
    if (!game) return 10;
    
    const frame = game.frames[currentFrame - 1];
    
    if (currentFrame < 10) {
      // 1-9フレーム目
      if (currentRoll === 1) {
        return 10;
      } else if (currentRoll === 2) {
        return 10 - (frame.firstRoll || 0);
      }
    } else {
      // 10フレーム目
      if (currentRoll === 1) {
        return 10;
      } else if (currentRoll === 2) {
        // 1投目がストライクの場合、2投目は0から10が選べる
        if (frame.firstRoll === 10) {
          return 10;
        }
        // 通常の場合は1投目の残りピン数まで
        const maxPins = 10 - (frame.firstRoll || 0);
        console.log(`10フレーム目2投目: 1投目=${frame.firstRoll}, 最大ピン数=${maxPins}`);
        return maxPins;
      } else if (currentRoll === 3) {
        // 1投目がストライクの場合
        if (frame.firstRoll === 10) {
          // 2投目がストライク（10）の場合、3投目は0から10が選べる
          if (frame.secondRoll === 10) {
            console.log('10フレーム目3投目: 1投目=X, 2投目=X → 最大ピン数=10');
            return 10;
          }
          // 2投目が0から9の場合、3投目は0から（10 - 2投目得点）が選べる
          else if (frame.secondRoll !== null && frame.secondRoll < 10) {
            const maxPins = 10 - frame.secondRoll;
            console.log(`10フレーム目3投目: 1投目=X, 2投目=${frame.secondRoll} → 最大ピン数=${maxPins}`);
            return maxPins;
          }
        }
        // 1投目がストライク以外で2投目でスペアの場合、3投目は0から10が選べる
        else if (frame.isSpare) {
          console.log(`10フレーム目3投目: 1投目=${frame.firstRoll}, 2投目でスペア → 最大ピン数=10`);
          return 10;
        }
        // その他の場合（想定外のケース）
        console.log('10フレーム目3投目: 想定外のケース → 最大ピン数=10');
        return 10;
      }
    }
    
    return 10;
  };

  // フレーム表示用のスコアフォーマット
  const formatFrameDisplay = (frame: Frame): string => {
    if (frame.frameNumber < 10) {
      // 1-9フレーム目
      if (frame.firstRoll === null) {
        return ''; // 未入力の場合は空文字を返す
      }
      
      const first = frame.firstRoll === 0 ? 'G' : (frame.firstRoll === 10 ? 'X' : frame.firstRoll);
      const second = frame.secondRoll === 0 ? '-' : (frame.secondRoll !== null ? frame.secondRoll : '');
      
      if (frame.isStrike) {
        return 'X';
      } else if (frame.isSpare) {
        return `${first} /`;
      } else {
        return `${first} ${second}`;
      }
    } else {
      // 10フレーム目
      if (frame.firstRoll === null) {
        return ''; // 未入力の場合は空文字を返す
      }
      
      const first = frame.firstRoll === 0 ? 'G' : (frame.firstRoll === 10 ? 'X' : frame.firstRoll);
      const second = frame.secondRoll === 0 ? '-' : (frame.secondRoll === 10 ? 'X' : frame.secondRoll);
      const third = frame.thirdRoll === 0 ? '-' : (frame.thirdRoll === 10 ? 'X' : frame.thirdRoll);
      
      let result: string = String(first);
      if (frame.secondRoll !== null) {
        if (frame.isStrike && frame.secondRoll === 10) {
          result += 'X';
        } else if (frame.isSpare) {
          result += ' /';
        } else {
          result += ' ';
          result += String(second);
        }
      }
        if (frame.thirdRoll !== null) {
          if (frame.thirdRoll === 10) {
            result += 'X';
          } else {
            // 1投目がストライクの場合且つ、2投目は0から9の場合：
            // 3投目の得点が2投目と3投目で合計10点の場合は「/」とする
            if (frame.firstRoll === 10 && frame.secondRoll !== null && frame.secondRoll < 10) {
              const secondAndThirdTotal = (frame.secondRoll || 0) + (frame.thirdRoll || 0);
              if (secondAndThirdTotal === 10) {
                result += ' /';
              } else {
                result += ' ' + String(third);
              }
            } else {
              result += ' ' + String(third);
            }
          }
        }
      return result;
    }
  };

  // 進むボタンの表示条件チェック
  const canShowNextButton = (): boolean => {
    if (!game) return false;
    
    // フレーム番号が1から9の時に表示
    if (currentFrame < 1 || currentFrame > 9) {
      return false;
    }
    
    const currentFrameData = game.frames[currentFrame - 1];
    
    // 現在のフレームにスコアが2投分または10点であれば表示
    const hasTwoRolls = currentFrameData.firstRoll !== null && currentFrameData.secondRoll !== null;
    const hasStrike = currentFrameData.firstRoll === 10;
    
    return hasTwoRolls || hasStrike;
  };


  if (!game) {
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
          
          <Paper sx={{ p: 4, textAlign: 'center' }}>
            <SportsIcon sx={{ fontSize: 64, color: 'primary.main', mb: 2 }} />
            <Typography variant="h5" gutterBottom>
              新しいゲームを開始
            </Typography>
            <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
              ボーリングゲームのスコアを記録しましょう
            </Typography>
            <Button
              variant="contained"
              size="large"
              startIcon={<SportsIcon />}
              onClick={startNewGame}
            >
              ゲーム開始
            </Button>
          </Paper>
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

        {/* ゲームヘッダー */}
        <Paper sx={{ p: 3, mb: 3 }}>
          <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 3 }}>
            <Typography variant="h4" color="primary" fontWeight="bold">
              フレーム
            </Typography>
            
            {/* フレームナビゲーション */}
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              {currentFrame > 1 && (
                <Button
                  variant="outlined"
                  onClick={() => {
                    setCurrentFrame(currentFrame - 1);
                    setCurrentRoll(1);
                  }}
                  startIcon={<NavigateBeforeIcon />}
                >
                  前へ
                </Button>
              )}
              
              <Typography variant="h6" color="text.secondary">
                {currentFrame}
              </Typography>
              
              {canShowNextButton() && (
                <Button
                  variant="outlined"
                  onClick={() => {
                    setCurrentFrame(currentFrame + 1);
                    setCurrentRoll(1);
                  }}
                  endIcon={<NavigateNextIcon />}
                >
                  次へ
                </Button>
              )}
            </Box>
          </Box>
        </Paper>

        {/* スコア入力セクション */}
        {!isGameCompleted && (
          <Paper sx={{ p: 3, mb: 3 }}>
            <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 3 }}>
              <Typography variant="h5" gutterBottom>
                投球 {currentRoll}
              </Typography>
              
              <Typography variant="body1" color="text.secondary" sx={{ textAlign: 'center' }}>
                倒したピン数を選択してください
              </Typography>
              
              <Grid container spacing={2} justifyContent="center" sx={{ maxWidth: '400px' }}>
                {Array.from({ length: getMaxPins() + 1 }, (_, i) => (
                  <Grid item key={i}>
                    <Button
                      variant="outlined"
                      size="large"
                      onClick={() => handlePinInput(i)}
                      sx={{ 
                        minWidth: '60px', 
                        height: '60px',
                        fontSize: '1.2rem',
                        fontWeight: 'bold'
                      }}
                    >
                      {i}
                    </Button>
                  </Grid>
                ))}
              </Grid>
            </Box>
          </Paper>
        )}

        {/* ゲーム完了メッセージ */}
        {isGameCompleted && (
          <Paper sx={{ p: 3, mb: 3, textAlign: 'center', backgroundColor: 'success.light' }}>
            <Typography variant="h5" color="success.dark" gutterBottom>
              ゲーム完了！
            </Typography>
            <Typography variant="body1" color="text.secondary">
              お疲れ様でした。最終スコア: {game?.totalScore}点
            </Typography>
          </Paper>
        )}

        {/* スコアボード */}
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom sx={{ textAlign: 'center' }}>
            スコアボード
          </Typography>
          
          <Grid container spacing={1} justifyContent="center">
            {game.frames.map((frame) => (
              <Grid item key={frame.frameNumber}>
                <Card 
                  sx={{ 
                    p: 1, 
                    textAlign: 'center', 
                    minWidth: '80px',
                    border: currentFrame === frame.frameNumber ? 2 : 1,
                    borderColor: currentFrame === frame.frameNumber ? 'primary.main' : 'divider'
                  }}
                >
                  <Typography variant="caption" color="text.secondary">
                    {frame.frameNumber}
                  </Typography>
                  
                  <Box sx={{ display: 'flex', justifyContent: 'center', mb: 0.5, minHeight: 20 }}>
                    <Typography variant="body2" sx={{ fontSize: '0.8rem', fontWeight: 'bold' }}>
                      {formatFrameDisplay(frame)}
                    </Typography>
                  </Box>
                  
                  <Typography variant="body2" fontWeight="bold">
                    {(() => {
                      // completeフラグがfalseならスコア表示をしない
                      if (!frame.isCompleted) {
                        return '';
                      }
                      
                      // frameScoreがnullまたはundefinedの場合は何も表示しない
                      if (frame.frameScore === null || frame.frameScore === undefined) {
                        return '';
                      }
                      
                      return frame.frameScore;
                    })()}
                  </Typography>
                </Card>
              </Grid>
            ))}
          </Grid>
          
          <Box sx={{ textAlign: 'center', mt: 2 }}>
            <Typography variant="h5" color="primary">
              合計スコア: {game.frames[9]?.frameScore || 0}
            </Typography>
          </Box>
        </Paper>



        {/* エラーメッセージ */}
        {saveError && (
          <Box sx={{ mb: 3 }}>
            <Alert severity="error" onClose={() => setSaveError(null)}>
              {saveError}
            </Alert>
          </Box>
        )}

        {/* ゲームコントロール */}
        {!isGameCompleted && (
          <Box sx={{ display: 'flex', justifyContent: 'center', gap: 2 }}>
            <Button
              variant="contained"
              color="success"
              startIcon={isSaving ? <CircularProgress size={20} color="inherit" /> : <CheckIcon />}
              onClick={handleFinishGame}
              disabled={!canFinishGame() || isSaving}
              size="large"
            >
              {isSaving ? '保存中...' : 'ゲーム終了'}
            </Button>
          </Box>
        )}

        {/* ゲーム終了ダイアログ */}
        <Dialog open={showFinishDialog} onClose={() => setShowFinishDialog(false)}>
          <DialogTitle>ゲーム完了</DialogTitle>
          <DialogContent>
            <Typography variant="h6" gutterBottom>
              お疲れ様でした！
            </Typography>
            <Typography variant="body1" sx={{ mb: 2 }}>
              最終スコア: <strong>{game?.totalScore}点</strong>
            </Typography>
            <Alert severity="success">
              ゲームデータがFirebaseに保存されました
            </Alert>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => {
              setShowFinishDialog(false);
              navigate('/');
            }}>
              ダッシュボードへ
            </Button>
            <Button 
              variant="contained" 
              onClick={() => navigate('/history')}
            >
              履歴を見る
            </Button>
          </DialogActions>
        </Dialog>
      </Box>
    </Container>
  );
}
