from Item import Item


class Supplier:
    def __init__(self, supplier_id: int, stock: {Item: int}):
        self.supplier_id = supplier_id
        self.stock = stock

    def receive_order(self, items: {Item: int}) -> {Item: int}:
        available_items = {}
        for item, quantity in items.items():
            if item in self.stock and self.stock[item] >= quantity:
                available_items[item] = quantity
                self.stock[item] -= quantity
            else:
                if item in self.stock:
                    available_items[item] = self.stock[item]
                    self.stock[item] = 0

        return available_items

    def __str__(self) -> str:
        return f"Supplier(id={self.supplier_id}, items={self.stock})"