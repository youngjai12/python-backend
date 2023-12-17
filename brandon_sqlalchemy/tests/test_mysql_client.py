from brandon_sqlalchemy.config.config_loader import ConfigLoader
from brandon_sqlalchemy.mysqlclient.asis_mysqlclient import DbManager
from brandon_sqlalchemy.mysqlclient.mysqlclient import DbConnection, SessionProcessor
import time

def test_config_path():
    config_loader = ConfigLoader("local.yaml")
    db_config = config_loader.stock_db_config
    print(db_config)


def test_sql_engine_uniq():
    connection1 = DbConnection("local.yaml")
    connection2 = DbConnection("local.yaml")

    print(f"conn 1 {connection1} \n")
    print(f"conn 2 {connection2} \n")

def test_conn_same():
    session_processor = SessionProcessor("local.yaml")
    with session_processor.conn_context() as conn:
        print(f"## conn1 : {conn}")
    time.sleep(1.5)

    with session_processor.conn_context() as conn:
        print(f"## conn2 : {conn}")
    time.sleep(1.5)
    with session_processor.conn_context() as conn:
        print(f"## conn3 : {conn}")


def test_as_is_conn():
    with DbManager().conn_context() as conn:
        print(f"asis1 conn: {conn}")

    with DbManager().conn_context() as conn:
        print(f"asis2 conn: {conn}")

    with DbManager().conn_context() as conn:
        print(f"asis3 conn: {conn}")