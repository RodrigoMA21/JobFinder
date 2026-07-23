from typing import Any, Optional


class AppException(Exception):
    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: str = "GENERIC_ERROR",
        data: Optional[Any] = None,
    ):
        self.status_code = status_code
        self.detail = detail
        self.error_code = error_code
        self.data = data


class NotFoundException(AppException):
    def __init__(self, entity: str, entity_id: str):
        super().__init__(
            status_code=404,
            detail=f"{entity} with id '{entity_id}' not found",
            error_code="NOT_FOUND",
        )


class ValidationException(AppException):
    def __init__(self, detail: str, data: Optional[Any] = None):
        super().__init__(
            status_code=422,
            detail=detail,
            error_code="VALIDATION_ERROR",
            data=data,
        )


class ExternalAPIException(AppException):
    def __init__(self, source: str, detail: str):
        super().__init__(
            status_code=502,
            detail=f"External API '{source}' error: {detail}",
            error_code="EXTERNAL_API_ERROR",
        )
