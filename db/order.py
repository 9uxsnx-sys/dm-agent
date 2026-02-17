from sqlalchemy import Column, Integer, String, Float, DateTime
from db.database import Base
from datetime import datetime

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    user_id = Column(String, index=True)
    product = Column(String)
    quantity = Column(Integer)
    total_price = Column(Float)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
