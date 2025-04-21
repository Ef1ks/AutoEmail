from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    email: str
    password: str
    port: int
    serverEmail: str
    dane: str

    class Config:
        env_file = ".env"

settings = Settings()