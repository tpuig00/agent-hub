from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración de la app. Lee las variables de entorno (y del .env si existe)."""

    model_config = SettingsConfigDict(env_file=".env")

    # Sin valor por defecto: si falta en el entorno, la app no arranca
    openai_api_key: str
    openai_vector_store_id: str

    # Con valor por defecto: no es secreto y hay una opción razonable; el .env puede sobrescribirlo
    agent_model: str = "gpt-4o-mini"
    log_level: str = "INFO"


settings = Settings()
