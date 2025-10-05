"""ユーザーモデル"""
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    """ユーザーベースモデル"""
    email: EmailStr
    display_name: str = Field(..., min_length=1, max_length=50)
    photo_url: Optional[str] = None


class UserCreate(UserBase):
    """ユーザー作成モデル"""
    uid: str = Field(..., min_length=1)


class UserUpdate(BaseModel):
    """ユーザー更新モデル"""
    display_name: Optional[str] = Field(None, min_length=1, max_length=50)
    photo_url: Optional[str] = None


class UserResponse(UserBase):
    """ユーザーレスポンスモデル"""
    id: str
    uid: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserSchema(BaseModel):
    """ユーザースキーマ（データベース用）"""
    id: str
    uid: str
    email: str
    display_name: str
    photo_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
