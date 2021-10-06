import os
import sqlalchemy

from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker

engine = sqlalchemy.create_engine(os.getenv('DATABASE_URL'), pool_pre_ping=True, echo=False)
Session = sessionmaker(bind=engine, expire_on_commit=True)


@contextmanager
def scoped_session() -> sqlalchemy.orm.Session:
    session: sqlalchemy.orm.Session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
