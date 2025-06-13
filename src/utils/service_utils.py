from enum import Enum, auto
from typing import Optional, Generic, TypeVar

T = TypeVar("T")


class ServiceError(Enum):
    NOT_FOUND = auto()
    ALREADY_EXISTS = auto()
    INVALID_INPUT = auto()
    DEPENDENCY_ERROR = auto()
    INTERNAL_ERROR = auto()


class ServiceResult(Generic[T]):
    def __init__(
        self,
        success: bool,
        data: Optional[T] = None,
        error_type: Optional[ServiceError] = None,
        message: Optional[str] = None,
    ):
        self.success = success
        self.data = data
        self.error_type = error_type
        self.message = message

    def __repr__(self):
        if self.success:
            return f"[ServiceResult: Success, Data: {self.data}]"
        return f"[ServiceResult: Failure, Error: {self.error_type}, Message: {self.message}]"
