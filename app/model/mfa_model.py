from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class MfaModel(Base):
    __tablename__ = 'mfa'
    __table_args__ = {'schema': 'sysauth'}

    id = Column(Integer, primary_key=True)
    app = Column(String(256), nullable=False)
    user = Column(String(256), nullable=False)
    code = Column(Integer, nullable=False)
