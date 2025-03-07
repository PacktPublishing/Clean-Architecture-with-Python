# order_system/infrastructure/repositories/sqlite_order_repository.py
import sqlite3
from typing import List, Optional
from uuid import UUID

from ...domain.entities.order import Order, OrderItem, OrderStatus
from ...domain.repositories.order_repository import OrderRepository


class RepositoryError(Exception):
    pass


class SQLiteOrderRepository(OrderRepository):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._ensure_tables()

    def _ensure_tables(self) -> None:
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS orders (
                    id TEXT PRIMARY KEY,
                    customer_id TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT,
                    total_price REAL NOT NULL
                )
            """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS order_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id TEXT NOT NULL,
                    product_id TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    price REAL NOT NULL,
                    FOREIGN KEY (order_id) REFERENCES orders (id)
                )
            """
            )
            conn.commit()
        finally:
            conn.close()

    def _order_exists(self, conn, order_id: UUID) -> bool:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM orders WHERE id = ?", (str(order_id),))
        return cursor.fetchone() is not None

    def save(self, order: Order) -> None:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row

        try:
            if self._order_exists(conn, order.id):
                # Update existing order
                conn.execute(
                    "UPDATE orders SET status = ?, updated_at = ?, total_price = ? WHERE id = ?",
                    (
                        order.status.value,
                        order.updated_at.isoformat() if order.updated_at else None,
                        order.total_price,
                        str(order.id),
                    ),
                )

                # Delete existing items
                conn.execute("DELETE FROM order_items WHERE order_id = ?", (str(order.id),))
            else:
                # Insert new order
                conn.execute(
                    "INSERT INTO orders (id, customer_id, status, created_at, updated_at, total_price) VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        str(order.id),
                        str(order.customer_id),
                        order.status.value,
                        order.created_at.isoformat(),
                        order.updated_at.isoformat() if order.updated_at else None,
                        order.total_price,
                    ),
                )

            # Insert order items
            for item in order.items:
                conn.execute(
                    "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)",
                    (str(order.id), str(item.product_id), item.quantity, item.price),
                )

            conn.commit()
        except Exception as e:
            conn.rollback()
            raise RepositoryError(f"Failed to save order: {str(e)}")
        finally:
            conn.close()

    def get_by_id(self, order_id: UUID) -> Optional[Order]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row

        try:
            # Get order
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM orders WHERE id = ?", (str(order_id),))
            order_data = cursor.fetchone()

            if not order_data:
                return None

            # Get order items
            cursor.execute("SELECT * FROM order_items WHERE order_id = ?", (str(order_id),))
            items_data = cursor.fetchall()

            # Create order
            order = Order(customer_id=UUID(order_data["customer_id"]), id=UUID(order_data["id"]))

            # Set order status
            order.status = OrderStatus(order_data["status"])

            # Add items
            for item_data in items_data:
                item = OrderItem(
                    product_id=UUID(item_data["product_id"]),
                    quantity=item_data["quantity"],
                    price=item_data["price"],
                )
                order.add_item(item)

            return order
        except Exception as e:
            raise RepositoryError(f"Failed to get order: {str(e)}")
        finally:
            conn.close()

    def get_by_customer(self, customer_id: UUID) -> List[Order]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row

        try:
            # Get orders for customer
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM orders WHERE customer_id = ?", (str(customer_id),))
            order_ids = cursor.fetchall()

            orders = []
            for order_id in order_ids:
                order = self.get_by_id(UUID(order_id["id"]))
                if order:
                    orders.append(order)

            return orders
        except Exception as e:
            raise RepositoryError(f"Failed to get orders for customer: {str(e)}")
        finally:
            conn.close()
