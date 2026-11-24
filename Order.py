from __future__ import annotations
import threading
from datetime import datetime
#from Picker import Picker
#from Courier import Courier
from User import User
from Item import Item


class Order:
    def __init__(self, order_id: int, user: 'User', items: {Item: int}, warehouse=None):
        self.order_id = order_id
        self.user = user
        self.items = items
        self.status = "placed"
        self.warehouse = warehouse
        self.picker = None
        self.courier = None
        self.start_time = datetime.now()
        self.delivery_time = None
        self.lock = threading.Lock()

    def set_picker(self, picker: 'Picker') -> None:
        with self.lock:
            self.picker = picker
            self.status = "picking"
            print(f"Order {self.order_id}: Picker assigned {picker.employee_id}")

    def set_courier(self, courier: 'Courier') -> None:
        with self.lock:
            self.courier = courier
            self.status = "delivery"
            print(f"Order {self.order_id}: Courier assigned {courier.employee_id}")

    def set_delivery_time(self, delivery_time: int) -> None:
        with self.lock:
            self.delivery_time = delivery_time
            self.status = "delivered"
            print(f"Order {self.order_id}: delivery at: {delivery_time}")

    def __str__(self) -> str:
        return f"Order(id={self.order_id}, user={self.user.user_id}, items={self.items}, status='{self.status}')"