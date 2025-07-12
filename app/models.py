from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from .database import Base

class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    status = Column(String, default="open")
    timestamp = Column(DateTime, default=datetime.utcnow)
    sentiment = Column(String, default="unknown")
    category = Column(String, default="другое")
    country = Column(String, default="unknown")          # 🆕 страна по IP
    is_spam = Column(Boolean, default=False)             # 🆕 метка спама
