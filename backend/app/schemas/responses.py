from typing import Any, Dict, Generic, List, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PaginationMeta(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int


class PaginatedResponse(BaseModel, Generic[T]):
    success: bool = True
    data: List[T]
    meta: PaginationMeta
    error: Optional[Dict[str, Any]] = None


class SingleResponse(BaseModel, Generic[T]):
    success: bool = True
    data: T
    error: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseModel):
    success: bool = False
    data: Optional[Any] = None
    error: Dict[str, Any]
