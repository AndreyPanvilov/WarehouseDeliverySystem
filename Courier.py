import math
import random
import time
from Worker import Worker
from datetime import datetime, timedelta
from User import User
from Order import Order


class Courier(Worker):
    def __init__(self, employee_id, warehouse):
        super().__init__(employee_id, "Courier", warehouse)
        self.__is_delivering = False
        self.__delivery_start_time = None
        self.__delivery_return_time = None

    @property
    def is_delivering(self):
        return self.__is_delivering

    def calculate_delivery_time(self, user: User) -> float:
        distance = math.sqrt(
            (user.address_x - self.warehouse.location_x) ** 2 + (user.address_y - self.warehouse.location_y) ** 2
        )
        travel_time_seconds = distance * 30
        delivery_time = travel_time_seconds
        return delivery_time

    def start_shift(self, duration_hours: int) -> None:
        with self.lock:
            random_number = random.randint(1, 100)
            if random_number != 99:
                self.available = False
                self.shift_start_time = datetime.now()
                self.shift_end_time = self.shift_start_time + timedelta(hours=duration_hours)
                print(f"{self.role} {self.employee_id}: shift started for {duration_hours} hours.")
            else:
                print(f"courier {self.employee_id} did not come for his shift")
                print(f"courier {self.employee_id} got penalty 1k rubles")

    def end_shift(self) -> None:
        with self.lock:
            self.available = True
            hours_worked = (datetime.now() - self.shift_start_time).total_seconds() / 3600
            payment = hours_worked * 300
            print(f"{self.role} {self.employee_id}: shift ended. Paid {payment:.2f} rubles.")
            self.shift_start_time = None
            self.shift_end_time = None

    def start_delivery(self, order: Order) -> None:
        #self.__is_delivering = True
        with self.lock:
            self.__is_delivering = True
            self.__delivery_start_time = datetime.now()
            delivery_time = self.calculate_delivery_time(order.user)
            self.__delivery_return_time = self.__delivery_start_time + timedelta(seconds=delivery_time) + \
                                          timedelta(seconds=120)
            order.set_delivery_time(self.__delivery_return_time)
            print(
                f"Courier {self.employee_id} started delivery for Order: {order.order_id}. Expected delivery time: {self.__delivery_return_time}"
            )
            time.sleep(delivery_time + 60 + 60)
            print(f"Courier {self.employee_id}: delivery finished.")
            time.sleep(delivery_time)

    def end_delivery(self):
        with self.lock:
            self.__is_delivering = False
            print(f"Courier {self.employee_id}: returns.")

    def is_available(self):
        with self.lock:
            return super().is_available() and not self.__is_delivering

