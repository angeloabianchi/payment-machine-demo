from django.urls import path
from .views import card_payment, cash_payment, get_transactions, get_transaction_by_id, payment_form, process_payment

urlpatterns = [
    # URL pattern for processing card payments
    path('payment/card', card_payment, name='card_payment'),

    # URL pattern for processing cash payments
    path('payment/cash', cash_payment, name='cash_payment'),

    # URL pattern to retrieve all transactions
    path('transactions', get_transactions, name='get_transactions'),

    # URL pattern to retrieve a specific transaction by its ID
    path('transactions/<int:transaction_id>', get_transaction_by_id, name='get_transaction'),

    # URL pattern to display the payment form
    path('payment-form/', payment_form, name='payment_form'),

    # URL pattern to process the payment submission
    path('process-payment/', process_payment, name='process_payment'),
]
