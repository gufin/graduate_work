from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    service_api_url = Field(..., env="SERVICE_API_URL")
    db_host = Field(..., env="DB_HOST")
    db_port = Field(..., env="DB_PORT")
    user = Field(..., env="POSTGRES_USER")
    password = Field(..., env="POSTGRES_PASSWORD")
    db = Field(..., env="POSTGRES_DB")

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


test_settings = TestSettings()
