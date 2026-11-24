from __future__ import annotations
import math
import time
from datetime import datetime
import threading
import queue
from Order import Order
from Warehouse import Warehouse
from User import User
from Supplier import Supplier
from Item import Item


def print_all_orders(orders: list['Order']) -> None:
    print("\nAll Orders:")
    for order in orders:
        print(order)


def process_order(order: 'Order', employees: list) -> None:
    if order.warehouse:
        available_items = order.warehouse.check_stock(order.items)
        if available_items:
            order.warehouse.update_stock(available_items)

            # Assign Picker
            while True:
                available_pickers = [employee for employee in employees if employee.role == "Picker"
                                     and not employee.is_picking]
                if available_pickers:
                    picker = available_pickers[0]
                    order.set_picker(picker)
                    picker.pick_order(order)
                    break
                else:
                    time.sleep(1)

            while True:
                available_couriers = [employee for employee in employees if
                                      employee.role == "Courier" and not employee.is_delivering]
                if available_couriers:
                    courier = available_couriers[0]
                    order.set_courier(courier)
                    courier.start_delivery(order)
                    courier.end_delivery()
                    break
                else:
                    time.sleep(1)
        else:
            print(f"Order {order.order_id} could not be fulfilled due to missing items.")
    else:
        print(f"Order {order.order_id} could not be fulfilled as no warehouse was assigned")


def delivery_simulation(orders: list['Order'], warehouses: list[Warehouse])-> None:
    order_queue = queue.Queue()
    for order in orders:
       order_queue.put(order)
    threads = []

    def process_orders_from_queue():
        while True:
            try:
                order = order_queue.get(timeout=1)
            except queue.Empty:
                break

            assigned_warehouse = assign_order_to_warehouse(order, warehouses)
            print(f"for order {order.order_id} assigned warehouse {assigned_warehouse.warehouse_id}")
            order.warehouse = assigned_warehouse
            employees = []
            for i in assigned_warehouse.pickers:
                employees.append(i)
            for i in assigned_warehouse.couriers:
                employees.append(i)
            process_order(order, employees)
            order_queue.task_done()

    num_threads = 5
    for _ in range(num_threads):
        thread = threading.Thread(target=process_orders_from_queue)
        threads.append(thread)
        thread.start()
    for thread in threads:
        time.sleep(1)
        thread.join()


    while orders:
        for order in list(orders):
           if order.status == 'delivered':
                order.courier.end_delivery()
                orders.remove(order)
           else:
                time.sleep(1)


def calculate_distance(coord1_x: float, coord1_y: float, coord2_x: float, coord2_y: float)-> float:
    return math.sqrt((coord2_x - coord1_x) ** 2 + (coord2_y - coord1_y) ** 2)


def assign_order_to_warehouse(order: 'Order', warehouses: list) -> Warehouse:
    eligible_warehouses = []
    max_cnt_items_avlbl = 0
    best_fulfill_warehouse = None
    cnt_item_in_ord = sum(value for value in order.items.values())
    for warehouse in warehouses:
       if warehouse.is_open():
            items_available = warehouse.check_stock(order.items)
            sum_val = sum(value for value in items_available.values())
            if cnt_item_in_ord == sum_val:
                eligible_warehouses.append(warehouse)
            else:
                if max_cnt_items_avlbl < sum_val:
                    best_fulfill_warehouse = warehouse

    if not eligible_warehouses:
        print("No warehouses can fulfill the order")
        print("fulfill order by what best fulfill warehouse have? (y/n)")
        s = input()
        if s == "n":
            return None
        elif s == "y":
            return best_fulfill_warehouse

    eligible_warehouses.sort(
        key=lambda warehouse: calculate_distance(
            order.user.address_x, order.user.address_y, warehouse.location_x, warehouse.location_y
        )
    )
    return eligible_warehouses[0]


if __name__ == "__main__":
    warehouse1 = Warehouse(1, 20, 20, datetime.strptime("08:00", "%H:%M").time(),
                           datetime.strptime("23:00", "%H:%M").time(), 2, 3)
    warehouse2 = Warehouse(2, 80, 80, datetime.strptime("09:00", "%H:%M").time(),
                           datetime.strptime("22:00", "%H:%M").time(), 3, 2)
    warehouses = [warehouse1, warehouse2]

    item1 = Item(1, "Milk", 30)
    item2 = Item(2, "Bread", 50)
    item3 = Item(3, "Eggs", 70)

    supplier1 = Supplier(1, {item1: 1000, item2: 2000, item3: 1500})

    user1 = User(1, 10, 10)
    user2 = User(2, 90, 90)
    user3 = User(3, 50, 50)
    user4 = User(4, 70, 70)
    user5 = User(5, 15, 15)
    user6 = User(6, 20, 25)

    ordered_items1 = warehouse1.place_order({item1: 100, item2: 200, item3: 150}, supplier1)
    ordered_items2 = warehouse2.place_order({item1: 100, item2: 250, item3: 100}, supplier1)

    delivered_items1 = supplier1.receive_order(ordered_items1)
    delivered_items2 = supplier1.receive_order(ordered_items2)

    #delivered_items1 = {item1: 100, item2: 150, item3: 100}
    warehouse1.receive_goods(delivered_items1)
    #delivered_items2 = {item1: 50, item2: 75, item3: 100}
    warehouse2.receive_goods(delivered_items2)

    for warehouse in warehouses:
        for employee in warehouse.pickers:
            employee.start_shift(8)
        for employee in warehouse.couriers:
            employee.start_shift(8)

    orders = []

    user1_order = Order(1, user1, {item1: 2, item2: 1})
    user2_order = Order(2, user2, {item2: 4, item3: 1})
    user3_order = Order(3, user3, {item1: 1, item3: 1, item2: 10})
    user4_order = Order(4, user4, {item1: 1})
    user5_order = Order(5, user5, {item1: 1, item3: 3})
    user6_order = Order(6, user6, {item1: 1})

    orders.append(user1_order)
    orders.append(user2_order)
    orders.append(user3_order)
    orders.append(user4_order)
    orders.append(user5_order)
    orders.append(user6_order)

    print_all_orders(orders)
    delivery_simulation(orders, warehouses)

    for warehouse in warehouses:
        for employee in warehouse.pickers:
            employee.end_shift()
        for employee in warehouse.couriers:
            employee.end_shift()