"""
/permissions/schema/response.py 

Provides the response model for the schema to be returned to the user.
"""
# Importing the necessary modules
from datetime import datetime 
from pydantic import BaseModel 
from typing import Optional

class PermissionsResponse(BaseModel):
    """
    
    """
    permission_id: int 
    permission_name: str 
    permission_description: str 
    created_at: datetime
    created_by: int 
    updated_at: Optional[datetime]
    updated_by: Optional[int]

    class Config:
        from_attributes = True