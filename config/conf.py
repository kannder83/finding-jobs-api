from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: int
    database_password: str
    database_name: str
    database_username: str
    debug: bool
    allowed_hosts: str
    prod_port: int
    prod_url: str
    version: str

    class Config:
        env_file = ".env"


settings = Settings()
