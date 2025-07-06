# Import necessary functions from external modules
from read_ops import load_products  # Loads initial product data
from operations import show_products, restock, purchase  # Functions to handle store operations

# Load product data before the main loop starts
load_products()

# Main loop for the store system interface
while True:
    # Display menu header
    print("\n" + "=" * 50)
    print("           WECARE BEAUTY STORE SYSTEM")
    print("=" * 50)
    
    # Provide user options
    print("1. Show Products")  # Display available products
    print("2. Make Purchase")  # Purchase an item
    print("3. Restock Products")  # Replenish stock
    print("4. Exit")  # Exit the program

    # Get user choice as input
    choice = input("Enter your choice (1-4): ")

    # Perform actions based on user choice
    if choice == "1":
        show_products()  # Call function to display products
    elif choice == "2":
        purchase()  # Call function to process purchase
    elif choice == "3":
        restock()  # Call function to restock products
    elif choice == "4":
        print("\nThank you! Goodbye.")  # Exit message
        break  # Terminate loop
    else:
        print("\nInvalid choice! Enter 1-4.")  # Handle invalid input
