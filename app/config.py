from pydantic import BaseSettings


class Settings(BaseSettings):
    database_host: str
    database_port: str
    database_name: str
    database_username: str
    database_password: str
    secret_key: str
    algoritham: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()
