from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import insert
from backend.db_manager.models import Vacancy, Resume, Base, Task, Entity
import os
from typing import List, Dict
from backend.config.config_reader import config_reader
from backend.config.data_models import DatabaseConfig
from datetime import datetime
from backend.custom_logger import logger
from sqlalchemy import create_engine, MetaData, Table, text, insert
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
import psycopg2
from typing import List, Dict, Any, Iterator
from itertools import islice


_db_cfg = config_reader.get(DatabaseConfig)
DATABASE_URL = _db_cfg.url

engine = create_async_engine(DATABASE_URL, echo=_db_cfg.echo)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

class Repository:
    def __init__(self, config: DatabaseConfig = None):
        if config is None:
            config = config_reader.get(DatabaseConfig)
        self.db_user = config.user
        self.db_pwd = config.password
        self.host = config.host
        self.port = config.port
        self.database = config.dbname
        self.pool_size = config.pool_size
        self.pool_size_overflow = config.pool_size_overflow
        self._engine = None
        self._session = None

    def connect(self):
        self._engine = create_engine(
            'postgresql+psycopg2://',
            creator=lambda: psycopg2.connect(
                user=self.db_user,
                password=self.db_pwd,
                host=self.host,
                port=self.port,
                database=self.database
            ),
            poolclass=QueuePool,
            pool_size=self.pool_size,
            max_overflow=self.pool_size_overflow
        )
        self._session = sessionmaker(bind=self._engine, expire_on_commit=False)

        with self.get_session() as session:
            session.execute(text('SELECT 1'))

    @contextmanager
    def get_session(self):
        session = self._session()
        try:
            yield session
        except Exception as err:
            session.rollback()
            raise
        finally:
            session.close()

    def insert_into_table(self, entity: Entity, records: List[Dict[str, Any]]):
        """Insert records into the specified table."""
        with self.get_session() as session:
            metadata = MetaData(schema='public')
            table = Table(entity.value, metadata, autoload_with=self._engine)

            if records:
                session.execute(insert(table), records)
                session.commit()

    def batch_insert(self, entity: Entity, data_iterator: Iterator[Dict[str, Any]], batch_size: int = 1000):
        """Insert records in batches from an iterator."""
        while True:
            batch = list(islice(data_iterator, batch_size))
            if not batch:
                break
            self.insert_into_table(entity, batch)

    def select_from_table(self, entity: Entity, where: str) -> List[Dict[str, Any]]:
        """Select records from the specified table."""
        with self.get_session() as session:
            query = text(f"SELECT * FROM {entity.value} WHERE {where}")
            result = session.execute(query)
            return [dict(row) for row in result]

    def delete_from_table(self, entity: Entity, where: str):
        """Delete records from the specified table."""
        with self.get_session() as session:
            query = text(f"DELETE FROM {entity.value} WHERE {where}")
            session.execute(query)
            session.commit()

    def json_to_dataclass_iterator(self, json_array: List[Dict[str, Any]]) -> Iterator[Task]:
        """Convert a JSON array to an iterator of Task dataclass instances."""
        for item in json_array:
            yield Task(
                service_id=item["service_id"],
                request_id=item["request_id"],
                flag=item["data"]["flag"],
                count=item["data"].get("count"),
                is_dev=item["data"].get("is_dev")
            )
