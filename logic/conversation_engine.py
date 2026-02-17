from agents import get_intent, extract_data, generate_reply
from logic.stock_engine import check_stock, get_product_details
from logic.pricing_engine import calculate_price
from app.state_manager import set_session, get_session
from sqlalchemy.ext.asyncio import AsyncSession

async def handle_message(user_id: str, message: str, platform: str, db: AsyncSession) -> str:
    session = await get_session(user_id) or {}
    intent = await get_intent(message)
    
    if intent == "OTHER":
        return await generate_reply("unknown", None, None, None, "N/A", "greeting")
    
    if intent == "CHECK_ORDER":
        return await generate_reply("unknown", None, None, None, "N/A", "check_order")
    
    extracted = await extract_data(message)
    product = extracted.get("product") or session.get("product")
    quantity = extracted.get("quantity") or session.get("quantity")
    customer_type = extracted.get("customer_type") or session.get("customer_type")
    
    session.update({"product": product, "quantity": quantity, "customer_type": customer_type, "platform": platform})
    
    if not product:
        await set_session(user_id, session)
        return await generate_reply(customer_type or "unknown", None, None, None, "N/A", "ask_product")
    
    if not customer_type:
        await set_session(user_id, session)
        return await generate_reply("unknown", product, quantity, None, "N/A", "ask_customer_type")
    
    if not quantity:
        await set_session(user_id, session)
        return await generate_reply(customer_type, product, None, None, "N/A", "ask_quantity")
    
    from db.order import Order
    from db.customer import Customer
    from sqlalchemy.future import select

    product_obj = await get_product_details(product, db)
    if not product_obj:
        await set_session(user_id, session)
        return await generate_reply(customer_type, product, quantity, None, "Not found", "product_not_found")
    
    has_stock = await check_stock(product, quantity, db)
    stock_status = "In Stock" if has_stock else f"Only {product_obj.stock} available"
    price = calculate_price(quantity, customer_type, product_obj)
    
    # NEW: Save customer if not exists or update type
    result = await db.execute(select(Customer).where(Customer.user_id == user_id))
    customer = result.scalars().first()
    if not customer:
        customer = Customer(user_id=user_id, customer_type=customer_type, platform=platform)
        db.add(customer)
    elif customer.customer_type != customer_type:
        customer.customer_type = customer_type

    # NEW: Create the order
    new_order = Order(
        user_id=user_id,
        product=product,
        quantity=quantity,
        total_price=price,
        status="confirmed" if has_stock else "pending_stock"
    )
    db.add(new_order)
    
    # Update stock if available
    if has_stock:
        product_obj.stock -= quantity
    
    await db.commit()
    await set_session(user_id, session)
    return await generate_reply(customer_type, product, quantity, price, stock_status, "confirm_order")
