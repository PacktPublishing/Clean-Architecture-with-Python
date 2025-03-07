# order_system/web/legacy_routes.py
import sqlite3
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, current_app
from uuid import uuid4

bp = Blueprint("legacy", __name__, url_prefix="/legacy", cli_group=None)


def get_db_connection():
    conn = sqlite3.connect(current_app.config["DB_PATH"])
    conn.row_factory = sqlite3.Row
    return conn


@bp.route("/create_order", methods=["GET", "POST"])
def create_order_form():
    if request.method == "GET":
        # Get all products for display in form
        conn = get_db_connection()
        products = conn.execute("SELECT * FROM products").fetchall()
        conn.close()
        return render_template("create_order.html", products=products, implementation="legacy")

    # On POST, process the form data
    return redirect(url_for("index"))


@bp.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()

    # Input validation
    if not data or not "customer_id" in data or not "items" in data:
        return jsonify({"error": "Missing required fields"}), 400

    # Direct database access in route handler
    conn = get_db_connection()

    # Calculate total price and check inventory
    total_price = 0

    for item in data["items"]:
        # Inventory check via direct database query
        product = conn.execute(
            "SELECT * FROM products WHERE id = ?", (item["product_id"],)
        ).fetchone()

        if not product or product["stock"] < item["quantity"]:
            conn.close()
            return jsonify({"error": f'Product {item["product_id"]} out of stock'}), 400

        # Price calculation
        price = product["price"] * item["quantity"]
        total_price += price

    # External payment service call directly in route handler
    # For demo purposes, we'll simulate a successful payment
    payment_success = True

    if not payment_success:
        conn.close()
        return jsonify({"error": "Payment failed"}), 400

    # Order creation directly in route handler
    order_id = str(uuid4())
    conn.execute(
        "INSERT INTO orders (id, customer_id, status, created_at, total_price) VALUES (?, ?, ?, datetime(), ?)",
        (order_id, data["customer_id"], "PAID", total_price),
    )

    # Order items creation and inventory update
    for item in data["items"]:
        product = conn.execute(
            "SELECT price FROM products WHERE id = ?", (item["product_id"],)
        ).fetchone()

        conn.execute(
            "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)",
            (order_id, item["product_id"], item["quantity"], product["price"]),
        )

        conn.execute(
            "UPDATE products SET stock = stock - ? WHERE id = ?",
            (item["quantity"], item["product_id"]),
        )

    conn.commit()
    conn.close()

    return jsonify({"order_id": order_id, "status": "success"}), 201
