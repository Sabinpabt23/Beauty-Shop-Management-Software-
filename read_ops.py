'''
Module responsible for loading product data from a file into a dictionary.
Each product has attributes such as name, brand, stock level, cost, and country of origin.
'''

products = {}  # Dictionary to store product details

def load_products():
    '''
    Loads product information from 'products.txt'.
    The file should contain comma-separated values in the format: Name, Brand, Stock, Cost, Country.
    Each line represents a single product.
    '''
    try:
        with open("products.txt", "r") as file:  # Open the file in read mode
            product_id = 1  # Initialize product ID counter
            for line in file:
                parts = line.replace('\n', '').split(", ")  # Remove newline and split line into components
                if len(parts) == 5:  # Ensure correct data format
                    products[product_id] = {
                        "name": parts[0],  # Product name
                        "brand": parts[1],  # Product brand
                        "stock": int(parts[2]),  # Stock quantity (converted to integer)
                        "cost": float(parts[3]),  # Cost price (converted to float)
                        "country": parts[4]  # Country of origin
                    }
                    product_id += 1  # Increment product ID for the next entry
    except:
        print("Could not load products")  # Handle file reading errors gracefully
