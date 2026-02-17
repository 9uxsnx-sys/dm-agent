#!/usr/bin/env python3
"""Quick test script to verify all components are connected."""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_imports():
    """Test all modules can be imported."""
    print("Testing imports...")
    try:
        from agents import get_intent, extract_data, generate_reply
        from logic import handle_message, check_stock, get_product_details, calculate_price, classify_customer_type
        from db import Product, Customer, Order, Base, engine, async_session, get_db
        from services import generate_response
        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

async def test_mock_products():
    """Test mock product creation."""
    print("\nTesting mock products...")
    try:
        from db import Product
        product = Product(
            name="Test Product",
            stock=10,
            units_per_box=5,
            wholesale_price=50.0,
            retailer_price=75.0,
            individual_price=100.0
        )
        print(f"✓ Product created: {product.name}")
        return True
    except Exception as e:
        print(f"✗ Product test failed: {e}")
        return False

async def test_n8n_workflow():
    """Test n8n workflow file is valid JSON."""
    print("\nTesting n8n workflow...")
    try:
        import json
        with open("n8n/workflow.json", "r") as f:
            workflow = json.load(f)
        assert "nodes" in workflow
        assert "connections" in workflow
        print(f"✓ n8n workflow valid: {workflow.get('name', 'Unnamed')}")
        return True
    except Exception as e:
        print(f"✗ n8n workflow test failed: {e}")
        return False

async def main():
    print("="*50)
    print("AI Sales Agent - Quick Connection Test")
    print("="*50)
    
    results = []
    results.append(await test_imports())
    results.append(await test_mock_products())
    results.append(await test_n8n_workflow())
    
    print("\n" + "="*50)
    if all(results):
        print("✓ All tests passed! Project is organized correctly.")
        print("\nNext steps:")
        print("1. Run: docker-compose up -d")
        print("2. Seed DB: docker-compose exec app python db/seed.py")
        print("3. Test agent: curl -X POST http://localhost:8000/webhook ...")
    else:
        print("✗ Some tests failed. Check errors above.")
        return 1
    print("="*50)
    return 0

if __name__ == "__main__":
    exit(asyncio.run(main()))
