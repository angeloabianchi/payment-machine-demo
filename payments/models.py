from django.db import models


class Transaction(models.Model):
    # Define payment method choices for the transaction
    PAYMENT_METHODS = (
        ('card', 'Card'),
        ('cash', 'Cash'),
    )

    # Field to store the payment method used in the transaction (e.g., Card or Cash)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)

    # Field to store the amount of the transaction, with up to 10 digits
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    # Field to store the currency of the transaction (e.g., EUR, USD)
    currency = models.CharField(max_length=3)

    # Boolean field indicating whether the transaction was successful or not
    success = models.BooleanField()

    # Field to store an error code in case the transaction fails (optional)
    error_code = models.IntegerField(null=True, blank=True)

    # Field to store the change amount for cash transactions (optional)
    change_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # JSON field to store coin types for cash transactions (optional)
    coin_types = models.JSONField(null=True, blank=True)

    def __str__(self):
        # Return a string representation of the transaction, including its ID, payment method, and amount
        return f'Transaction {self.id}: {self.payment_method} - {self.amount} {self.currency}'
