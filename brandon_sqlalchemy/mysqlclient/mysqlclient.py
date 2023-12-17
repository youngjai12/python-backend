import os
import json
from contextlib import contextmanager
from sqlalchemy import create_engine
import pandas as pd
from sqlalchemy import text
from pathlib import Path

from brandon_sqlalchemy.config.config_loader import ConfigLoader


class DbConnection:
    _instance = None

    def _make_engine(self):
        return create_engine(
            f'mysql+mysqldb://{self.db_config["username"]}:{self.db_config["password"]}@{self.db_config["url"]}'
            f':{self.db_config["port"]}'
            f'/{self.db_config["schema"]}'
            f'?autocommit=true', pool_size=100, pool_recycle=600, max_overflow=200)
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, filename):
        self.db_config = ConfigLoader(filename).stock_db_config
        self.db_engine = self._make_engine()
        self.get_conn = self.db_engine.connect()


class SessionProcessor:

    def __init__(self, filename):
        self.dbConnection = DbConnection(filename).get_conn

    @contextmanager
    def conn_context(self):

        trans = self.dbConnection.begin()
        try:
            yield self.dbConnection
            trans.commit()
        except Exception as e:
            trans.rollback()
            raise e
        finally:
            self.dbConnection.close()



