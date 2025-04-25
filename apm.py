import tkinter as tk
from tkinter import messagebox, ttk
import time
import random
from datetime import datetime

# Main window setup
root = tk.Tk()
root.title("APM - Grocery Delivery")
root.geometry("1200x800")  # Increased window size for additional content
root.configure(bg="white")

# Mock database
users = {
    "customer1": {"password": "password1", "address": "123 Main St", "phone": "555-1234"},
    "admin": {"password": "adminpass"}
}
inventory = {
    "Milk": {"stock": 100, "price": 2, "category": "Dairy, Bread & Eggs"},
    "Bread": {"stock": 50, "price": 1.5, "category": "Dairy, Bread & Eggs"},
    "Eggs": {"stock": 30, "price": 2.5, "category": "Dairy, Bread & Eggs"},
    "Banana": {"stock": 80, "price": 1, "category": "Fruits & Vegetables"},
    "Tomato": {"stock": 60, "price": 0.5, "category": "Fruits & Vegetables"},
    "Potato": {"stock": 70, "price": 0.75, "category": "Fruits & Vegetables"},
    "Coke": {"stock": 40, "price": 1.2, "category": "Cold Drinks & Juices"},
    "Orange Juice": {"stock": 35, "price": 2.3, "category": "Cold Drinks & Juices"},
    "Chips": {"stock": 50, "price": 1.1, "category": "Snacks & Munchies"},
    "Popcorn": {"stock": 45, "price": 1.5, "category": "Snacks & Munchies"},
}
orders = []
drivers = [
    {"name": "Driver1", "available": True, "location": "Downtown"},
    {"name": "Driver2", "available": True, "location": "Uptown"},
    {"name": "Driver3", "available": True, "location": "Midtown"}
]

# Global variables
current_user = None
selected_items = {}
order_status = {}

# Category items mapping
category_items = {
    "Dairy, Bread & Eggs": [("Milk", 2), ("Bread", 1.5), ("Eggs", 2.5)],
    "Fruits & Vegetables": [("Banana", 1), ("Tomato", 0.5), ("Potato", 0.75)],
    "Cold Drinks & Juices": [("Coke", 1.2), ("Orange Juice", 2.3)],
    "Snacks & Munchies": [("Chips", 1.1), ("Popcorn", 1.5)],
}

# Login window
def open_login():
    login_win = tk.Toplevel(root)
    login_win.title("Login - APM")
    login_win.geometry("300x200")
    login_win.configure(bg="white")

    tk.Label(login_win, text="Login", font=("Helvetica", 16, "bold"), bg="white").pack(pady=10)
    tk.Label(login_win, text="Username", bg="white").pack()
    username_entry = tk.Entry(login_win)
    username_entry.pack()

    tk.Label(login_win, text="Password", bg="white").pack()
    password_entry = tk.Entry(login_win, show="*")
    password_entry.pack()

    def submit_login():
        username = username_entry.get()
        password = password_entry.get()
        if not username or not password:
            messagebox.showerror("Login", "Please fill in all fields.")
            return
        if username in users and users[username]["password"] == password:
            global current_user
            current_user = username
            messagebox.showinfo("Login", f"Logged in as {username}!")
            login_win.destroy()
        else:
            messagebox.showerror("Login", "Invalid credentials")

    tk.Button(login_win, text="Submit", command=submit_login, bg="lightgreen").pack(pady=10)

# User Profile Window
def open_profile():
    if not current_user or current_user == "admin":
        messagebox.showwarning("Access Denied", "Only customers can access profiles.")
        return

    profile_win = tk.Toplevel(root)
    profile_win.title("User Profile")
    profile_win.geometry("350x300")
    profile_win.configure(bg="white")

    tk.Label(profile_win, text="User Profile", font=("Helvetica", 16, "bold"), bg="white").pack(pady=10)
    tk.Label(profile_win, text=f"Username: {current_user}", bg="white").pack()
    
    tk.Label(profile_win, text="Address:", bg="white").pack()
    address_entry = tk.Entry(profile_win)
    address_entry.insert(0, users[current_user].get("address", ""))
    address_entry.pack()

    tk.Label(profile_win, text="Phone:", bg="white").pack()
    phone_entry = tk.Entry(profile_win)
    phone_entry.insert(0, users[current_user].get("phone", ""))
    phone_entry.pack()

    def save_profile():
        if not address_entry.get() or not phone_entry.get():
            messagebox.showerror("Profile", "All fields are required.")
            return
        users[current_user]["address"] = address_entry.get()
        users[current_user]["phone"] = phone_entry.get()
        messagebox.showinfo("Profile", "Profile updated successfully!")
        profile_win.destroy()

    tk.Button(profile_win, text="Save", command=save_profile, bg="lightgreen").pack(pady=10)

# Order History Window
def open_order_history():
    if not current_user:
        messagebox.showwarning("Login Required", "Please login to view order history.")
        return

    history_win = tk.Toplevel(root)
    history_win.title("Order History")
    history_win.geometry("600x400")
    history_win.configure(bg="white")

    tk.Label(history_win, text="Order History", font=("Helvetica", 16, "bold"), bg="white").pack(pady=10)

    user_orders = [o for o in orders if o["user"] == current_user]
    if not user_orders:
        tk.Label(history_win, text="No orders yet.", bg="white").pack(pady=10)
        return

    tree = ttk.Treeview(history_win, columns=("Order ID", "Date", "Total", "Status"), show="headings")
    tree.heading("Order ID", text="Order ID")
    tree.heading("Date", text="Date")
    tree.heading("Total", text="Total")
    tree.heading("Status", text="Status")
    for order in user_orders:
        date = datetime.fromtimestamp(order["timestamp"]).strftime("%Y-%m-%d %H:%M")
        tree.insert("", "end", values=(order["id"], date, f"${order['total']:.2f}", order["status"]))
    tree.pack(pady=10, fill="both", expand=True)

    def view_details():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Selection", "Please select an order to view details.")
            return
        order_id = tree.item(selected[0])["values"][0]
        order = next(o for o in orders if o["id"] == order_id)
        details_win = tk.Toplevel(history_win)
        details_win.title(f"Order {order_id} Details")
        details_win.geometry("400x300")
        details_win.configure(bg="white")

        tk.Label(details_win, text=f"Order {order_id}", font=("Helvetica", 14, "bold"), bg="white").pack(pady=5)
        tk.Label(details_win, text=f"Status: {order['status']}", bg="white").pack()
        tk.Label(details_win, text=f"Driver: {order['driver'] or 'Not Assigned'}", bg="white").pack()
        tk.Label(details_win, text="Items:", bg="white").pack()
        for cat, items in order["items"].items():
            for name, price, qty in items:
                tk.Label(details_win, text=f"{cat}: {name} x{qty} - ${price * qty}", bg="white").pack(anchor="w", padx=20)

    tk.Button(history_win, text="View Details", command=view_details, bg="lightblue").pack(pady=5)

# Category selection window with search and filters
def open_category_window(category, items):
    if not current_user:
        messagebox.showwarning("Login Required", "Please login to select items.")
        return

    win = tk.Toplevel(root)
    win.title(f"{category} Items")
    win.geometry("450x500")
    win.configure(bg="white")

    tk.Label(win, text=f"Select items from {category}", font=("Helvetica", 13, "bold"), bg="white").pack(pady=10)

    # Search and filter
    search_frame = tk.Frame(win, bg="white")
    search_frame.pack(pady=5)
    tk.Label(search_frame, text="Search:", bg="white").pack(side="left")
    search_entry = tk.Entry(search_frame)
    search_entry.pack(side="left", padx=5)
    tk.Label(search_frame, text="Sort by:", bg="white").pack(side="left")
    sort_var = tk.StringVar(value="Name")
    tk.OptionMenu(search_frame, sort_var, "Name", "Price").pack(side="left", padx=5)

    item_frame = tk.Frame(win, bg="white")
    item_frame.pack(pady=10)

    selected_vars = {}
    quantities = {}

    def display_items(search_term="", sort_by="Name"):
        for widget in item_frame.winfo_children():
            widget.destroy()

        filtered_items = [item for item in items if search_term.lower() in item[0].lower()]
        if sort_by == "Price":
            filtered_items.sort(key=lambda x: x[1])
        else:
            filtered_items.sort(key=lambda x: x[0])

        for name, price in filtered_items:
            frame = tk.Frame(item_frame, bg="white")
            frame.pack(anchor="w", padx=20, pady=5)
            selected_vars[name] = tk.BooleanVar()
            quantities[name] = tk.IntVar(value=1)
            tk.Checkbutton(frame, text=f"{name} (${price})", variable=selected_vars[name], font=("Helvetica", 11), bg="white").pack(side="left")
            tk.Spinbox(frame, from_=1, to=inventory[name]["stock"], width=5, textvariable=quantities[name]).pack(side="left", padx=5)

    display_items()

    def update_display():
        display_items(search_entry.get(), sort_var.get())

    tk.Button(win, text="Apply Filter", command=update_display, bg="lightblue").pack(pady=5)

    def confirm_selection():
        selected_items_in_category = []
        for name, var in selected_vars.items():
            if var.get():
                qty = quantities[name].get()
                if qty > inventory[name]["stock"]:
                    messagebox.showwarning("Stock Error", f"Only {inventory[name]['stock']} {name} available.")
                    return
                selected_items_in_category.append((name, inventory[name]["price"], qty))
        
        if not selected_items_in_category:
            messagebox.showwarning("Selection Required", "Please select at least one item.")
            return
        
        selected_items[category] = selected_items_in_category
        messagebox.showinfo("Selected", f"Selected items from {category}: " + ", ".join([f"{item[0]} x{item[2]}" for item in selected_items_in_category]))
        win.destroy()

    tk.Button(win, text="Confirm", bg="#86efac", command=confirm_selection).pack(pady=10)

# Checkout with simulated payment
def open_checkout():
    if not current_user:
        messagebox.showwarning("Login Required", "Please login to checkout.")
        return

    if not selected_items:
        messagebox.showwarning("No items", "Please select at least one item before checkout.")
        return

    win = tk.Toplevel(root)
    win.title("Checkout")
    win.geometry("400x400")
    win.configure(bg="white")

    tk.Label(win, text="Your Selected Items", font=("Helvetica", 14, "bold"), bg="white").pack(pady=10)

    total = 0
    for cat, items in selected_items.items():
        for name, price, qty in items:
            tk.Label(win, text=f"{cat}: {name} x{qty} - ${price * qty}", bg="white", font=("Helvetica", 11)).pack(anchor="w", padx=20)
            total += price * qty

    tk.Label(win, text=f"\nTotal: ${total:.2f}", font=("Helvetica", 13, "bold"), bg="white").pack(pady=10)

    def simulate_payment():
        payment_win = tk.Toplevel(win)
        payment_win.title("Payment Gateway")
        payment_win.geometry("300x200")
        payment_win.configure(bg="white")

        tk.Label(payment_win, text="Simulated Payment", font=("Helvetica", 14, "bold"), bg="white").pack(pady=10)
        tk.Label(payment_win, text="Card Number:", bg="white").pack()
        card_entry = tk.Entry(payment_win)
        card_entry.pack()
        tk.Label(payment_win, text="Expiry Date (MM/YY):", bg="white").pack()
        expiry_entry = tk.Entry(payment_win)
        expiry_entry.pack()
        tk.Label(payment_win, text="CVV:", bg="white").pack()
        cvv_entry = tk.Entry(payment_win, show="*")
        cvv_entry.pack()

        def complete_payment():
            if not card_entry.get() or not expiry_entry.get() or not cvv_entry.get():
                messagebox.showerror("Payment", "All fields are required.")
                return
            messagebox.showinfo("Payment", "Payment Successful!")
            payment_win.destroy()
            process_order(total)

        tk.Button(payment_win, text="Pay Now", command=complete_payment, bg="lightgreen").pack(pady=10)

    def process_order(total):
        order_id = f"ORD{len(orders) + 1:04d}"
        order = {
            "id": order_id,
            "user": current_user,
            "items": selected_items.copy(),
            "total": total,
            "status": "Processing",
            "timestamp": time.time(),
            "driver": None
        }
        for cat, items in selected_items.items():
            for name, _, qty in items:
                inventory[name]["stock"] -= qty
                if inventory[name]["stock"] < 10:
                    messagebox.showwarning("Low Stock", f"{name} stock is low ({inventory[name]['stock']}). Restocking needed.")
        orders.append(order)
        order_status[order_id] = "Processing"
        messagebox.showinfo("Order Placed", f"Order ID: {order_id}\nThanks for shopping at APM 😊")
        selected_items.clear()
        win.destroy()
        simulate_delivery(order_id)

    tk.Button(win, text="Proceed to Payment", bg="#4ade80", font=("Helvetica", 12), command=simulate_payment).pack(pady=10)

# Simulate delivery with location-based driver assignment
def simulate_delivery(order_id):
    def assign_driver():
        available_drivers = [d for d in drivers if d["available"]]
        if available_drivers:
            # Simulate location-based assignment (random for now)
            driver = random.choice(available_drivers)
            driver["available"] = False
            return driver["name"]
        return None

    def update_status():
        order = next(o for o in orders if o["id"] == order_id)
        if order["status"] == "Processing":
            driver = assign_driver()
            if driver:
                order["driver"] = driver
                order["status"] = "Out for Delivery"
                order_status[order_id] = "Out for Delivery"
                root.after(5000, update_status)
            else:
                messagebox.showwarning("No Drivers", "No drivers available. Order will be delayed.")
        elif order["status"] == "Out for Delivery":
            order["status"] = "Delivered"
            order_status[order_id] = "Delivered"
            for d in drivers:
                if d["name"] == order["driver"]:
                    d["available"] = True

    root.after(2000, update_status)

# Administrator dashboard with reporting
def open_admin_dashboard():
    if current_user != "admin":
        messagebox.showwarning("Access Denied", "Admin access required.")
        return

    win = tk.Toplevel(root)
    win.title("Admin Dashboard")
    win.geometry("800x600")
    win.configure(bg="white")

    tk.Label(win, text="Admin Dashboard", font=("Helvetica", 16, "bold"), bg="white").pack(pady=10)

    # Inventory Management
    tk.Label(win, text="Inventory Levels", font=("Helvetica", 12, "bold"), bg="white").pack(pady=5)
    tree = ttk.Treeview(win, columns=("Item", "Stock", "Price"), show="headings")
    tree.heading("Item", text="Item")
    tree.heading("Stock", text="Stock")
    tree.heading("Price", text="Price")
    for item, data in inventory.items():
        tree.insert("", "end", values=(item, data["stock"], f"${data['price']}"))
    tree.pack(pady=5)

    def adjust_inventory():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Selection Required", "Please select an item to adjust.")
            return
        item = tree.item(selected[0])["values"][0]
        adjust_win = tk.Toplevel(win)
        adjust_win.title(f"Adjust {item}")
        adjust_win.geometry("200x150")
        adjust_win.configure(bg="white")

        tk.Label(adjust_win, text=f"Current Stock: {inventory[item]['stock']}", bg="white").pack(pady=5)
        tk.Label(adjust_win, text="Adjust by:", bg="white").pack()
        adjust_entry = tk.Entry(adjust_win)
        adjust_entry.pack()

        def apply_adjustment():
            try:
                adjustment = int(adjust_entry.get())
                inventory[item]["stock"] += adjustment
                if inventory[item]["stock"] < 0:
                    inventory[item]["stock"] = 0
                tree.item(selected[0], values=(item, inventory[item]["stock"], f"${inventory[item]['price']}"))
                messagebox.showinfo("Adjustment", f"Stock for {item} adjusted to {inventory[item]['stock']}")
                adjust_win.destroy()
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid number.")

        tk.Button(adjust_win, text="Apply", command=apply_adjustment, bg="lightgreen").pack(pady=10)

    tk.Button(win, text="Adjust Selected Item", command=adjust_inventory, bg="lightblue").pack(pady=5)

    # Active Orders
    tk.Label(win, text="Active Orders", font=("Helvetica", 12, "bold"), bg="white").pack(pady=5)
    for order in orders:
        if order["status"] != "Delivered":
            tk.Label(win, text=f"Order {order['id']}: {order['status']} - Driver: {order['driver'] or 'Not Assigned'}", bg="white").pack(anchor="w", padx=20)

    # Basic Reporting
    tk.Label(win, text="Reports", font=("Helvetica", 12, "bold"), bg="white").pack(pady=5)
    total_orders = len(orders)
    total_revenue = sum(o["total"] for o in orders)
    tk.Label(win, text=f"Total Orders: {total_orders}", bg="white").pack(anchor="w", padx=20)
    tk.Label(win, text=f"Total Revenue: ${total_revenue:.2f}", bg="white").pack(anchor="w", padx=20)

    def generate_detailed_report():
        report_win = tk.Toplevel(win)
        report_win.title("Detailed Report")
        report_win.geometry("400x300")
        report_win.configure(bg="white")

        tk.Label(report_win, text="Detailed Report", font=("Helvetica", 14, "bold"), bg="white").pack(pady=10)
        tk.Label(report_win, text=f"Total Orders: {total_orders}", bg="white").pack(anchor="w", padx=20)
        tk.Label(report_win, text=f"Total Revenue: ${total_revenue:.2f}", bg="white").pack(anchor="w", padx=20)
        tk.Label(report_win, text="Top Items Sold:", bg="white").pack(anchor="w", padx=20)
        
        item_counts = {}
        for order in orders:
            for cat, items in order["items"].items():
                for name, _, qty in items:
                    item_counts[name] = item_counts.get(name, 0) + qty
        top_items = sorted(item_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        for item, count in top_items:
            tk.Label(report_win, text=f"{item}: {count} units", bg="white").pack(anchor="w", padx=40)

    tk.Button(win, text="Generate Detailed Report", command=generate_detailed_report, bg="lightblue").pack(pady=5)

# UI Layout
header = tk.Frame(root, bg="#ffffff", height=60)
header.pack(fill="x", padx=10, pady=5)

tk.Label(header, text="apm", font=("Helvetica", 20, "bold"), fg="green", bg="white").pack(side="left", padx=10)
tk.Label(header, text="Delivery in 10 minutes\nJersey City, New Jersey, U.S.A", font=("Helvetica", 10), bg="white").pack(side="left", padx=10)

tk.Entry(header, width=40, font=("Helvetica", 12)).pack(side="left", padx=10)
tk.Button(header, text="Login", command=open_login).pack(side="left", padx=10)
tk.Button(header, text="Profile", command=open_profile).pack(side="left", padx=10)
tk.Button(header, text="🛒 My Cart", command=open_checkout, bg="white").pack(side="left", padx=10)
tk.Button(header, text="Order History", command=open_order_history, bg="white").pack(side="left", padx=10)
tk.Button(header, text="Admin", command=open_admin_dashboard, bg="white").pack(side="left", padx=10)

banner = tk.Frame(root, bg="#a3e635", height=120)
banner.pack(fill="x", padx=20, pady=10)

tk.Label(banner, text="ultra fast delivery Your time Our Priority", font=("Helvetica", 18, "bold"), bg="#a3e635").pack(anchor="w", padx=20)
tk.Label(banner, text="Your favourite and ultra fast delivery is now online", font=("Helvetica", 12), bg="#a3e635").pack(anchor="w", padx=20)
tk.Button(banner, text="Shop Now", bg="white", fg="green").pack(anchor="w", padx=20, pady=5)

section_frame = tk.Frame(root, bg="white")
section_frame.pack(pady=10)

def create_section(parent, title, desc, color):
    frame = tk.Frame(parent, bg=color, width=300, height=100)
    frame.pack_propagate(False)
    frame.pack(side="left", padx=10)
    tk.Label(frame, text=title, font=("Helvetica", 12, "bold"), bg=color).pack(anchor="w", padx=10)
    tk.Label(frame, text=desc, font=("Helvetica", 10), bg=color).pack(anchor="w", padx=10)
    tk.Button(frame, text="Order Now", bg="white").pack(padx=10, pady=5)

create_section(section_frame, "Pharmacy at your doorstep!", "Cough syrups, pain relief sprays & more", "#ccfbf1")
create_section(section_frame, "Pet Care supplies in minutes", "Food, treats, toys & more", "#fef08a")
create_section(section_frame, "No time for last minute shopping?", "Get all the essentials in minutes", "#ddd6fe")

tk.Label(root, text="Explore Categories", font=("Helvetica", 14, "bold"), bg="white").pack(anchor="w", padx=20)

cat_frame = tk.Frame(root, bg="white")
cat_frame.pack(pady=10)

for i, cat in enumerate(category_items):
    frame = tk.Frame(cat_frame, bg="#f9fafb", bd=1, relief="solid", width=150, height=80)
    frame.pack_propagate(False)
    frame.grid(row=i//5, column=i%5, padx=10, pady=10)
    btn = tk.Button(frame, text=cat, wraplength=120, justify="center", font=("Helvetica", 9),
                    command=lambda c=cat: open_category_window(c, category_items[c]))
    btn.pack(expand=True)

root.mainloop()