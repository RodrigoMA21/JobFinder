from typing import Any, Dict, Optional

from pydantic import BaseModel


class StandardResponse(BaseModel):
    success: bool = True
    data: Any = None
    error: Optional[Dict[str, Any]] = None
