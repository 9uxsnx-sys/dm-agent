"""Test database seed and basic imports."""
import pytest
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import Product, Customer, Order, Base, engine, async_session
from logic import handle_message, check_stock, get_product_details, calculate_price
from agents import get_intent, extract_data, generate_reply


@pytest.mark.asyncio
async def test_db_connection():
    """Test database connection works."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    assert True


@pytest.mark.asyncio
async def test_product_model():
    """Test Product model can be instantiated."""
    product = Product(
        name="Test Product",
        stock=10,
        units_per_box=5,
        wholesale_price=50.0,
        retailer_price=75.0,
        individual_price=100.0
    )
    assert product.name == "Test Product"
    assert product.stock == 10


@pytest.mark.asyncio
async def test_agent_imports():
    """Test all agent functions are importable."""
    assert callable(get_intent)
    assert callable(extract_data)
    assert callable(generate_reply)


@pytest.mark.asyncio
async def test_logic_imports():
    """Test all logic functions are importable."""
    assert callable(handle_message)
    assert callable(check_stock)
    assert callable(get_product_details)
    assert callable(calculate_price)
