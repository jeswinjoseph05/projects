car_inventory = {
    "1": {"name": "Toyota Corolla", "price": 20000},
    "2": {"name": "Honda Civic", "price": 22000},
    "3": {"name": "Ford Mustang", "price": 30000},
    "4": {"name": "Tesla Model 3", "price": 40000}
}


print("🚗 Welcome to the Python Car Shop!")
name = input("Enter your name: ")
budget = float(input(f"Hi {name}, what's your total budget? $"))

cart = []
total_cost = 0

while True:
    print("\nAvailable cars:")
    for key, car in car_inventory.items():
        print(f"{key}. {car['name']} - ${car['price']}")
    
    choice = input("Enter the number of the car you want to buy: ")
    
    if choice.lower() == "exit":
        break
    
    if choice in car_inventory:
        selected_car = car_inventory[choice]
        if total_cost + selected_car["price"] <= budget:
            cart.append(selected_car["name"])
            total_cost += selected_car["price"]
            print(f"✅ {selected_car['name']} added to your cart. Total so far: ${total_cost}")
        else:
            print("You don't have enough budget for this car.")
    else:
        print("❗ Invalid choice. Please try again.")

 
    continue_choice = input("Do you want to buy another car? (yes/no): ").lower()
    if continue_choice != "yes":
        break


print("\n🧾 Purchase Summary:")
if cart:
    for ild, car in enumerate(cart, 1):
        print(f"{ild}. {car}")
    print(f"Total cost: ${total_cost}")
    print(f"Remaining budget: ${budget - total_cost}")
else:
    print("You didn't buy any cars.")

print("\n🚘 Thank you for visiting Python Car Shop!")
