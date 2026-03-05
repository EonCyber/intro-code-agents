import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    db_url: str
    nats_url: str
    log_level: str


def load_settings() -> Settings:
    return Settings(
        db_url=os.getenv("DB_URL", "sqlite+aiosqlite:///./prompts.db"),
        nats_url=os.getenv("NATS_URL", "nats://localhost:4222"),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
    )
