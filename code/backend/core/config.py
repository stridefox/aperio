# core/config.py
# Application settings and environment variable configuration (Pydantic BaseSettings).
# Status: placeholder - not implemented yet.

# Importing the necessary modules 
from pydantic_settings import BaseSettings, SettingsConfigDict

class DatabaseConnectionSettings(BaseSettings):
    """
    Provides database connection settings from environment variables.

    Attributes:
        DB_HOST (str): Database host
        DB_PORT (int): Database port
        DB_USER (str): Database user
        DB_PASSWORD (str): Database password
        DB_NAME (str): Database name
    """
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra = "ignore"
    )

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

class SecuritySettings(BaseSettings):
    """
    Provides security settings from environment variables.
    
    Attributes:
        JWT_SECRET_KEY (str): Secret key for JWT
        JWT_ALGORITHM (str): Algorithm for JWT
        JWT_EXPIRY_TIME (int): Expiry time for JWT in seconds
    """
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra = "ignore"
    )
    
    JWT_SECRET_KEY: str 
    JWT_ALGORITHM: str
    JWT_EXPIRY_TIME: int



    
    