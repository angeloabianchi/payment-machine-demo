import luhn
import random
from django.http import JsonResponse
from .models import Transaction


# Function to validate the card number using the Luhn algorithm
def validate_card(card_number):
    return luhn.verify(str(card_number))

# Function to simulate a bank payment process
def process_bank_payment():
    # For demo purposes, we'll simulate success/failure randomly
    return random.choice([True, False])

# Function to calculate change for a given amount of cash
def calculate_change(amount, coin_types):

    # List of coin values in euro cents, ordered from highest to lowest
    euro_coins = [20000, 10000, 5000, 1000, 500, 200, 100, 50, 20, 10, 5, 2, 1]
    amount_received = 0
    index = 0               #Index to track current coin in euro_coins list
    amount = int(amount)    # Ensure the amount is an integer

    # Calculate total received amount
    for coin_value, coin_count in coin_types.items():
        amount_received = amount_received + (int(coin_value) * coin_count)

    # Validate and calculate the change
    if amount_received > amount:
        change = amount_received - amount
        change_coins = {}

        # Calculate the change distribution
        while change > 0:
            coin_amount = int(change / euro_coins[index])
            change = change % euro_coins[index]
            if coin_amount != 0:
                change_coins[euro_coins[index]] = coin_amount
            index = index + 1

        return {
            "success": True,
            "change": amount_received - amount,
            "coin_types": change_coins
        }

    # If the received amount is insufficient, return an error response
    else:
        return {"success": False, "error": "Insufficient cash"}
