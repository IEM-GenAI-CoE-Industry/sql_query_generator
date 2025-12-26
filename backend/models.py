# backend/models.py
from sqlalchemy import Column, Integer, String, Numeric
from db import Base

class WallpaperTransaction(Base):
    __tablename__ = "wallpaper_transactions"  # <-- change to your real table name

    id = Column(Integer, primary_key=True, index=True)  # SL No. / primary key

    price = Column(Numeric(10, 2), nullable=False)                 # Price
    cost = Column(Numeric(10, 2), nullable=False)                  # Cost
    sales = Column(Integer, nullable=False)                        # Sales (units)
    profit_margin = Column(Numeric(5, 2), nullable=False)          # Profit_margin
    inventory = Column(Integer, nullable=False)                    # Inventory
    discount_percentage = Column(Numeric(5, 2), nullable=True)     # Discount_percentage
    delivery_days = Column(Integer, nullable=True)                 # Delivery_days
    category = Column(String(50), nullable=False)                  # Category
    material = Column(String(50), nullable=False)                  # Material
    color = Column(String(30), nullable=False)                     # Color
    location = Column(String(50), nullable=False)                  # Location
    season = Column(String(20), nullable=True)                     # Season
    store_type = Column(String(20), nullable=True)                 # Store_type
