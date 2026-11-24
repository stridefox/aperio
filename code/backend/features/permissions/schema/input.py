"""
/permissions/schema/input.py

Provides schema to validate the inputs provided by the user.
"""
# Importing the necessary modules 
from pydantic import BaseModel, Field, ConfigDict

class Permissions(BaseModel):
    permission_name: str = Field (
        max_length = 30,
        description = "Provides the name of a specific permission."
    )
    permission_description: str = Field (
        min_length = 10,
        max_length = 200, 
        description = "Provides the intent of the permission."
    )
