from random import random

from sqlalchemy import create_engine
from contextlib import contextmanager
import pandas as pd
import json
import os

import re

from sqlalchemy import text
from datetime import datetime, timedelta, date

from brandon_sqlalchemy.config.config_loader import ConfigLoader


class DbConnector:
    def __init__(self, filename):
        # init var
        self.filename = filename
        self.config = None
        self.engine = None
        self.db_config = ConfigLoader(filename).stock_db_config

        # set config
        self.set_engine()

    def get_config(self, k=None):
        if k is None:
            return self.config
        else:
            return self.config[k]

    def set_engine(self):
        # sqlalchemy 설정
        self.engine = create_engine(
            f'mysql+mysqldb://{self.db_config["username"]}:{self.db_config["password"]}@{self.db_config["url"]}'
            f':{self.db_config["port"]}'
            f'/{self.db_config["schema"]}'
            f'?autocommit=true', pool_size=100, pool_recycle=600, max_overflow=200)
    def get_conn(self):
        return self.engine.connect()


class DbManager:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        cls = type(self)
        if not hasattr(cls, "_init"):
            self.db_dict = {'galaxynet': DbConnector('local.yaml')}
            self.default_db = 'galaxynet'

            # set init flag
            cls._init = True

    def get_config(self, db_key=None, k=None):
        if db_key is None:
            db_key = self.default_db
        return self.db_dict[db_key].get_config(k)

    def get_conn(self, db_key=None):
        if db_key is None:
            db_key = self.default_db
        return self.db_dict[db_key].get_conn()

    @contextmanager
    def conn_context(self, db_key=None):
        if db_key is None:
            db_key = self.default_db
        conn = self.get_conn(db_key)
        trans = conn.begin()
        try:
            yield conn
            trans.commit()
        except Exception as e:
            trans.rollback()
            raise e
        finally:
            conn.close()


def exec_query(sql, cursor='norm'):

    with DbManager().conn_context() as conn:
        sql = sql

        if cursor == 'norm':
            if any([sql.lower().startswith(v) for v in ['delete', 'replace', 'update', 'alter', 'create']]):
                result = conn.execute(text(sql))
            else:
                # convert into tuple
                result = pd.read_sql(text(sql), conn)

                if result.shape[0] == 1:
                    result = result.iloc[0, 0]
                    result = (result,)
                    result = (result,)
                elif result.shape[0] > 1:
                    result = result

        elif cursor == 'dict':
            result = pd.read_sql(text(sql), conn)

    return result



def insert_data(data, table_name):

    # insert dataframe
    _data = data

    # 테이블명, 스키마명이 동시에 입력될 경우, 테이블명을 따로 분리하여 table_name에 저장
    if re.search(r"\.", table_name) is not None:
        table_name_list = re.split(r"\.\s*", table_name)
        last_idx = len(table_name_list)-1

        schema_name = table_name_list[0]
        table_name = table_name_list[last_idx]
    else:
        schema_name = 'stock_db'

    with DbManager().conn_context() as conn:
        # 1) 임시테이블 생성 후 저장
        tmp_table_name = f'tmp_table_{datetime.now().strftime("%Y%m%d_%H%M%S_%f")}_{int(random() * 1000000)}'
        _data.to_sql(name=tmp_table_name,
                     schema='stock_db',
                     con=conn,
                     if_exists='append',
                     index=False)

        # 2) Replace Into 구문 실행(tmp_table => target_table)
        conn.execute(text(f'replace into {schema_name}.{table_name} select * from {schema_name}.{tmp_table_name}'))

        # 3) tmp 테이블 삭제
        conn.execute(text(f'drop table {schema_name}.{tmp_table_name}'))