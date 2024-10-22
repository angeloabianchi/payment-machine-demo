from django.shortcuts import render
import json
import requests
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .utils import validate_card, calculate_change, process_bank_payment
from .models import Transaction

# Render the payment form page
def payment_form(request):
    return render(request, 'payment_form.html')

# Process the payment request based on the provided payment method.
def process_payment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            payment_method = data.get('payment_method')
            amount = data.get('amount')
            currency = data.get('currency', 'eur')

            # Process card payment
            if payment_method == 'card':
                card_num = data.get('card_num')
                payment_data = {
                    'amount': amount,
                    'currency': currency,
                    'card_num': card_num
                }
                response = requests.post('http://localhost:8000/api/payment/card', json=payment_data)

            # Process cash payment
            else:
                coin_types = data.get('coin_types')

                if not coin_types:
                    return JsonResponse({'success': False, 'error': 'coin_types not provided'})

                payment_data = {
                    'amount': amount,
                    'currency': currency,
                    'coin_types': coin_types  # Already in dictionary format, no need to parse
                }
                response = requests.post('http://localhost:8000/api/payment/cash', json=payment_data)

            return JsonResponse(response.json())
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON data'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

# Validates card information, processes the payment with the bank, and saves the transaction.
@api_view(['POST'])
def card_payment(request):

    try:
        data = json.loads(request.body)
        amount = data['amount']
        currency = data['currency']
        success = False
        error_code = None

        if 'card_num' in data:
            # Validate currency
            if currency == 'eur':
                card_num = data['card_num']

                # Validate card number
                if validate_card(card_num):
                    # Process bank payment
                    bank_response = process_bank_payment()
                else:
                    return JsonResponse({"success": False, "error": 702})
            else:
                return JsonResponse({"success": False, "error": "This machine only accepts EUR"})

        # Save the transaction
        transaction = Transaction(
            payment_method = 'card',
            amount = amount,
            currency = currency,
            success = bank_response,
            error_code = None if bank_response else 702,
        )
        transaction.save()

        if bank_response:
            return JsonResponse({"success": True, "message": "Payment Confirmed"})
        else:
            return JsonResponse({"success": False, "error": "Please check your bank balance and try again!"})

    except (KeyError, ValueError, json.JSONDecodeError):
        return JsonResponse({"success": False, "error": "Invalid data"})

# Calculates change, validates the input, and saves the transaction.
@api_view(['POST'])
def cash_payment(request):

    # Define error codes
    ERROR_CODES = {
        'INSUFFICIENT_CASH': 701,
        'INVALID_AMOUNT': 702,
        'INVALID_CURRENCY': 703,
        'INVALID_COIN_TYPES': 704,
        'MISSING_DATA': 705
    }

    try:
        data = json.loads(request.body)
        currency = data.get('currency')
        amount = data.get('amount')

        if not amount:
            return JsonResponse({"success": False, "error": "Amount is required"})

        if 'coin_types' in data:
            if currency == 'eur':
                coin_types = data['coin_types']
                if not isinstance(coin_types, dict):
                    return JsonResponse({"success": False, "error": "Invalid coin_types format"})

                change = calculate_change(amount, coin_types)

                # Map the error message to error code if the change calculation failed
                if not change["success"]:
                    error_code = ERROR_CODES['INSUFFICIENT_CASH']
                    if change.get("error") == "Invalid amount":
                        error_code = ERROR_CODES['INVALID_AMOUNT']
                    elif change.get("error") == "Invalid coin types":
                        error_code = ERROR_CODES['INVALID_COIN_TYPES']

                    transaction = Transaction(
                        payment_method='cash',
                        amount=amount,
                        currency=currency,
                        success=False,
                        error_code=error_code,
                        change_amount=None,
                        coin_types=None,
                    )
                    transaction.save()

                    return JsonResponse({
                        "success": False,
                        "error": change.get("error"),
                        "error_code": error_code
                    })

                # If successful, save the transaction
                transaction = Transaction(
                    payment_method='cash',
                    amount=amount,
                    currency=currency,
                    success=True,
                    error_code=None,
                    change_amount=change.get("amount"),
                    coin_types=change.get("coin_types")
                )
                transaction.save()

                return JsonResponse(change)
            else:
                return JsonResponse({"success": False, "error": "This machine only accepts EUR"})

        return JsonResponse({"success": False, "error": "coin_types not provided"})

    except (KeyError, ValueError, json.JSONDecodeError) as e:
        return JsonResponse({"success": False, "error": str(e)})
    except Exception as e:
        return JsonResponse({"success": False, "error": f"Unexpected error: {str(e)}"})


# Get all transactions
@api_view(['GET'])
def get_transactions(request):
    transactions = Transaction.objects.all().values()
    return JsonResponse({"transactions": list(transactions)})


# Get transaction by ID
@api_view(['GET'])
def get_transaction_by_id(request, transaction_id):
    try:
        transaction = Transaction.objects.get(id=transaction_id)
        transaction_data = {
            "id": transaction.id,
            "payment_method": transaction.payment_method,
            "amount": str(transaction.amount),
            "currency": transaction.currency,
            "success": transaction.success,
            "error_code": transaction.error_code,
            "change_amount": str(transaction.change_amount) if transaction.change_amount else None,
            "coin_types": transaction.coin_types,
        }
        return JsonResponse(transaction_data)
    except Transaction.DoesNotExist:
        return JsonResponse({"success": False, "error": "Transaction not found"}, status=404)
