from sqlalchemy import Column, Integer, String, Float
from db.database import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    stock = Column(Integer)
    units_per_box = Column(Integer)
    wholesale_price = Column(Float)
    retailer_price = Column(Float)
    individual_price = Column(Float)
