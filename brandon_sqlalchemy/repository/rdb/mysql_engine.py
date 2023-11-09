from contextlib import contextmanager, AbstractContextManager
from typing import Any, Callable

from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker, Session


class Mysql:
    def __init__(self, uri: str, connect_timeout: int, opts: dict[str, Any]):

        engine = create_engine(uri, connect_args={"connect_timeout": connect_timeout}, **opts)
        session_factory = scoped_session(
            sessionmaker(
                bind=engine,
                autocommit=False,
                autoflush=True,
                expire_on_commit=False,
            )
        )
        self._dict_session_factory = session_factory

    def retrieve_session(self):
        return self._dict_session_factory()

    @contextmanager
    def create_session(
        self, query_timeout = None
    ) -> Callable[..., AbstractContextManager[Session]]:
        session: Session = self.retrieve_session()

        if query_timeout and query_timeout > 0:
            session.execute(text(f"SET SESSION MAX_EXECUTION_TIME={query_timeout * 1000}"))

        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
