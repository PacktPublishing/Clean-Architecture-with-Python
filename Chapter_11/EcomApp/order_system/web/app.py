# EcomApp/order_system/web/app.py
"""
Simplified Flask app demonstrating Chapter 11 feature flag transformation pattern.
"""
import os
import sqlite3
from flask import Flask, request, jsonify, render_template
from uuid import UUID, uuid4

from ..config import Config

# Clean Architecture imports
from ..application.use_cases.create_order import CreateOrderRequest, CreateOrderUseCase
from ..infrastructure.repositories.sqlite_order_repository import SQLiteOrderRepository
from ..infrastructure.repositories.sqlite_product_repository import SQLiteProductRepository
from ..infrastructure.services.dummy_payment_service import DummyPaymentService
from ..interfaces.controllers.order_controller import OrderController


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Feature flag configuration - can be overridden by environment variable
    app.config["USE_CLEAN_ARCHITECTURE"] = os.getenv("USE_CLEAN_ARCHITECTURE", "True").lower() in (
        "true",
        "1",
        "yes",
    )

    print(f"🚀 Starting Order Processing System")
    print(f"📊 Feature Flag: USE_CLEAN_ARCHITECTURE = {app.config['USE_CLEAN_ARCHITECTURE']}")
    print(f"💾 Database: {app.config['DB_PATH']}")

    def get_db_connection():
        conn = sqlite3.connect(app.config["DB_PATH"])
        conn.row_factory = sqlite3.Row
        return conn

    def get_order_controller():
        """Factory to create clean architecture components"""
        db_path = app.config["DB_PATH"]

        # Create repositories
        order_repository = SQLiteOrderRepository(db_path)
        product_repository = SQLiteProductRepository(db_path)

        # Create payment service
        payment_service = DummyPaymentService()

        # Create use case
        create_use_case = CreateOrderUseCase(
            order_repository=order_repository,
            product_repository=product_repository,
            payment_service=payment_service,
        )

        # Create controller
        return OrderController(create_use_case=create_use_case)

    # Initialize controller for clean architecture path
    order_controller = get_order_controller()

    class ValidationError(Exception):
        pass

    @app.route("/")
    def index():
        """Home page showing current feature flag status and order form"""
        db_path = app.config["DB_PATH"]
        product_repository = SQLiteProductRepository(db_path)
        products = product_repository.get_all()

        # Get recent orders for display
        orders = get_recent_orders()

        return render_template(
            "index.html",
            use_clean_arch=app.config["USE_CLEAN_ARCHITECTURE"],
            products=products,
            orders=orders,
        )

    @app.route("/orders", methods=["GET"])
    def get_orders():
        """API endpoint to get recent orders"""
        orders = get_recent_orders()
        return jsonify(orders)

    @app.route("/orders", methods=["POST"])
    def create_order():
        """
        This is the exact pattern described in Chapter 11.
        A single route handler that uses a feature flag to choose between
        legacy and clean architecture implementations.
        """
        data = request.get_json()

        # Basic input validation remains in the route handler
        if not data or not "customer_id" in data or not "items" in data:
            return jsonify({"error": "Missing required fields"}), 400

        try:
            # Feature flag to control which implementation handles the request
            if app.config.get("USE_CLEAN_ARCHITECTURE", False):
                # Use the clean implementation
                result = order_controller.handle_create_order(data)
                result["implementation"] = "Clean Architecture"
                return jsonify(result), 201
            else:
                # Original legacy implementation remains here
                result = create_order_legacy(data)
                if "error" not in result[0].get_json():
                    result_data = result[0].get_json()
                    result_data["implementation"] = "Legacy"
                    return jsonify(result_data), 201
                return result
        except ValidationError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "Internal server error"}), 500

    def get_recent_orders():
        """Get the 10 most recent orders for display"""
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT o.id, o.customer_id, o.status, o.created_at, o.total_price,
                       COUNT(oi.id) as item_count
                FROM orders o 
                LEFT JOIN order_items oi ON o.id = oi.order_id
                GROUP BY o.id, o.customer_id, o.status, o.created_at, o.total_price
                ORDER BY o.created_at DESC 
                LIMIT 10
            """
            )
            orders = []
            for row in cursor.fetchall():
                orders.append(
                    {
                        "id": row["id"],
                        "customer_id": row["customer_id"],
                        "status": row["status"],
                        "created_at": row["created_at"],
                        "total_price": row["total_price"],
                        "item_count": row["item_count"],
                    }
                )
            return orders
        finally:
            conn.close()

    def create_order_legacy(data):
        """
        Legacy implementation with all the architectural problems described in Chapter 11.
        This represents the 'before' state in the transformation.
        """
        # Direct database access in route handler
        conn = get_db_connection()

        try:
            # Business logic mixed with data access
            total_price = 0
            for item in data["items"]:
                # Inventory check via direct database query
                product = conn.execute(
                    "SELECT * FROM products WHERE id = ?", (item["product_id"],)
                ).fetchone()
                if not product or product["stock"] < item["quantity"]:
                    return jsonify({"error": f'Product {item["product_id"]} out of stock'}), 400

                # Price calculation
                price = product["price"] * item["quantity"]
                total_price += price

            # External payment service call directly in route handler
            # For demo purposes, simulate payment processing
            payment_success = True

            if not payment_success:
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
            return (
                jsonify({"order_id": order_id, "status": "success", "total_price": total_price}),
                201,
            )

        finally:
            conn.close()

    return app
