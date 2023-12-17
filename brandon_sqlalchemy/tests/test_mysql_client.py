from brandon_sqlalchemy.config.config_loader import ConfigLoader
from brandon_sqlalchemy.mysqlclient.mysqlclient import DbConnector


def test_config_path():
    config_loader = ConfigLoader("local.yaml")
    db_config = config_loader.db_config
    print(db_config)