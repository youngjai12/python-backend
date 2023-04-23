from repository.rdb.base import AutotradeBase
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, TEXT, DATETIME
from sqlalchemy.schema import Column

class OrderConfirmHistory(AutotradeBase):
    __tablename__ = "order_confirm_history"

    id = Column(INTEGER, primary_key=True)
    reporter_id = Column(INTEGER, nullable=False)
    reporter_phone_number = Column(VARCHAR(50), nullable=False)
    creator_id = Column(INTEGER, nullable=False)
    chat_id = Column(INTEGER, nullable=True)
    chat_type = Column(VARCHAR(20), nullable=True)
    creator_phone_number = Column(VARCHAR(50), nullable=False)
    creator_nickname = Column(VARCHAR(20), nullable=False)
    chat_inviter_id = Column(INTEGER, nullable=True)
    chat_log_message = Column(TEXT, nullable=True)
    created_at = Column(DATETIME, nullable=False)

