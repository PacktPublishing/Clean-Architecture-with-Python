# order_system/web/clean_routes.py
from dataclasses import dataclass
from flask import Blueprint, current_app, jsonify, render_template, request, redirect, url_for
from uuid import UUID

from ..application.use_cases.create_order import CreateOrderRequest, CreateOrderUseCase
from ..domain.repositories.order_repository import OrderRepository
from ..domain.repositories.product_repository import ProductRepository
from ..domain.services.payment_service import PaymentService
from ..infrastructure.repositories.sqlite_order_repository import SQLiteOrderRepository
from ..infrastructure.repositories.sqlite_product_repository import SQLiteProductRepository
from ..infrastructure.services.dummy_payment_service import DummyPaymentService
from ..interfaces.controllers.order_controller import OrderController

bp = Blueprint("clean", __name__, url_prefix="/clean", cli_group=None)


# Factory to create dependencies
def get_order_controller():
    db_path = current_app.config["DB_PATH"]

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


@bp.route("/create_order", methods=["GET", "POST"])
def create_order_form():
    if request.method == "GET":
        # Get products using Clean Architecture
        db_path = current_app.config["DB_PATH"]
        product_repository = SQLiteProductRepository(db_path)
        products = product_repository.get_all()
        return render_template("create_order.html", products=products, implementation="clean")

    # On POST, process the form data
    return redirect(url_for("index"))


@bp.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()

    # Input validation
    if not data or not "customer_id" in data or not "items" in data:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # Use the clean implementation
        controller = get_order_controller()
        result = controller.handle_create_order(data)
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500
