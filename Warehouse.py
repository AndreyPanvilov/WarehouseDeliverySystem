from Picker import Picker
from Courier import Courier
from datetime import datetime
from Supplier import Supplier
from Order import Order


class Warehouse:
    def __init__(self, warehouse_id: int, location_x: int, location_y: int, open_time: datetime.time,
                 close_time: datetime.time, num_pickers: int, num_couriers: int):
        self.__warehouse_id = warehouse_id
        self.__location_x = location_x
        self.__location_y = location_y
        self.__stock = {}  # {item_id: quantity}
        self.__open_time = open_time
        self.__close_time = close_time
        self.__pickers = []
        self.__couriers = []
        for i in range(num_pickers):
            self.__pickers.append(Picker(f'Picker-{i}-{warehouse_id}', self))
        for i in range(num_couriers):
            self.__couriers.append(Courier(f'Courier-{i}-{warehouse_id}', self))

    @property
    def warehouse_id(self) -> int:
        return self.__warehouse_id

    @property
    def location_x(self) -> int:
        return self.__location_x

    @property
    def location_y(self) -> int:
        return self.__location_y

    @property
    def stock(self) -> {}:
        return self.__stock

    @property
    def open_time(self) -> datetime.time:
        return self.__open_time

    @property
    def close_time(self) -> datetime.time:
        return self.__close_time

    @property
    def pickers(self) -> list[Picker]:
        return self.__pickers

    @property
    def couriers(self) -> list[Courier]:
        return self.__couriers

    def __str__(self) -> str:
        return f"Warehouse(id={self.__warehouse_id}, location=({self.__location_x}, {self.__location_y}))"

    def place_order(self, items: {}, supplier: Supplier) -> {}:
        print(f"Warehouse {self.__warehouse_id}: Ordering from {supplier.supplier_id}: {items}")
        return items

    def receive_goods(self, items: {}):
        for item, qty in items.items():
            if item in self.stock:
                self.stock[item] += qty
            else:
                self.stock[item] = qty
        print(f"Warehouse {self.__warehouse_id}: Received goods. New stock: {self.stock}")

    def check_stock(self, order: Order) -> {}:
        available_items = {}
        for item, quantity in order.items():
            if item in self.stock and self.stock[item] >= quantity:
                available_items[item] = quantity
            else:
                if item in self.stock:
                    print(
                        f"Warehouse: {self.__warehouse_id} not enough of Item: {item} quantity: {quantity}. Has quantity: {self.stock[item]}"
                    )

                else:
                    print(f"Warehouse: {self.__warehouse_id} Item: {item} does not exist in storage.")


        return available_items

    def update_stock(self, items) -> None:
        for item, qty in items.items():
            if item in self.stock:
                self.stock[item] -= qty
        print(f"Warehouse {self.__warehouse_id}: Updated stock. New stock: {self.stock}")

    def is_open(self) -> None:
        now = datetime.now().time()
        return self.__open_time <= now <= self.__close_time