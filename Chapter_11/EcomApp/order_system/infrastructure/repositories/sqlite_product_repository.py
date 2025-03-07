# order_system/infrastructure/repositories/sqlite_product_repository.py
import sqlite3
from typing import List, Optional
from uuid import UUID

from ...domain.entities.product import Product
from ...domain.repositories.product_repository import ProductRepository


class SQLiteProductRepository(ProductRepository):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._ensure_tables()

    def _ensure_tables(self) -> None:
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS products (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    price REAL NOT NULL,
                    stock INTEGER NOT NULL
                )
            """
            )
            conn.commit()

            # Add some sample products if table is empty
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM products")
            count = cursor.fetchone()[0]

            if count == 0:
                sample_products = [
                    (str(UUID("eeb9e5e6-7585-4809-abb5-548f46ca93ea")), "Laptop", 999.99, 10),
                    (str(UUID("1c9e3f9a-9cf8-4df0-8426-7bd241592cef")), "Smartphone", 499.99, 20),
                    (str(UUID("d8cf7035-7cb1-4dd5-8a9b-3d9a618dbf10")), "Headphones", 99.99, 30),
                    (str(UUID("f6c843d5-907b-462c-8513-82e19638a735")), "Tablet", 349.99, 15),
                ]
                conn.executemany(
                    "INSERT INTO products (id, name, price, stock) VALUES (?, ?, ?, ?)",
                    sample_products,
                )
                conn.commit()
        finally:
            conn.close()

    def get_by_id(self, product_id: UUID) -> Optional[Product]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products WHERE id = ?", (str(product_id),))
            data = cursor.fetchone()

            if not data:
                return None

            return Product(
                id=UUID(data["id"]), name=data["name"], price=data["price"], stock=data["stock"]
            )
        finally:
            conn.close()

    def save(self, product: Product) -> None:
        conn = sqlite3.connect(self.db_path)

        try:
            conn.execute(
                "INSERT INTO products (id, name, price, stock) VALUES (?, ?, ?, ?)",
                (str(product.id), product.name, product.price, product.stock),
            )
            conn.commit()
        finally:
            conn.close()

    def update(self, product: Product) -> None:
        conn = sqlite3.connect(self.db_path)

        try:
            conn.execute(
                "UPDATE products SET name = ?, price = ?, stock = ? WHERE id = ?",
                (product.name, product.price, product.stock, str(product.id)),
            )
            conn.commit()
        finally:
            conn.close()

    def get_all(self) -> List[Product]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products")
            products_data = cursor.fetchall()

            products = []
            for data in products_data:
                product = Product(
                    id=UUID(data["id"]), name=data["name"], price=data["price"], stock=data["stock"]
                )
                products.append(product)

            return products
        finally:
            conn.close()
