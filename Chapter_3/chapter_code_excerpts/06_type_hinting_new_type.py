from typing import NewType

UserId = NewType("UserId", int)
ProductId = NewType("ProductId", int)


def process_order(user_id: UserId, product_id: ProductId) -> None:
    print(f"Processing order for User {user_id} and Product {product_id}")


# Usage
user_id = UserId(1)
product_id = ProductId(1)  # Same underlying int, but distinct type
process_order(user_id, product_id)
# This would raise a type error:
# process_order(product_id, user_id)
