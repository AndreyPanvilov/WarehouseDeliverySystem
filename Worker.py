from abc import ABC, abstractmethod
import threading
from datetime import datetime


class Worker(ABC):
    def __init__(self, employee_id: str, role, warehouse):
        self.employee_id = employee_id
        self.role = role
        self.available = True
        self.warehouse = warehouse
        self.shift_start_time = None
        self.shift_end_time = None
        self.available_at = None
        self.lock = threading.Lock()

    @abstractmethod
    def start_shift(self, duration_hours: int):
        pass

    @abstractmethod
    def end_shift(self):
        pass

    def is_available(self):
        with self.lock:
            return (
                #self.available
                self.shift_start_time is not None
                and (self.available_at is None or self.available_at < datetime.now())
                and self.shift_end_time > datetime.now()
            )

    def __str__(self) -> str:
        return f"Employee(id={self.employee_id}, role={self.role}, available={self.available})"
