from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    service_api_url = Field(..., env="PROFILE_SERVICE_API_URL")
    db_host = Field(..., env="PROFILE_DB_HOST")
    db_port = Field(..., env="PROFILE_DB_PORT")
    user = Field(..., env="PROFILE_DB_USER")
    password = Field(..., env="PROFILE_DB_PASSWORD")
    db = Field(..., env="PROFILE_DB_NAME")

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


test_settings = TestSettings()
