from pydantic import BaseSettings, Field


class KafkaSettings(BaseSettings):
    host: str = Field(..., env='KAFKA_BROKER_HOST')
    port: int = Field(..., env='KAFKA_BROKER_PORT')
    auto_offset_reset: str = Field(..., env='KAFKA_BROKER_AUTO_OFFSET_RESET')
    group_id: str = Field(..., env='KAFKA_BROKER_GROUP_ID')

    class Config:
        env_file = '.env.example', '.env'
        env_file_encoding = 'utf-8'


class PostgresDsl(BaseSettings):
    dbname: str = Field(..., env='PROFILE_DB_NAME')
    user: str = Field(..., env='PROFILE_DB_USER')
    password: str = Field(..., env='PROFILE_DB_PASSWORD')
    host: str = Field(..., env='PROFILE_DB_HOST')
    port: str = Field(..., env='PROFILE_DB_PORT')

    class Config:
        env_file = '.env.example', '.env'
        env_file_encoding = 'utf-8'


class Settings(BaseSettings):
    project_name: str = Field(..., env='PROFILE_APP_PROJECT_NAME')
    postgres_url: str = Field(..., env='PROFILE_DB_URL')
    storage_url: str = Field(..., env='STORAGE_URL')
    postgres_dsl: PostgresDsl = PostgresDsl()
    schema_name: str = Field(..., env='PROFILE_DB_SCHEMA_NAME')
    kafka_settings: KafkaSettings = KafkaSettings()
    integration_off: str

    class Config:
        env_file = '.env.example', '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
