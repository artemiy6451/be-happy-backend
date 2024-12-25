from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    token: str = ""

    db_host: str = ""
    db_port: str = ""
    db_name: str = ""
    db_user: str = ""
    db_pass: str = ""

    @property
    def database_uri(self):
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@"
            f"{self.db_host}:{self.db_port}/{self.db_name}"
        )
