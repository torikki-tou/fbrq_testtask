from pydantic import BaseSettings


class Settings(BaseSettings):
    MONGO_CONNECTION_STRING: str
    CELERY_BROKER_CON_STRING: str
    PROBE_SERVICE_JWT: str


settings = Settings()
