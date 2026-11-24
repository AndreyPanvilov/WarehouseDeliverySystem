import random
import math
import time
from datetime import datetime, timedelta


class User:
    def __init__(self, user_id, address_x, address_y):
        self.user_id = user_id
        self.address_x = address_x
        self.address_y = address_y

    def __str__(self):
        return f"User(id={self.user_id}, address=({self.address_x}, {self.address_y}))"


class Supplier:
    def __init__(self, supplier_id):
        self.supplier_id = supplier_id

    def __str__(self):
         return f"Supplier(id={self.supplier_id})"


class Item:
    def __init__(self, item_id, name):
        self.item_id = item_id
        self.name = name

    def __str__(self):
        return f"Item(id={self.item_id}, name='{self.name}')"


class Warehouse:
    def __init__(self, warehouse_id, location_x, location_y):
        self.warehouse_id = warehouse_id
        self.location_x = location_x
        self.location_y = location_y
        self.stock = {}  # {item_id: quantity}

    def __str__(self):
        return f"Warehouse(id={self.warehouse_id}, location=({self.location_x}, {self.location_y}))"

    def place_order(self, items, supplier):
        print(f"Warehouse {self.warehouse_id}: Ordering from {supplier.supplier_id}: {items}")
        return items

    def receive_goods(self, items):
      for item, qty in items.items():
        if item in self.stock:
          self.stock[item] += qty
        else:
            self.stock[item] = qty
      print(f"Warehouse {self.warehouse_id}: Received goods. New stock: {self.stock}")

    def check_stock(self, order):
         available_items = {}
         for item, quantity in order.items():
             if item in self.stock and self.stock[item] >= quantity:
                available_items[item] = quantity
             else:
                  if item in self.stock:
                     print(f"Warehouse: {self.warehouse_id} not enough of Item: {item} quantity: {quantity}. Has quantity: {self.stock[item]}")
                  else:
                    print(f"Warehouse: {self.warehouse_id} Item: {item} does not exist in storage.")

         return available_items

    def update_stock(self, items):
      for item, qty in items.items():
        if item in self.stock:
           self.stock[item] -= qty
      print(f"Warehouse {self.warehouse_id}: Updated stock. New stock: {self.stock}")


class Order:
  def __init__(self, order_id, user, items, warehouse):
    self.order_id = order_id
    self.user = user
    self.items = items
    self.status = "placed"
    self.warehouse = warehouse
    self.picker = None
    self.courier = None
    self.start_time = datetime.now()
    self.delivery_time = None

  def set_picker(self, picker):
        self.picker = picker
        self.status = "picking"
        print(f"Order {self.order_id}: Picker assigned {picker.employee_id}")

  def set_courier(self, courier):
      self.courier = courier
      self.status = "delivery"
      print(f"Order {self.order_id}: Courier assigned {courier.employee_id}")

  def set_delivery_time(self, delivery_time):
     self.delivery_time = delivery_time
     self.status = "delivered"
     print(f"Order {self.order_id}: delivery at: {delivery_time}")

  def __str__(self):
       return f"Order(id={self.order_id}, user={self.user.user_id}, items={self.items}, status='{self.status}')"


class Employee:
  def __init__(self, employee_id, role, warehouse):
    self.employee_id = employee_id
    self.role = role
    self.available = False
    self.warehouse = warehouse
    self.shift_start_time = None
    self.shift_end_time = None

  def start_shift(self, duration_hours):
      self.available = True
      self.shift_start_time = datetime.now()
      self.shift_end_time = self.shift_start_time + timedelta(hours=duration_hours)
      print(f"{self.role} {self.employee_id}: shift started for {duration_hours} hours.")

  def end_shift(self):
        self.available = True
        hours_worked = (datetime.now() - self.shift_start_time).total_seconds() / 3600
        payment = hours_worked * 300
        print(f"{self.role} {self.employee_id}: shift ended. Paid {payment:.2f} rubles.")
        self.shift_start_time = None
        self.shift_end_time = None

  def is_available(self):
        return self.available and self.shift_start_time is not None and self.shift_end_time > datetime.now()

  def __str__(self):
     return f"Employee(id={self.employee_id}, role={self.role}, available={self.available})"


class Courier(Employee):
    def __init__(self, employee_id, warehouse):
      super().__init__(employee_id, 'Courier', warehouse)
      self.is_delivering = False
      self.delivery_start_time = None
      self.delivery_return_time = None

    def calculate_delivery_time(self, user):
          distance = math.sqrt((user.address_x - self.warehouse.location_x)**2 + (user.address_y - self.warehouse.location_y)**2)
          travel_time_seconds = distance * 30
          delivery_time = travel_time_seconds + 60 + 60 # 1 minute to leave the warehouse + 1 minute to give the package to the user
          return delivery_time

    def start_delivery(self, order):
          self.is_delivering = True
          self.delivery_start_time = datetime.now()
          delivery_time = self.calculate_delivery_time(order.user)
          self.delivery_return_time = self.delivery_start_time + timedelta(seconds = delivery_time)
          order.set_delivery_time(self.delivery_return_time)
          print(f"Courier {self.employee_id} started delivery for Order: {order.order_id}. Expected delivery time: {self.delivery_return_time}")


    def end_delivery(self):
           self.is_delivering = False
           print(f"Courier {self.employee_id}: delivery finished.")

    def is_available(self):
           return super().is_available() and not self.is_delivering


class Picker(Employee):
    def __init__(self, employee_id, warehouse):
         super().__init__(employee_id, 'Picker', warehouse)

    def pick_order(self, order):
        time_taken = len(order.items) * 45
        print(f"Picker {self.employee_id}: picking order {order.order_id}. Takes {time_taken} seconds")
        time.sleep(time_taken) #simulate picking for X seconds
        return order

# Helper function to print orders
def print_all_orders(orders):
  print("\nAll Orders:")
  for order in orders:
        print(order)


# Example usage
if __name__ == "__main__":

    # Create entities
    supplier1 = Supplier(1)
    warehouse1 = Warehouse(1, 50, 50)

    item1 = Item(1, "Milk")
    item2 = Item(2, "Bread")
    item3 = Item(3, "Eggs")

    user1 = User(1, 10, 10)
    user2 = User(2, 90, 90)

    courier1 = Courier(1, warehouse1)
    courier2 = Courier(2, warehouse1)

    picker1 = Picker(1, warehouse1)
    picker2 = Picker(2, warehouse1)
    employees = [courier1, courier2, picker1, picker2]

    orders = []

    for employee in employees:
        employee.start_shift(8)
    print(employees[2].shift_end_time, employees[2].shift_start_time, employees[2].available)
    # Warehouse places order to supplier
    ordered_items = warehouse1.place_order({item1: 100, item2: 200, item3: 150}, supplier1)

    # Supplier delivers to warehouse
    delivered_items = {item1: 100, item2: 150, item3: 100}
    warehouse1.receive_goods(delivered_items)
    print("all ok")

    # Users place orders
    user1_order = Order(1, user1, {item1: 2, item2: 1}, warehouse1)
    user2_order = Order(2, user2, {item2: 4, item3: 1}, warehouse1)
    orders.append(user1_order)
    orders.append(user2_order)

    # Orders reach the warehouse
    print_all_orders(orders)
    for order in orders:
        available_items = warehouse1.check_stock(order.items)
        if available_items:
            warehouse1.update_stock(available_items)
            print(f"Order {order.order_id}: Available items are: {available_items}")

            # Assign Picker
            available_pickers = [employee for employee in employees if employee.role == 'Picker' and employee.is_available()]
            if available_pickers:
                picker = random.choice(available_pickers)
                order.set_picker(picker)
                picker.pick_order(order)
                print_all_orders(orders)
            else:
                print(f"No pickers available for order: {order.order_id}")
                continue

            # Assign Courier
            available_couriers = [employee for employee in employees if employee.role == 'Courier' and employee.is_available()]
            if available_couriers:
                courier = random.choice(available_couriers)
                order.set_courier(courier)
                courier.start_delivery(order)
            else:
                print(f"No couriers available for order: {order.order_id}")
                continue

        else:
          print(f"Order {order.order_id} could not be fulfilled due to missing items.")

    # Simulate time passing and check if delivery should end
    while orders:
        for order in list(orders):
            if order.status == 'delivered':
                  order.courier.end_delivery()
                  orders.remove(order)
            else:
               time.sleep(1)
    # End all shifts and pay employees
    for employee in employees:
      employee.end_shift()