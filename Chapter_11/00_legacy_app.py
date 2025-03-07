# order_system/app.py
from flask import Flask, request, jsonify
import sqlite3
import requests

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect("orders.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()

    # Input validation mixed with business logic
    if not data or not "customer_id" in data or not "items" in data:
        return jsonify({"error": "Missing required fields"}), 400

    # Direct database access in route handler
    conn = get_db_connection()

    # Business logic mixed with data access
    total_price = 0
    for item in data["items"]:
        # Inventory check via direct database query
        product = conn.execute(
            "SELECT * FROM products WHERE id = ?", (item["product_id"],)
        ).fetchone()
        if not product or product["stock"] < item["quantity"]:
            conn.close()
            return jsonify({"error": f'Product {item["product_id"]} out of stock'}), 400

        # Price calculation mixed with HTTP response preparation
        price = product["price"] * item["quantity"]
        total_price += price

    # External payment service call directly in route handler
    payment_result = requests.post(
        "https://payment-gateway.example.com/process",
        json={"customer_id": data["customer_id"], "amount": total_price, "currency": "USD"},
    )

    if payment_result.status_code != 200:
        conn.close()
        return jsonify({"error": "Payment failed"}), 400

    # Order creation directly in route handler
    order_id = conn.execute(
        "INSERT INTO orders (customer_id, total_price, status) VALUES (?, ?, ?)",
        (data["customer_id"], total_price, "PAID"),
    ).lastrowid

    # Order items creation and inventory update
    for item in data["items"]:
        conn.execute(
            "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)",
            (order_id, item["product_id"], item["quantity"], price),
        )
        conn.execute(  # Update inventory
            "UPDATE products SET stock = stock - ? WHERE id = ?",
            (item["quantity"], item["product_id"]),
        )
    conn.commit()
    conn.close()
    return jsonify({"order_id": order_id, "status": "success"}), 201
