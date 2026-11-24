"""
/core/response_model.py

This module defines the response model for the APIs.
"""

# Importing the necessary modules
from datetime import datetime, timezone
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, TypeVar, Generic
from fastapi.responses import JSONResponse

T = TypeVar('T')

class APIResponse(BaseModel, Generic[T]):
    """
    Provides the individual API response structure.

    Attributes:
        api_status_code (int): The status code of the API response.
        api_status_message (str): The status message of the API response.
        data (Optional[T]): The data of the API response.
    """
    api_status_code: int
    api_status_message: str
    data: Optional[T] = None

class ResponseModel(BaseModel, Generic[T]):
    """
    Provides the server response structure.

    Attributes:
        server_status_code (int): The status code of the server response.
        request_id (str): The request ID of the server response.
        server_timestamp (str): The timestamp of the server response.
        api_url (Optional[str]): The API URL of the server response.
        api_data (APIResponse[T]): The API data of the server response.
    """
    server_status_code: int
    request_id: str
    server_timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    ) 
    api_url: Optional[str] = None
    api_data: APIResponse[T]

    @field_validator('server_timestamp', mode = "before")
    @classmethod
    def validate_server_timestamp(cls, value: datetime | str) -> str:
        if isinstance(value, datetime):
            return value.isoformat()
        return value

    @model_validator(mode = "after")
    def check_status_codes(self):
        if self.server_status_code != self.api_data.api_status_code // 100:
            raise ValueError("Server status code and API status code do not match")
        return self
    
    def to_json_response(self) -> JSONResponse:
        return JSONResponse(
            status_code=self.server_status_code,
            content=self.model_dump(mode = "json")
        )

