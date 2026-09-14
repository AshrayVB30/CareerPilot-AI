# Configuration variables for the application.
# pyrefly: ignore [missing-import]
from pydantic_settings import BaseSettings, SettingsConfigDict

# creates a settings object that loads values from .env file.
class Settings(BaseSettings):
    # general application settings.
    app_name: str = "CareerPilot AI API"
    app_env: str = "development"
    app_debug: bool = True
    # api_host and api_port define where the API will run.
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    # database connection details.
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    # JWT secret key, algorithm, and token expiration time.
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    # model config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

# creates an instance of the Settings class, holding our app's configuration.
settings = Settings()