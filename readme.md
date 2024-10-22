# Payment Machine Demo
 A Django-based payment processing system that handles both card and cash payments with a user-friendly interface.

## Features

- Card payment processing with Luhn algorithm validation
- Cash payment processing with automatic change calculation
- Transaction history tracking
- Simple web interface for payment processing
- RESTful API endpoints

## Prerequisites

- Python 3.12.3
- Django 5.1.2
- SQLite (included with Django)

### Installing Python

If you do not have Python installed, you can install it with the following commands:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip
```

## Project Structure
```plaintext
payment-machine-demo/
├── payment/
│   ├── templates/    # HTML templates
│   ├── models.py     # Database models
│   ├── test_payments.py     # Testing
│   ├── urls.py       # URL routing
│   ├── utils.py      # Utility functions for payments
│   └── views.py      # Payment processing and API views
├── payment_machine_demo/
│   ├── settings.py   # Project settings
│   ├── urls.py       # Main URL configuration
│   └── wsgi.py       # WSGI configuration
├── static/
│   ├── css/          # StylesheetsAC
│   └── js/           # JavaScript files
├── manage.py         # Django management script
├── requirements.txt  # Project dependencies
└── .env              # Environment variables
```
## Installation

1. Clone the repository

```bash
git clone https://github.com/angeloabianchi/payment-machine-demo.git
cd payment-machine-demo
```

2. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```
3. Install dependencies

```bash
pip install -r requirements.txt
```
4. Set up environment variables

- Create a .env file in the root directory
- Add the following variables:
```
SECRET_KEY=your_secret_key_here
```
You can generate a new secret key using Python:

```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
5. Run migrations

```bash
python manage.py migrate
```
6. Start the development server
```
python manage.py runserver
```
## Testing

### UI Testing with Selenium

The project includes automated UI tests using Selenium WebDriver. These tests verify the functionality of the payment form interface and payment processing.

### Test Setup Requirements

1. Install Selenium WebDriver:
```
pip install selenium
```
2. Install Webdriver
```
pip install webdriver-manager
```
### Running the Tests

Execute the UI tests using:

```bash
python manage.py test payment.test_payment
```

### Test Coverage

The Selenium tests include:

1. Payment Form Elements Test

- Verifies presence and visibility of basic form elements
- Tests amount field, payment method selector, and currency field

2. Payment Method Switching Test

- Tests switching between card and cash payment methods
- Verifies appropriate form sections are displayed/hidden

3. Card Payment Processing Test

- Tests card payment submission
- Validates form submission and response handling
- Verifies JSON response format and success status

4. Cash Payment Processing Test

- Tests cash payment submission with bill denominations
- Validates change calculation
- Verifies response format and change amount

## API Endpoints

```plaintext
POST   /api/payment/card        # Process card payments
POST   /api/payment/cash        # Process cash payments
GET    /api/transactions        # Get all transactions
GET    /api/transactions/{id}   # Get transaction by ID
```

## Usage Examples

### Card Payment

```json
{
    "amount": 14527,
    "currency": "eur",
    "card_num": 4000000000001000
}
```

### Cash Payment

```json
{
    "amount": 14527,
    "currency": "eur",
    "coin_types": {
        "10000": 2
    }
}
```
## Web Interface

The project includes a web interface for processing payments and viewing transactions. Access it at:
```
http://localhost:8000/api/payment-form/
```
## Future Improvements

1. Features

- Support multiple currencies
- Real bank integration

2. Testing

- Add integration tests

## Dependencies
```plaintext
asgiref==3.8.1
certifi==2024.8.30
charset-normalizer==3.4.0
Django==5.1.2
djangorestframework==3.15.2
idna==3.10
luhn==0.2.0
python-decouple==3.8
requests==2.32.3
sqlparse==0.5.1
urllib3==2.2.3
```
