from pydantic import BaseSettings


class Settings(BaseSettings):
    MONGO_CONNECTION_STRING: str


settings = Settings()
