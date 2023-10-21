import math
from scipy.optimize import fsolve

# Converts a string with commas to a float
def string_to_float(s):
    return float(s.replace(',', ''))

# Equation for logistic function based on R.
def logistic_function(R, initial_value, L, current_value, time_difference):
    c = L / initial_value - 1
    return current_value - (L / (1 + c * math.exp(-R * time_difference)))

# Calculate R for linear function given initial value, buy date, current value, and current date.
def calculate_linear_R(initial_value, buy_date, current_value, current_date):
    return (current_value - initial_value) / (current_date - buy_date)

# Calculate R for exponential function given initial value, buy date, current value, and current date.
def calculate_exponential_R(initial_value, buy_date, current_value, current_date):
    if current_date == buy_date:
        return 0
    return (current_value / initial_value) ** (1 / (current_date - buy_date)) - 1

# Calculate R for logistic function given initial value, buy date, current value, and current date.
def calculate_logistic_R(initial_value, buy_date, current_value, current_date):
    L = 2 * initial_value  # Assumption
    time_difference = current_date - buy_date  # This will already give T in terms of years
    
    # Solve for R using the previously defined logistic_function
    R, = fsolve(logistic_function, 0.05, args=(initial_value, L, current_value, time_difference))
    return R

# Get parameters for a function type given initial value, buy date, and current value.
def get_parameters_from_values(function_type):
    initial_value = string_to_float(input("Enter the initial value of the asset: "))
    buy_date = float(input("Enter the buy date (as a year, e.g., 2020): "))
    current_value = string_to_float(input("Enter the current value of the asset: "))
    current_date = float(input("Enter the current date (as a year, e.g., 2023): "))
    time_difference = current_date - buy_date  # T in terms of years
    
    if function_type == "linear":
        R, c = calculate_linear_R(initial_value, buy_date, current_value, current_date), current_value - calculate_linear_R(initial_value, buy_date, current_value, current_date) * current_date
        return R, c
    elif function_type == "exponential":
        c, R = initial_value, calculate_exponential_R(initial_value, buy_date, current_value, current_date)
        return c, R
    elif function_type == "logistic":
        c, R, L = initial_value, calculate_logistic_R(initial_value, buy_date, current_value, current_date), 2 * current_value
        return c, R, L

# Get parameters for linear equation
def get_linear_parameters():
    choice = input("Enter parameters using (1) current value or (2) initial value, buy date, and current value: ")
    if choice == '1':
        R = float(input("Enter the growth/decay rate (R): "))
        c = float(input("Enter the current value of the asset (c): "))
    elif choice == '2':
        R, c = get_parameters_from_values("linear")
    else:
        print("Invalid choice. Using default method (current value).")
        R = float(input("Enter the growth/decay rate (R): "))
        c = float(input("Enter the current value of the asset (c): "))
    return f"y = {R}T + {c}"

# Get parameters for exponential equation
def get_exponential_parameters():
    choice = input("Enter parameters using (1) current value or (2) initial value, buy date, and current value: ")
    if choice == '1':
        c = float(input("Enter the current value of the asset (c): "))
        R = float(input("Enter the growth/decay factor (R): "))
    elif choice == '2':
        c, R = get_parameters_from_values("exponential")
    else:
        print("Invalid choice. Using default method (current value).")
        c = float(input("Enter the current value of the asset (c): "))
        R = float(input("Enter the growth/decay factor (R): "))
    return f"y = {c} * (1 + {R})^T"

# Get parameters for logistic equation
def get_logistic_parameters():
    choice = input("Enter parameters using (1) current value or (2) initial value, buy date, and current value: ")
    if choice == '1':
        c = float(input("Enter the current value of the asset (c): "))
        R = float(input("Enter the growth/decay rate (R): "))
        L = float(input("Enter the limit (maximum/minimum value of asset) (L): "))
    elif choice == '2':
        c, R, L = get_parameters_from_values("logistic")
    else:
        print("Invalid choice. Using default method (current value).")
        c = float(input("Enter the current value of the asset (c): "))
        R = float(input("Enter the growth/decay rate (R): "))
        L = float(input("Enter the limit (maximum/minimum value of asset) (L): "))
    return f"y = {L} / (1 + {c} * e^(-{R} * T))"


def get_equation():
    # List of common assets
    asset_options = ["house", "car", "stock", "land", "jewelry", "custom"]
    
    # Ask for asset
    print("Choose an asset from the following list:")
    for idx, asset_choice in enumerate(asset_options, 1):
        print(f"{idx}. {asset_choice.capitalize()}")
    
    asset_choice = input("Enter your choice (number or asset name): ").lower()
    while asset_choice not in asset_options and asset_choice not in map(str, range(1, len(asset_options) + 1)):
        print("Invalid choice. Please select from the list above.")
        asset_choice = input("Enter your choice (number or asset name): ").lower()
    
    if asset_choice == "custom" or asset_choice == "6":
        asset = input("Enter the name of your custom asset: ").lower()
    else:
        if asset_choice.isdigit():
            asset = asset_options[int(asset_choice) - 1]
        else:
            asset = asset_choice

    # Ask for function type
    function = input("Choose a function (linear/exponential/logistic): ").lower()
    while function not in ["linear", "exponential", "logistic"]:
        print("Invalid function. Please choose between 'linear', 'exponential', or 'logistic'.")
        function = input("Choose a function (linear/exponential/logistic): ").lower()

    # Get parameters based on function
    if function == "linear":
        equation = get_linear_parameters()
    elif function == "exponential":
        equation = get_exponential_parameters()
    elif function == "logistic":
        equation = get_logistic_parameters()

    # Display custom equation
    print(f"Custom equation for {asset}: {equation}")


get_equation()
