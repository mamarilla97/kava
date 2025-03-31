from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Configuración de la aplicación
    APP_NAME: str = "Mi FastAPI App"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Configuración del servidor
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Versión de la API
    API_V1_STR: str = "/api/v1"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings() 