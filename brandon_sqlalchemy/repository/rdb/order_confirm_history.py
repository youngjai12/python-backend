from typing import Optional, Callable
from contextlib import AbstractContextManager
from brandon_sqlalchemy.repository.rdb.base import AutotradeBase
from sqlalchemy.orm import Session, Mapped, mapped_column

class OrderConfirmHistory(AutotradeBase):
    __tablename__ = "order_confirm_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    tr_log_id: Mapped[Optional[int]]
    order_receipt_id: Mapped[Optional[str]]
    stock_cd: Mapped[str]
    type: Mapped[str]
    price: Mapped[Optional[float]]
    ord_price: Mapped[Optional[float]]
    quantity: Mapped[Optional[float]]
    ord_qty: Mapped[Optional[float]]
    status_flag: Mapped[int]
    ord_ymd: Mapped[str]
    acct_id: Mapped[str]
    ord_no: Mapped[Optional[str]]
    ord_dtim: Mapped[Optional[str]]
    updated_at: Mapped[Optional[str]]
    ord_gno_brno: Mapped[Optional[str]]
    details: Mapped[Optional[str]]
    market: Mapped[Optional[str]]


class OrderConfirmRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self._session_factory = session_factory

    def get_history_by_stock_cd_with_period_day(self, target_stock, start_day, end_day):
        with self._session_factory("autotrade") as session:
            return (
                session.query(OrderConfirmHistory)
                .filter(OrderConfirmHistory.stock_cd == target_stock)
                .filter(OrderConfirmHistory.ord_ymd.between(start_day, end_day))
                .all()
            )

