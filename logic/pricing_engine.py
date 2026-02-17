def calculate_price(quantity: int, customer_type: str, product_db_obj) -> float:
    if customer_type == "wholesaler":
        unit_price = product_db_obj.wholesale_price
    elif customer_type == "retailer":
        unit_price = product_db_obj.retailer_price
    else:
        unit_price = product_db_obj.individual_price
    return quantity * unit_price
