# Chambers.Naomi-POS-ITT103-SP2026.py

SALES_TAX_RATE = 0.10
DISCOUNT_RATE = 0.05
DISCOUNT_THRESHOLD = 5000.00


def create_product_catalog():
    """Create and return the product catalog."""
    return {
        "Rice": {"price": 350.00, "stock": 20},
        "Sugar": {"price": 180.00, "stock": 15},
        "Flour": {"price": 220.00, "stock": 12},
        "Milk": {"price": 280.00, "stock": 10},
        "Bread": {"price": 200.00, "stock": 8},
        "Eggs": {"price": 450.00, "stock": 14},
        "Butter": {"price": 300.00, "stock": 6},
        "Cheese": {"price": 500.00, "stock": 7},
        "Juice": {"price": 250.00, "stock": 9},
        "Soap": {"price": 150.00, "stock": 11}
    }


def display_products(products):
    """Display all products in the catalog."""
    print("\n================ PRODUCT CATALOG ================")
    print("{'Product':<15}{'Price (JMD)':<15}{'Stock':<10}")
    print("-" * 42)

    for product_name, details in products.items():
        print("{product_name:<15}{details['price']:<15.2f}{details['stock']:<10}")

    print("-" * 42)
    display_low_stock_alert(products)


def display_low_stock_alert(products):
    """Display low-stock alerts for products below 5."""
    low_stock_items = []

    for product_name, details in products.items():
        if details["stock"] < 5:
            low_stock_items.append(product_name)

    if low_stock_items:
        print("\n*** LOW STOCK ALERT ***")
        for item in low_stock_items:
            print("- {item} is low on stock ({products[item]['stock']} remaining)")


def add_to_cart(products, cart):
    """Add items to the shopping cart."""
    product_name = input("Enter product name to add: ").strip().title()

    if product_name not in products:
        print("Product not found in catalog.")
        return

    if products[product_name]["stock"] == 0:
        print("Sorry, this item is out of stock.")
        return

    try:
        quantity = int(input("Enter quantity: "))
        if quantity <= 0:
            print("Quantity must be greater than 0.")
            return
    except ValueError:
        print("Invalid input. Please enter a whole number.")
        return

    available_stock = products[product_name]["stock"]

    if quantity > available_stock:
        print("Not enough stock available. Only {available_stock} left.")
        return

    if product_name in cart:
        cart[product_name]["quantity"] += quantity
    else:
        cart[product_name] = {
            "price": products[product_name]["price"],
            "quantity": quantity
        }

    products[product_name]["stock"] -= quantity
    print(f"{quantity} x {product_name} added to cart.")


def remove_from_cart(products, cart):
    """Remove items from the shopping cart."""
    if not cart:
        print("Cart is empty.")
        return

    product_name = input("Enter product name to remove: ").strip().title()

    if product_name not in cart:
        print("Item not found in cart.")
        return

    try:
        quantity = int(input("Enter quantity to remove: "))
        if quantity <= 0:
            print("Quantity must be greater than 0.")
            return
    except ValueError:
        print("Invalid input. Please enter a whole number.")
        return

    if quantity >= cart[product_name]["quantity"]:
        removed_quantity = cart[product_name]["quantity"]
        products[product_name]["stock"] += removed_quantity
        del cart[product_name]
        print(f"{product_name} removed completely from cart.")
    else:
        cart[product_name]["quantity"] -= quantity
        products[product_name]["stock"] += quantity
        print(f"{quantity} x {product_name} removed from cart.")


def view_cart(cart):
    """Display cart contents."""
    if not cart:
        print("\nCart is empty.")
        return

    print("\n================ SHOPPING CART ================")
    print("{'Product':<15}{'Qty':<10}{'Unit Price':<15}{'Total':<15}")
    print("-" * 55)

    cart_total = 0

    for product_name, details in cart.items():
        item_total = details["price"] * details["quantity"]
        cart_total += item_total
        print("{product_name:<15}{details['quantity']:<10}{details['price']:<15.2f}{item_total:<15.2f}")

    print("-" * 55)
    print("{'Cart Total:':<40}{cart_total:.2f}")


def calculate_totals(cart):
    """Calculate subtotal, discount, tax, and total."""
    subtotal = 0

    for details in cart.values():
        subtotal += details["price"] * details["quantity"]

    discount = 0
    if subtotal > DISCOUNT_THRESHOLD:
        discount = subtotal * DISCOUNT_RATE

    discounted_subtotal = subtotal - discount
    sales_tax = discounted_subtotal * SALES_TAX_RATE
    total_due = discounted_subtotal + sales_tax

    return subtotal, discount, sales_tax, total_due


def process_payment(total_due):
    """Handle payment and calculate change."""
    while True:
        try:
            amount_paid = float(input(f"Enter amount received (Total due: {total_due:.2f}): "))
            if amount_paid < total_due:
                print("Insufficient payment. Customer cannot pay less than the total due.")
            elif amount_paid <= 0:
                print("Amount must be greater than 0.")
            else:
                change = amount_paid - total_due
                return amount_paid, change
        except ValueError:
            print("Invalid input. Please enter a numeric value.")


def generate_receipt(cart, subtotal, discount, sales_tax, total_due, amount_paid, change):
    """Display a formatted receipt."""
    print("\n")
    print("=" * 52)
    print("               UCC CAMPUS STORE")
    print("                 SALES RECEIPT")
    print("=" * 52)
    print(f"{'Item':<15}{'Qty':<8}{'Unit Price':<12}{'Total':<12}")
    print("-" * 52)

    for product_name, details in cart.items():
        item_total = details["price"] * details["quantity"]
        print("{product_name:<15}{details['quantity']:<8}{details['price']:<12.2f}{item_total:<12.2f}")

    print("-" * 52)
    print("{'Subtotal:':<30}{subtotal:>20.2f}")
    print("{'Discount:':<30}{discount:>20.2f}")
    print("{'Sales Tax (10%):':<30}{sales_tax:>20.2f}")
    print("{'Total Due:':<30}{total_due:>20.2f}")
    print("{'Amount Paid:':<30}{amount_paid:>20.2f}")
    print("{'Change:':<30}{change:>20.2f}")
    print("=" * 52)
    print("         Thank you for shopping with us!")
    print("=" * 52)


def checkout(cart):
    """Complete the checkout process."""
    if not cart:
        print("Cart is empty. Cannot checkout.")
        return False

    subtotal, discount, sales_tax, total_due = calculate_totals(cart)

    print("\n================ CHECKOUT ================")
    print("Subtotal:      {subtotal:.2f}")
    print("Discount:      {discount:.2f}")
    print("Sales Tax:     {sales_tax:.2f}")
    print("Total Due:     {total_due:.2f}")

    amount_paid, change = process_payment(total_due)
    generate_receipt(cart, subtotal, discount, sales_tax, total_due, amount_paid, change)

    cart.clear()
    return True


def transaction_menu(products):
    """Handle a single customer transaction."""
    cart = {}

    while True:
        print("\n=============== POS MAIN MENU ===============")
        print("1. Display Products")
        print("2. Add Item to Cart")
        print("3. Remove Item from Cart")
        print("4. View Cart")
        print("5. Checkout")
        print("6. Cancel Transaction")
        print("=============================================")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            display_products(products)
        elif choice == "2":
            add_to_cart(products, cart)
        elif choice == "3":
            remove_from_cart(products, cart)
        elif choice == "4":
            view_cart(cart)
        elif choice == "5":
            completed = checkout(cart)
            if completed:
                break
        elif choice == "6":
            if cart:
                for product_name, details in cart.items():
                    products[product_name]["stock"] += details["quantity"]
                cart.clear()
            print("Transaction cancelled.")
            break
        else:
            print("Invalid choice. Please select a valid menu option.")


def main():
    """Run the POS system with multiple transactions."""
    products = create_product_catalog()

    print("Welcome to the Point of Sale (POS) System")

    while True:
        transaction_menu(products)

        again = input("/nWould you like to process another transaction? (yes/no): ").strip().lower()
        if again != "yes":
            print("System closed. Goodbye.")
            break


if __name__ == "__main__":
    main()
