import os
from typing import List

class Settings:
    PROJECT_NAME: str = "NetCoop AI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "netcoop-super-secret-jwt-key-2026-campus-mesh")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 # 24 hours
    
    # SQLite Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        f"sqlite:///{os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'netcoop.db'))}"
    )
    
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"
    ]
    
    # ML Artifacts directory
    ARTIFACTS_DIR: str = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "ml", "artifacts")
    )

settings = Settings()
