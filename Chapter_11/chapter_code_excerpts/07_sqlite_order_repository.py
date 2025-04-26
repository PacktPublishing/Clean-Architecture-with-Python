# order_system/infrastructure/repositories/sqlite_order_repository.py
class SQLiteOrderRepository(OrderRepository):

    # ... truncated implementation
    
    def save(self, order: Order) -> None:
        conn = sqlite3.connect(self.db_path)
        
        try:
            cursor = conn.cursor()
            # Check if order exists and perform insert or update
            if self._order_exists(conn, order.id):
                # ... SQL update operation ...
            else:
                # ... SQL insert operation ...
                
                # ... SQL operations for order items ...
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise RepositoryError(f"Failed to save order: {str(e)}")
        finally:
            conn.close()