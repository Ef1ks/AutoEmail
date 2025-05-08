from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    email: str
    password: str
    port: int
    serverEmail: str
    dane: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    db_username: str
    db_password: str
    db_hostname: str
    db_port: int
    db_name: str

    class Config:
        env_file = ".env"

settings = Settings()