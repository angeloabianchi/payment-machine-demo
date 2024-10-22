import unittest
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PaymentSystemBasicTests(unittest.TestCase):
    def setUp(self):
        # Set up browser before each test"
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:8000/api/payment-form/")

    def tearDown(self):
        # Close browser after each test
        self.driver.quit()

    def test_payment_form_elements(self):
        # Test that main form elements are present
        # Check if basic form elements exist
        amount_field = self.driver.find_element(By.ID, "amount")
        payment_method = self.driver.find_element(By.ID, "payment-method")
        currency_field = self.driver.find_element(By.ID, "currency")

        # Verify they are displayed
        self.assertTrue(amount_field.is_displayed())
        self.assertTrue(payment_method.is_displayed())
        self.assertTrue(currency_field.is_displayed())

    def test_switch_payment_method(self):
        # Test switching between card and cash payment methods
        # Get payment method dropdown
        payment_method = Select(self.driver.find_element(By.ID, "payment-method"))

        # Switch to cash payment
        payment_method.select_by_value("cash")
        cash_info = self.driver.find_element(By.ID, "cash-info")
        self.assertTrue(cash_info.is_displayed())

        # Switch to card payment
        payment_method.select_by_value("card")
        card_info = self.driver.find_element(By.ID, "card-info")
        self.assertTrue(card_info.is_displayed())

    def test_card_payment(self):
        # Test submitting a basic card payment
        # Fill in amount and card number
        self.driver.find_element(By.ID, "amount").send_keys("100")
        self.driver.find_element(By.ID, "card-number").send_keys("4532015112830366")

        # Submit form
        self.driver.find_element(By.CLASS_NAME, "submit").click()

        # Wait for the response to appear in the browser
        response_container = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "response-container"))
        )

        # Retrieve the JSON response directly from the browser
        response_text = response_container.text

        # Convert text to a dictionary
        json_data = json.loads(response_text)

        # Validate the JSON response
        self.assertEqual(json_data.get('success'), True)
        self.assertIn(json_data.get('message'), ['Payment Confirmed', 'Please check your bank balance and try again!'])

    def test_cash_payment(self):
        #Test submitting a basic cash payment
        # Fill in the payment amount
        self.driver.find_element(By.ID, "amount").send_keys("10000")

        # Select cash as the payment method
        payment_method = Select(self.driver.find_element(By.ID, "payment-method"))
        payment_method.select_by_value("cash")

        # Check if cash-specific elements are displayed (if any)
        cash_info = self.driver.find_element(By.ID, "cash-info")
        self.assertTrue(cash_info.is_displayed())

        # Fill in the bill denominations
        # Adjust IDs based on your form's structure
        self.driver.find_element(By.ID, "bill-5").send_keys("2")   # 2 x €5 bills
        self.driver.find_element(By.ID, "bill-10").send_keys("3")  # 3 x €10 bills
        self.driver.find_element(By.ID, "bill-20").send_keys("3")  # 3 x €20 bills
        self.driver.find_element(By.ID, "bill-50").send_keys("1")  # 1 x €50 bill

        # Submit the form
        self.driver.find_element(By.CLASS_NAME, "submit").click()

        # Wait for the response to appear in the browser
        response_container = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "response-container"))
        )

        # Retrieve the JSON response directly from the browser
        response_text = response_container.text

        # Convert text to a dictionary
        json_data = json.loads(response_text)

        print(json_data)
        # Validate the JSON response
        self.assertEqual(json_data.get('success'), True)
        self.assertEqual(json_data.get('change'), 5000)
        self.assertEqual(json_data.get('coin_types'), {"5000": 1})

if __name__ == '__main__':
    unittest.main()
