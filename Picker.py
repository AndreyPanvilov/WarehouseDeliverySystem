from __future__ import annotations
from Worker import Worker
from datetime import datetime, timedelta
from Order import Order
import time


class Picker(Worker):
    def __init__(self, employee_id: str, warehouse):
        super().__init__(employee_id, "Picker", warehouse)
        self.__is_picking = False

    @property
    def is_picking(self):
        return self.__is_picking

    def start_shift(self, duration_hours: int) -> None:
        with self.lock:
            self.available = False
            self.shift_start_time = datetime.now()
            self.shift_end_time = self.shift_start_time + timedelta(hours=duration_hours)
            print(f"{self.role} {self.employee_id}: shift started for {duration_hours} hours.")

    def end_shift(self):
        with self.lock:
            self.available = True
            hours_worked = (datetime.now() - self.shift_start_time).total_seconds() / 3600
            payment = hours_worked * 300
            print(f"{self.role} {self.employee_id}: shift ended. Paid {payment:.2f} rubles.")
            self.shift_start_time = None
            self.shift_end_time = None

    def pick_order(self, order: 'Order') -> None:
        #self.__is_picking = True
        with self.lock:
            self.__is_picking = True
            time_taken = len(order.items) * 5
            print(f"Picker {self.employee_id}: picking order {order.order_id}. Takes {time_taken} seconds")
            self.available_at = datetime.now()
            self.available_at += timedelta(seconds=time_taken)
            time.sleep(time_taken)
            self.__is_picking = False
            order.picker = self.employee_id

        return order

    def is_available(self):
        with self.lock:
            return super().is_available() and not self.__is_picking