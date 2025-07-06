'''
This module provides utility functions for handling product data,
saving inventory updates, and generating restock invoices.
'''

from datetime import datetime  # Import datetime for timestamp generation
from read_ops import products  # Import product data

def datefunction():
    '''
    Generates a timestamp in the format YYYYMMDDHHMM.
    This ensures a unique identifier for invoices and records.
    '''
    now = datetime.now()
    return str(now.year) + str(now.month).zfill(2) + str(now.day).zfill(2) + str(now.hour).zfill(2) + str(now.minute).zfill(2)

def save_products():
    '''
    Saves the current product inventory to "products.txt".
    Ensures product details are written in a consistent format: Name, Brand, Stock, Cost, Country.
    '''
    try:
        with open("products.txt", "w") as file:  # Open file in write mode
            for product_id in products:
                p = products[product_id]
                file.write(
                    p["name"] + ", " +  # Product name
                    p["brand"] + ", " +  # Brand name
                    str(p["stock"]) + ", " +  # Available stock quantity
                    str(p["cost"]) + ", " +  # Cost price
                    p["country"] + "\n"  # Country of origin
                )
    except:
        print("Could not save products")  # Handle file write errors gracefully

def generate_restock_invoice(session_items, vendor_name):
    '''
    Generates a restock invoice based on the supplied items and vendor details.
    Saves the invoice to a uniquely named text file using the vendor name and timestamp.
    '''
    timestamp = datefunction()  # Generate timestamp for uniqueness
    invoice = "-" * 50 + "\n"
    invoice += "RESTOCK INVOICE - " + timestamp + "\n"
    invoice += "Vendor: " + vendor_name + "\n"
    invoice += "-" * 50 + "\n"
    invoice += "Product\t\tBrand\t\tQty\tRate\tAmount\n"
    invoice += "-" * 50 + "\n"

    grand_total = 0  # Initialize total cost accumulator
    for item in session_items:
        product_id = item[0]  # Extract product ID
        amount = item[1]  # Extract quantity restocked
        total_cost = item[2]  # Extract total cost
        p = products[product_id]

        invoice += (
            p["name"] + "\t" +  # Product name
            p["brand"] + "\t" +  # Brand name
            str(amount) + "\t" +  # Quantity restocked
            str(p["cost"]) + "\t" +  # Unit price
            str(total_cost) + "\n"  # Total cost
        )
        grand_total += total_cost  # Accumulate grand total

    invoice += "-" * 50 + "\n"
    invoice += "TOTAL:\t\t\t\t\t\t" + str(grand_total) + "\n"
    invoice += "-" * 50 + "\n"

    filename = "restock_" + vendor_name.replace(" ", "_") + "_" + timestamp + ".txt"
    try:
        with open(filename, "w") as f:
            f.write(invoice)  # Save invoice to file
        print("Restock invoice saved as " + filename)
    except:
        print("Error saving restock invoice")  # Handle file write errors gracefully
