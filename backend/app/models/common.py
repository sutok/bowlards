"""共通モデル"""
from pydantic import BaseModel
from typing import Any, Optional, Dict
from datetime import datetime


class APIResponse(BaseModel):
    """API共通レスポンス形式"""
    success: bool
    data: Optional[Any] = None
    error: Optional[Dict[str, str]] = None
    meta: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseModel):
    """エラーレスポンス"""
    success: bool = False
    error: Dict[str, str]


class MetaInfo(BaseModel):
    """メタ情報"""
    total: int
    limit: int
    offset: int


def success_response(data: Any = None, meta: Optional[Any] = None) -> Dict[str, Any]:
    """成功レスポンスを作成
    
    Args:
        data: レスポンスデータ
        meta: メタ情報（MetaInfoオブジェクトまたは辞書）
    """
    # metaが辞書かMetaInfoオブジェクトか判定
    meta_dict = None
    if meta is not None:
        if isinstance(meta, dict):
            meta_dict = meta
        elif hasattr(meta, 'dict'):
            meta_dict = meta.dict()
        else:
            meta_dict = meta
    
    response = APIResponse(success=True, data=data, meta=meta_dict)
    return response.dict(exclude_none=True)


def error_response(code: str, message: str) -> Dict[str, Any]:
    """エラーレスポンスを作成"""
    response = ErrorResponse(
        success=False,
        error={"code": code, "message": message}
    )
    return response.dict()


def success_response_with_meta(data: Any, meta: Any) -> Dict[str, Any]:
    """メタ情報付き成功レスポンスを作成
    
    Args:
        data: レスポンスデータ
        meta: メタ情報（MetaInfoオブジェクトまたは辞書）
    """
    # metaが辞書かMetaInfoオブジェクトか判定
    meta_dict = meta.dict() if hasattr(meta, 'dict') else meta
    response = APIResponse(success=True, data=data, meta=meta_dict)
    return response.dict(exclude_none=True)
