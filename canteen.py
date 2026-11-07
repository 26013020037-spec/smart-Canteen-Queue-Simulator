
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# ---------------- DATA STORAGE ----------------

DATA_FILE = "canteen_data.json"

menu = {
    "Burger": 60,
    "Pizza": 120,
    "Sandwich": 50,
    "French Fries": 70,
    "Cold Coffee": 80,
    "Tea": 20,
    "Samosa": 15,
    "Noodles": 90
}

cart = {}


def load_orders():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                return json.load(file)
        except:
            return []
    return []


orders = load_orders()


def save_orders():
    with open(DATA_FILE, "w") as file:
        json.dump(orders, file, indent=4)


if orders:
    next_order_number = max(
        order["number"] for order in orders
    ) + 1
else:
    next_order_number = 101

total_sales = sum(order["total"] for order in orders)


# ---------------- MAIN WINDOW ----------------

root = tk.Tk()
root.title("Smart Canteen Queue Simulator")
root.geometry("1100x700")
root.configure(bg="#F5F0FF")

# ---------------- COLORS ----------------

PURPLE = "#7041A6"
DARK = "#392653"
PINK = "#F3D9F5"
WHITE = "#FFFFFF"
BG = "#F5F0FF"
GREEN = "#38A169"


# ---------------- HEADING ----------------

heading = tk.Label(
    root,
    text="🍔 SMART CANTEEN",
    font=("Arial", 25, "bold"),
    bg=PURPLE,
    fg="white",
    pady=15
)
heading.pack(fill="x")


# ---------------- SIDEBAR ----------------

sidebar = tk.Frame(root, bg=DARK, width=200)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

content = tk.Frame(root, bg=BG)
content.pack(side="right", fill="both", expand=True)


# ---------------- PAGE FUNCTIONS ----------------

def clear_page():
    for widget in content.winfo_children():
        widget.destroy()


def page_title(title):
    tk.Label(
        content,
        text=title,
        font=("Arial", 22, "bold"),
        bg=BG,
        fg=DARK
    ).pack(pady=20)


# ---------------- DASHBOARD ----------------

def dashboard():
    clear_page()
    page_title("Welcome to Smart Canteen!")

    pending = sum(
        1 for order in orders
        if order["status"] == "Pending"
    )

    completed = sum(
        1 for order in orders
        if order["status"] == "Ready"
    )

    total = len(orders)

    stats = [
        ("Total Orders", total, PURPLE),
        ("Pending Orders", pending, "#E69A35"),
        ("Completed Orders", completed, GREEN),
        ("Total Sales", "₹" + str(total_sales), "#D65A91")
    ]

    frame = tk.Frame(content, bg=BG)
    frame.pack(pady=40)

    for title, value, color in stats:
        card = tk.Frame(
            frame,
            bg=color,
            width=180,
            height=120
        )
        card.pack(side="left", padx=10)
        card.pack_propagate(False)

        tk.Label(
            card,
            text=title,
            bg=color,
            fg="white",
            font=("Arial", 12, "bold")
        ).pack(pady=15)

        tk.Label(
            card,
            text=value,
            bg=color,
            fg="white",
            font=("Arial", 20, "bold")
        ).pack()


# ---------------- FOOD MENU ----------------

def show_menu():
    clear_page()
    page_title("Our Food Menu")

    for item, price in menu.items():

        row = tk.Frame(content, bg=WHITE)
        row.pack(fill="x", padx=50, pady=5)

        tk.Label(
            row,
            text=item,
            font=("Arial", 13, "bold"),
            bg=WHITE,
            width=20,
            anchor="w"
        ).pack(side="left", padx=10, pady=10)

        tk.Label(
            row,
            text="₹" + str(price),
            font=("Arial", 13),
            bg=WHITE,
            width=10
        ).pack(side="left")

        tk.Button(
            row,
            text="Add to Cart",
            bg=PURPLE,
            fg="white",
            command=lambda i=item: add_to_cart(i)
        ).pack(side="right", padx=15)


def add_to_cart(item):
    if item in cart:
        cart[item] += 1
    else:
        cart[item] = 1

    messagebox.showinfo(
        "Added",
        item + " added to cart!"
    )


# ---------------- CART ----------------

def show_cart():
    clear_page()
    page_title("Your Shopping Cart")

    if not cart:
        tk.Label(
            content,
            text="Your cart is empty!",
            font=("Arial", 16),
            bg=BG
        ).pack(pady=30)
        return

    for item, quantity in cart.items():
        row = tk.Frame(content, bg=WHITE)
        row.pack(fill="x", padx=50, pady=5)

        tk.Label(
            row,
            text=f"{item}  x  {quantity}",
            font=("Arial", 13),
            bg=WHITE
        ).pack(side="left", padx=15, pady=10)

        tk.Button(
            row,
            text="-",
            command=lambda i=item: change_quantity(i, -1)
        ).pack(side="right", padx=5)

        tk.Button(
            row,
            text="+",
            command=lambda i=item: change_quantity(i, 1)
        ).pack(side="right", padx=5)

        tk.Button(
            row,
            text="Remove",
            command=lambda i=item: remove_item(i)
        ).pack(side="right", padx=5)

    total = calculate_total()

    tk.Label(
        content,
        text="Total Amount: ₹" + str(total),
        font=("Arial", 18, "bold"),
        bg=BG,
        fg=PURPLE
    ).pack(pady=20)

    tk.Button(
        content,
        text="Checkout",
        bg=GREEN,
        fg="white",
        font=("Arial", 14, "bold"),
        command=checkout
    ).pack(pady=10)


def change_quantity(item, amount):
    cart[item] += amount

    if cart[item] <= 0:
        del cart[item]

    show_cart()


def remove_item(item):
    del cart[item]
    show_cart()


def calculate_total():
    total = 0

    for item, quantity in cart.items():
        total += menu[item] * quantity

    return total


# ---------------- CHECKOUT ----------------

def checkout():
    global next_order_number, total_sales

    if not cart:
        messagebox.showwarning(
            "Empty Cart",
            "Please add food items first!"
        )
        return

    total = calculate_total()

    order = {
        "number": next_order_number,
        "items": cart.copy(),
        "total": total,
        "status": "Pending"
    }

    orders.append(order)

    total_sales += total

    save_orders()

    receipt = f"""
    SMART CANTEEN RECEIPT

    Order Number: {next_order_number}

    -------------------------

    """

    for item, quantity in cart.items():
        receipt += (
            f"{item} x {quantity} = "
            f"₹{menu[item] * quantity}\n"
        )

    waiting_time = sum(
        1 for o in orders if o["status"] == "Pending"
    ) * 5

    receipt += f"""

    -------------------------

    Total Amount: ₹{total}

    Estimated Waiting Time:
    {waiting_time} minutes

    Status: Pending

    Thank You! Visit Again!
    """

    save_orders()

    messagebox.showinfo("Order Receipt", receipt)

    next_order_number += 1
    cart.clear()

    save_orders()
    dashboard()


# ---------------- ORDER MANAGEMENT ----------------

def manage_orders():
    clear_page()
    page_title("Order Management")

    if not orders:
        tk.Label(
            content,
            text="No orders available!",
            font=("Arial", 15),
            bg=BG
        ).pack(pady=30)
        return

    for order in orders:

        details = ", ".join(
            f"{item} x {qty}"
            for item, qty in order["items"].items()
        )

        row = tk.Frame(content, bg=WHITE)
        row.pack(fill="x", padx=30, pady=5)

        text = (
            f"Order #{order['number']} | "
            f"{details} | "
            f"₹{order['total']} | "
            f"{order['status']}"
        )

        tk.Label(
            row,
            text=text,
            bg=WHITE,
            font=("Arial", 10)
        ).pack(side="left", padx=10, pady=10)


    tk.Button(
        content,
        text="Process Next Order",
        bg=GREEN,
        fg="white",
        font=("Arial", 13, "bold"),
        command=process_order
    ).pack(pady=20)


def process_order():

    for order in orders:

        if order["status"] == "Pending":

            order["status"] = "Ready"

            save_orders()

            messagebox.showinfo(
                "Order Completed",
                f"Order #{order['number']} is Ready!"
            )

            manage_orders()
            return

    messagebox.showinfo(
        "Information",
        "No pending orders!"
    )


# ---------------- SALES REPORT ----------------

def sales_report():
    clear_page()
    page_title("Sales Report")

    completed = sum(
        1 for order in orders
        if order["status"] == "Ready"
    )

    pending = sum(
        1 for order in orders
        if order["status"] == "Pending"
    )

    tk.Label(
        content,
        text=f"Total Orders: {len(orders)}",
        font=("Arial", 16),
        bg=BG
    ).pack(pady=10)

    tk.Label(
        content,
        text=f"Completed Orders: {completed}",
        font=("Arial", 16),
        bg=BG
    ).pack(pady=10)

    tk.Label(
        content,
        text=f"Pending Orders: {pending}",
        font=("Arial", 16),
        bg=BG
    ).pack(pady=10)

    tk.Label(
        content,
        text=f"Total Sales: ₹{total_sales}",
        font=("Arial", 20, "bold"),
        fg=GREEN,
        bg=BG
    ).pack(pady=20)


# ---------------- SIDEBAR BUTTONS ----------------

buttons = [
    ("🏠 Dashboard", dashboard),
    ("🍕 Food Menu", show_menu),
    ("🛒 Shopping Cart", show_cart),
    ("📋 Manage Orders", manage_orders),
    ("📊 Sales Report", sales_report)
]

for text, command in buttons:

    tk.Button(
        sidebar,
        text=text,
        font=("Arial", 12, "bold"),
        bg=DARK,
        fg="white",
        activebackground=PURPLE,
        activeforeground="white",
        relief="flat",
        command=command
    ).pack(fill="x", pady=12, ipady=10)


# ---------------- START APPLICATION ----------------

dashboard()

root.mainloop()
