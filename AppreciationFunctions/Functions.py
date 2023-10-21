import math
from scipy.optimize import fsolve
import openai
import re

# Converts a string with commas to a float
def string_to_float(s):
    return float(s.replace(',', ''))

# Equation for logistic function based on R.
def logistic_function(R, initial_value, L, current_value, time_difference):
    c = L / initial_value - 1
    return current_value - (L / (1 + c * math.exp(-R * time_difference)))

def calculate_linear_R(initial_value, buy_date, current_value, current_date):
    return (current_value - initial_value) / (current_date - buy_date)

def calculate_exponential_R(initial_value, buy_date, current_value, current_date):
    if current_date == buy_date:
        return 0
    return (current_value / initial_value) ** (1 / (current_date - buy_date)) - 1

def calculate_logistic_R(initial_value, buy_date, current_value, current_date):
    L = 2 * initial_value  # Assumption
    time_difference = current_date - buy_date
    
    R, = fsolve(logistic_function, 0.05, args=(initial_value, L, current_value, time_difference))
    return R

# OpenAI API Key
openai.api_key = "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"

# AI Suggested R value
def suggest_R_value(asset, function_type):
    """Suggests a growth/decay R-value based on the type of asset and function and sets R equal to it."""
    messages = [{"role": "system", "content": f"Please provide a {function_type} growth/decay rate, R, for modeling {asset} appreciation/depreciation. Make sure it is realistic and varies with different assets and function types. Make the R value negative if you think the asset depreciates and positive if you think the asset appreciates. Always return an R value."}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=2000,  
    )
    suggested_R_value = response['choices'][0]['message']['content'].strip()
    
    # Extract only the numerical value using regex
    number_matches = re.findall(r"[-+]?\d*\.\d+|\d+", suggested_R_value)
    
    # If no valid numbers are found, raise an exception.
    if not number_matches:
        raise ValueError("Failed to extract a valid number from GPT response.")
    return float(number_matches[0])

def get_parameters_from_values(function_type):
    initial_value = string_to_float(input("Enter the initial value of the asset: "))
    buy_date = float(input("Enter the buy date (as a year, e.g., 2020): "))
    current_value = string_to_float(input("Enter the current value of the asset: "))
    current_date = float(input("Enter the current date (as a year, e.g., 2023): "))
    
    if function_type == "linear":
        R, c = calculate_linear_R(initial_value, buy_date, current_value, current_date), current_value - calculate_linear_R(initial_value, buy_date, current_value, current_date) * current_date
        return R, c
    elif function_type == "exponential":
        c, R = initial_value, calculate_exponential_R(initial_value, buy_date, current_value, current_date)
        return c, R
    elif function_type == "logistic":
        c, R, L = initial_value, calculate_logistic_R(initial_value, buy_date, current_value, current_date), 2 * current_value
        return c, R, L

def get_equation_parameters(function_type, asset):
    choice = input("Enter parameters using:\n" 
                   "(1) current value\n"
                   "(2) initial value, buy date, current value, and current date\n"
                   "(3) current value and AI-suggested R-value\n"
                   "Enter your choice (number): ")
    
    if choice == '1':
        R = float(input("Enter the growth/decay rate (R): "))
        c = float(input("Enter the current value of the asset (c): "))
        if function_type == "linear":
            return R, c
        elif function_type == "exponential":
            return c, R
        elif function_type == "logistic":
            L = float(input("Enter the limit (maximum/minimum value of asset) (L): "))
            return c, R, L

    elif choice == '2':
        return get_parameters_from_values(function_type)

    elif choice == '3':
        current_value = string_to_float(input("Enter the current value of the asset: "))
        R = suggest_R_value(asset, function_type)
        if function_type == "linear":
            c = current_value
            return R, c
        elif function_type == "exponential":
            c = current_value / (1 + R)
            return c, R
        elif function_type == "logistic":
            L = 2 * current_value
            c = L / current_value - 1
            return c, R, L

def get_equation():
    asset = input("Enter the name of your asset: ")
    function = input("Choose a function (linear/exponential/logistic): ").lower()
    while function not in ["linear", "exponential", "logistic"]:
        print("Invalid function. Please choose between 'linear', 'exponential', or 'logistic'.")
        function = input("Choose a function (linear/exponential/logistic): ").lower()

    if function == "linear":
        R, c = get_equation_parameters("linear", asset)
        equation = f"y = {R}T + {c}"

    elif function == "exponential":
        c, R = get_equation_parameters("exponential", asset)
        equation = f"y = {c} * (1 + {R})^T"

    elif function == "logistic":
        c, R, L = get_equation_parameters("logistic", asset)
        equation = f"y = {L} / (1 + {c} * e^(-{R} * T))"

    print(f"Custom equation for {asset}: {equation}")

get_equation()
