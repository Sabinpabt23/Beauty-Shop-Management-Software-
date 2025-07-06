'''
This module provides functionalities for displaying available products, 
restocking inventory, and handling customer purchases with invoice generation.
'''

from read_ops import products  # Importing existing product data
from write_ops import save_products, generate_restock_invoice, datefunction  # Functions for saving product data and generating invoices

def show_products():
    '''
    Displays available products in a formatted table.
    The price is calculated as twice the cost of the product.
    '''
    print("\n" + "-" * 50)
    print("ID\tName\t\tBrand\t\tStock\tPrice\tCountry")
    print("-" * 50)
    for product_id in products:
        p = products[product_id]
        price = p["cost"] * 2  # Setting sale price as twice the cost
        print(
            str(product_id) + "\t" +
            p["name"] + "\t" +
            p["brand"] + "\t" +
            str(p["stock"]) + "\t" +
            str(price) + "\t" +
            p["country"]
        )
    print("-" * 50)

def restock():
    '''
    Handles the restocking of products.
    Allows the user to input a product ID, quantity, and vendor details.
    Updates stock levels and generates a restock invoice.
    '''
    session_items = []  # Stores restocked items for invoice generation
    vendor_name = ""  # Vendor name initialization

    while True:
        show_products()
        try:
            product_id = int(input("\nEnter product ID to restock (0 to cancel): "))
            if product_id == 0:
                break
            if product_id not in products:
                print("Invalid product ID!")
                continue
            amount = int(input("How many to add? "))
            if amount <= 0:
                print("Must add at least 1 item!")
                continue
            if vendor_name == "":
                vendor_name = input("Enter vendor/supplier name: ")
                if vendor_name == "":
                    print("Vendor name cannot be empty!")
                    continue

            total_cost = amount * products[product_id]["cost"]  # Calculate total restocking cost
            products[product_id]["stock"] += amount  # Update stock levels
            session_items.append([product_id, amount, total_cost])  # Store transaction details

            print("\nRestocked " + str(amount) + " " + products[product_id]["name"] + ". New stock: " + str(products[product_id]["stock"]))
            save_products()  # Save updated product data

            more = input("\nDo you want to restock another item? (y/n): ").lower()
            if more != "y":
                break
        except ValueError:
            print("Invalid input! Numbers only.")

    if session_items:
        generate_restock_invoice(session_items, vendor_name)  # Generate an invoice for restocked items

def purchase():
    '''
    Handles the customer purchase process.
    Allows users to select products, apply a promotional "Buy 3 Get 1 Free" discount,
    deduct stock accordingly, and generate an invoice.
    '''
    show_products()
    name = input("\nEnter customer name: ")  # Collect customer details
    total = 0  # Initialize total bill amount
    items = []  # List to store purchased items

    print("\n" + "-" * 50)
    print("Item\t\tQty\tFree\tPrice")
    print("-" * 50)

    while True:
        try:
            product_id = int(input("\nEnter product ID (0 to finish): "))
            if product_id == 0:
                break
            if product_id not in products:
                print("Invalid ID! Try again.")
                continue

            p = products[product_id]
            qty = int(input("How many " + p['name'] + "? "))
            if qty <= 0:
                print("Must be at least 1!")
                continue

            free = qty // 3  # Calculate free items based on promotional offer
            required = qty + free
            if required > p["stock"]:
                print("Not enough stock. Available: " + str(p["stock"]) + " (including free items)")
                continue

            p["stock"] -= required  # Deduct stock after purchase
            price = p["cost"] * 2 * qty  # Calculate total price for purchased items
            items.append({"name": p["name"], "qty": qty, "free": free, "price": price})  # Store purchase details
            total += price

            print(p["name"] + "\t" + str(qty) + "\t" + str(free) + "\t" + str(price))
            print("-" * 50)
        except ValueError:
            print("Numbers only please!")

    if items:
        timestamp = datefunction()  # Generate timestamp for invoice
        invoice = "-" * 50 + "\n"
        invoice += "INVOICE - " + timestamp + "\n"
        invoice += "Customer: " + name + "\n"
        invoice += "-" * 50 + "\n"
        invoice += "Item\t\tQty\tFree\tPrice\n"
        invoice += "-" * 50 + "\n"
        for item in items:
            invoice += item['name'] + "\t" + str(item['qty']) + "\t" + str(item['free']) + "\t" + str(item['price']) + "\n"
        invoice += "-" * 50 + "\n"
        invoice += "TOTAL:\t\t\t\t" + str(total) + "\n"
        invoice += "-" * 50 + "\n"

        filename = "invoice_" + name.replace(" ", "_") + "_" + timestamp + ".txt"
        try:
            with open(filename, "w") as f:
                f.write(invoice)
            print("Invoice saved as " + filename)
            save_products()  # Save updated stock levels
        except:
            print("Error saving invoice")
    else:
        print("\nNo items purchased.")
