from pydantic import BaseSettings


class DatabaseSettings(BaseSettings):
    host: str = "localhost:5432"
    user: str = "username"
    password: str = "password"
    db_name: str = "database"
    test_db_name: str = "databasefortest"
    debug: bool = True

    @property
    def url(self):
        return f"postgresql+psycopg://{self.user}:{self.password}@{self.host}/{self.db_name}"

    @property
    def test_url(self):
        return f"postgresql+psycopg://{self.user}:{self.password}@{self.host}/{self.test_db_name}"

    class Config:
        env_prefix = "db_"
