"""ゲームモデル"""
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import List, Optional


class Frame(BaseModel):
    """フレームモデル"""
    number: int = Field(..., ge=1, le=10)
    rolls: List[int] = Field(default_factory=list)
    score: int = 0
    is_strike: bool = False
    is_spare: bool = False
    is_completed: bool = False


class FrontendFrame(BaseModel):
    """フロントエンド用フレームモデル"""
    frameNumber: int = Field(..., ge=1, le=10)
    firstRoll: Optional[int] = None
    secondRoll: Optional[int] = None
    thirdRoll: Optional[int] = None
    frameScore: Optional[int] = None
    isStrike: bool = False
    isSpare: bool = False
    isCompleted: bool = False


class GameBase(BaseModel):
    """ゲームベースモデル"""
    user_id: str
    total_score: int = 0
    frames: List[Frame] = Field(default_factory=list)
    status: str = "playing"
    played_at: datetime = Field(default_factory=datetime.now)


class GameCreate(GameBase):
    """ゲーム作成モデル"""
    pass


class CompletedGameRequest(BaseModel):
    """完了したゲーム保存リクエスト（フロントエンド用）"""
    gameDate: str
    totalScore: int
    frames: List[FrontendFrame]
    status: str = "completed"


class RollRequest(BaseModel):
    """ロールリクエストモデル"""
    frame_number: int = Field(..., ge=1, le=10)
    pin_count: int = Field(..., ge=0, le=10)
    
    @validator('pin_count')
    def validate_pin_count(cls, v, values):
        frame_number = values.get('frame_number')
        if frame_number < 10 and v > 10:
            raise ValueError('Pin count cannot exceed 10 for frames 1-9')
        return v


class GameResponse(GameBase):
    """ゲームレスポンスモデル"""
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class GameHistoryRequest(BaseModel):
    """ゲーム履歴リクエストモデル"""
    limit: int = Field(20, ge=1, le=100)
    offset: int = Field(0, ge=0)
    status: Optional[str] = Field(None, pattern="^(playing|completed)$")


class GameHistoryResponse(BaseModel):
    """ゲーム履歴レスポンスモデル"""
    games: List[GameResponse]
    total: int
    limit: int
    offset: int


class GameStatistics(BaseModel):
    """ゲーム統計モデル"""
    total_games: int = 0
    completed_games: int = 0
    average_score: float = 0.0
    highest_score: int = 0
    lowest_score: int = 0
    strike_count: int = 0
    spare_count: int = 0
    perfect_games: int = 0
    turkey_count: int = 0


class GameSchema(BaseModel):
    """ゲームスキーマ（データベース用）"""
    id: str
    user_id: str
    total_score: int
    frames: List[Frame]
    status: str
    played_at: datetime
    created_at: datetime
    updated_at: datetime
    expire_at: datetime
