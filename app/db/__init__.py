import sqlalchemy.orm
from sqlalchemy.orm import scoped_session, sessionmaker

from app import config
from app.db.models import Base

engine = sqlalchemy.create_engine(config.db_connect_string)

Base.metadata.create_all(engine)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

from .util import *
