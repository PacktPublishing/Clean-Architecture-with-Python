# order_system/config.py
import os
from pathlib import Path


class Config:
    # Application
    APP_NAME = "Order Processing System"

    # Database
    DB_PATH = os.getenv("DB_PATH", "order_system.db")

    # Feature Flags
    USE_CLEAN_ARCHITECTURE = os.getenv("USE_CLEAN_ARCHITECTURE", "True").lower() in (
        "true",
        "1",
        "yes",
    )
