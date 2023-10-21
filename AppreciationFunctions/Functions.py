import math

# Enter parameters for a linear, exponential, or logistic function
def get_linear_parameters():
    m = float(input("Enter the growth/decay rate (m): "))
    c = float(input("Enter the current value of the asset (c): "))
    return f"y = {m}x + {c}"

def get_exponential_parameters():
    a = float(input("Enter the current value of the asset (a): "))
    b = float(input("Enter the growth/decay factor (b): "))
    return f"y = {a} * {b}^x"

def get_logistic_parameters():
    a = float(input("Enter the current value of the asset (a): "))
    b = float(input("Enter the growth/decay rate (b): "))
    c = float(input("Enter the limit (maximum value of asset) (c): "))
    return f"y = {c} / (1 + {a} * e^(-{b} * x))"

# Get and display equation
def get_equation():
    # Ask for asset
    asset = input("Choose an asset (house, car, etc.): ").lower()

    # Ask for function
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
