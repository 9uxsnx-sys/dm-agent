from sqlalchemy import Column, Integer, String, DateTime
from db.database import Base
from datetime import datetime

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True)
    user_id = Column(String, unique=True, index=True)
    customer_type = Column(String)
    platform = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
