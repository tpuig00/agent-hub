from sqlalchemy.ext.asyncio import create_async_engine

from app.config import settings

# Crea el pool de conexiones. No conecta todavía: la primera consulta es la que abre la conexión.
engine = create_async_engine(settings.database_url)
