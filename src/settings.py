from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, validator

class Settings(BaseSettings):
    API_STR: str = "/api"
    SERVER_NAME: str
    SERVER_HOST: AnyHttpUrl
    CONNECTION_URI: AnyHttpUrl
    API_KEY: str
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = [
        "http://localhost:8000",
        "https://auth.kongsgaard.eu",
        "https://okobau.kongsgaard.eu",
        "https://stage.okobau.kongsgaard.eu",
    ]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        case_sensitive = True


settings = Settings()
