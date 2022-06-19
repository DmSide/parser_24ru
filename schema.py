import uuid as uuid
from sqlalchemy import String, \
    Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Jobs(Base):
    __tablename__ = 'jobs'
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4(), primary_key=True)
    title = Column(String(128), nullable=False)
    link = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=False)
    money = Column(String(128), nullable=True)
    countries = Column(String(256), nullable=False)
    published = Column(String(128), nullable=False)
