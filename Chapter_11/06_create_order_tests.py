# test_order_creation.py
def test_create_order_success():
    # Setup test data and expected results
    response = client.post(
        "/orders", json={"customer_id": "12345", "items": [{"product_id": "789", "quantity": 2}]}
    )

    # Verify status code and response structure
    assert response.status_code == 201
    assert "order_id" in response.json

    # Verify database state - order was created with correct values
    conn = get_db_connection()
    order = conn.execute(
        "SELECT * FROM orders WHERE id = ?", (response.json["order_id"],)
    ).fetchone()
    assert order["status"] == "PAID"


# Additional order creation test scenarios ...
