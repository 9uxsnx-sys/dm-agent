"""
Seed script to populate the database with mock products.
Run this after the database is initialized.
"""
import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.ext.asyncio import AsyncSession
from db import async_session, Product, Base, engine


async def seed_products():
    """Add 4 mock products to the database."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with async_session() as session:
        # Check if products already exist
        from sqlalchemy import select
        result = await session.execute(select(Product))
        existing = result.scalars().all()
        
        if existing:
            print("Products already exist in database. Skipping seed.")
            return
        
        # Create 4 mock products
        products = [
            Product(
                name="Premium Wireless Headphones",
                stock=50,
                units_per_box=10,
                wholesale_price=120.00,
                retailer_price=150.00,
                individual_price=180.00
            ),
            Product(
                name="Smart Fitness Watch",
                stock=75,
                units_per_box=15,
                wholesale_price=80.00,
                retailer_price=110.00,
                individual_price=140.00
            ),
            Product(
                name="Portable Bluetooth Speaker",
                stock=100,
                units_per_box=20,
                wholesale_price=45.00,
                retailer_price=60.00,
                individual_price=75.00
            ),
            Product(
                name="USB-C Charging Cable Set",
                stock=200,
                units_per_box=50,
                wholesale_price=15.00,
                retailer_price=25.00,
                individual_price=35.00
            )
        ]
        
        session.add_all(products)
        await session.commit()
        print(f"Successfully added {len(products)} mock products to the database.")


if __name__ == "__main__":
    asyncio.run(seed_products())
