from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_TESTS_USER: str
    POSTGRES_TESTS_PASSWORD: str
    POSTGRES_TESTS_HOST: str
    POSTGRES_TESTS_PORT: int
    POSTGRES_TESTS_DB: str
    TRONGRID_TOKEN: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
