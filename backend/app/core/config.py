# pyrefly: ignore [missing-import]
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):           # creates a configuration object.
    app_name: str = "CareerPilot AI API"
    app_env: str = "development"
    app_debug: bool = True
    # api_host & api_port define the host and port where your API will run.
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    # defines your PostgreSQL database connection details.     
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    # model_config -  loads config values from your .env file.
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

# creates an instance of the Settings class, holding our app’s configuration.   
settings = Settings()