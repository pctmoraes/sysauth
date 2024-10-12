from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MfaModel(Base):
    __tablename__ = 'mfa'
    __table_args__ = {'schema': 'sysauth'}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    app = Column(String(256), nullable=False)
    username = Column(String(256), nullable=False)
    code = Column(Integer, nullable=False)
    been_used = Column(Boolean, nullable=False)
