from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.product import Product
from app.db_cache import cached_query

@cached_query("product", ttl=300)
async def check_stock(product_name: str, quantity: int, db: AsyncSession) -> bool:
    result = await db.execute(select(Product).where(Product.name == product_name))
    product = result.scalars().first()
    if not product:
        return False
    return product.stock >= quantity

@cached_query("product_details", ttl=600)
async def get_product_details(product_name: str, db: AsyncSession):
    result = await db.execute(select(Product).where(Product.name == product_name))
    return result.scalars().first()
