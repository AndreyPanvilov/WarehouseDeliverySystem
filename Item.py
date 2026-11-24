class Item:
    def __init__(self, item_id: int, name: str, price: int):
        self.item_id = item_id
        self.name = name
        self.price = price

    def __str__(self) -> str:
        return f"Item(id={self.item_id}, name={self.name}, price={self.price})"