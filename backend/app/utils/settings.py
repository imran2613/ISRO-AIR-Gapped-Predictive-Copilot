from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ISRO MPLS Predictive Copilot"
    app_env: str = "local"
    database_url: str = "sqlite:///./mpls_ops.db"
    ai_provider: str = "offline"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-1.5-flash"
    cors_origins: list[str] | str = ["http://localhost:5173", "http://127.0.0.1:5173"]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: object) -> object:
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value


settings = Settings()
