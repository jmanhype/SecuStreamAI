import sys
import os
from pathlib import Path
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Add the project root directory to sys.path to allow imports from src
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from src.models.db_models import Base  # Import your models
from src.core.config import settings  # Import settings

# this is the Alembic Config object, which provides access to values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# Ensure required environment variables are set via Settings
assert settings.OPENAI_API_KEY is not None, "OPENAI_API_KEY is not set"
assert settings.SECRET_KEY is not None, "SECRET_KEY is not set"
assert settings.POSTGRES_PASSWORD is not None, "POSTGRES_PASSWORD is not set"

# Set sqlalchemy.url from settings
config.set_main_option('sqlalchemy.url', settings.SQLALCHEMY_DATABASE_URL)

target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

# Debug prints to verify environment variables are loaded
print("Environment Variables Loaded in Alembic:")
print(f"OPENAI_API_KEY: {'Loaded' if settings.OPENAI_API_KEY else 'Not Loaded'}")
print(f"SECRET_KEY: {'Loaded' if settings.SECRET_KEY else 'Not Loaded'}")
print(f"POSTGRES_PASSWORD: {'Loaded' if settings.POSTGRES_PASSWORD else 'Not Loaded'}")