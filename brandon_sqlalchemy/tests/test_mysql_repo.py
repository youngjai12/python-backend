
from brandon_sqlalchemy.repository.rdb.mysql_engine import Mysql
from brandon_sqlalchemy.repository.rdb.order_confirm_history import OrderConfirmRepository


def test_mysql_repo():
    mysql = Mysql(uri=LOCAL_DB_URI, connect_timeout=3, opts=DB_LOGIN_INFO)
    repo = OrderConfirmRepository(mysql.create_session())
    history = repo.get_history_by_stock_cd_with_period_day("083640", "20230801", "20231108")
    assert len(history) == 10