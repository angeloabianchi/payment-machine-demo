// Get elements from the DOM
const paymentMethodSelect = document.getElementById("payment-method");
const cardInfo = document.getElementById("card-info");
const cashInfo = document.getElementById("cash-info");
const paymentForm = document.getElementById("payment-form");
const transactionsButton = document.getElementById("transactions");
const transactionForm = document.getElementById("transaction-form");

// Function to show the payment form and hide the transaction form
function showPaymentForm() {
  // Show the payment form section and hide the transaction form section
  document.getElementById("payment-form-section").style.display = "block";
  document.getElementById("transaction-form-section").style.display = "none";

  // Enable fields in the payment form and disable fields in the transaction form
  document.getElementById("card-number").disabled = false;
  document.querySelectorAll("#transaction-form input").forEach((input) => {
    input.disabled = true;
  });

  // Update active tab styling
  document.getElementById("payment-tab").classList.add("active");
  document.getElementById("transaction-tab").classList.remove("active");
}

// Function to show the transaction form and hide the payment form
function showTransactionForm() {
  // Show the transaction form section and hide the payment form section
  document.getElementById("payment-form-section").style.display = "none";
  document.getElementById("transaction-form-section").style.display = "block";

  // Disable fields in the payment form and enable fields in the transaction form
  document.getElementById("card-number").disabled = true;
  document.querySelectorAll("#transaction-form input").forEach((input) => {
    input.disabled = false;
  });

  // Update active tab styling
  document.getElementById("transaction-tab").classList.add("active");
  document.getElementById("payment-tab").classList.remove("active");
}

// Function to handle payment method change and show/hide relevant fields
document
  .getElementById("payment-method")
  .addEventListener("change", function () {
    if (this.value === "card") {
      document.getElementById("card-info").style.display = "block";
      document.getElementById("cash-info").style.display = "none";
      document.getElementById("card-number").disabled = false; // Enable card number field
      document
        .querySelectorAll(".cash-input")
        .forEach((input) => (input.disabled = true)); // Disable cash fields
    } else {
      document.getElementById("card-info").style.display = "none";
      document.getElementById("cash-info").style.display = "block";
      document.getElementById("card-number").disabled = true; // Disable card number field
      document
        .querySelectorAll(".cash-input")
        .forEach((input) => (input.disabled = false)); // Enable cash fields
    }
  });

// Ensure the "Make a Payment" form is displayed by default when the page loads
window.onload = function () {
  showPaymentForm();
};

// Add event listener for the button click
transactionsButton.addEventListener("click", async () => {
  try {
    // Fetch all transactions from the endpoint
    const response = await fetch("/api/transactions", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
    });

    const data = await response.json();

    console.log(data);

    // Display the response in the terminal box
    document.getElementById("response-container").textContent = JSON.stringify(
      data,
      null,
      2
    );
  } catch (error) {
    console.error("Error:", error);
    document.getElementById("response-container").textContent =
      "Error fetching transactions";
  }
});

// Event listener for handling transaction search by ID
transactionForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  transactionId = document.getElementById("transaction-id").value;
  try {
    // Fetch the transaction from the endpoint
    const response = await fetch(`/api/transactions/${transactionId}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
    });

    const data = await response.json();

    console.log(data);

    // Display the response in the terminal box
    document.getElementById("response-container").textContent = JSON.stringify(
      data,
      null,
      2
    );
  } catch (error) {
    console.error("Error:", error);
    document.getElementById("response-container").textContent =
      "Error fetching transactions";
  }
});

// Event listener for payment method selection and display of relevant fields
paymentMethodSelect.addEventListener("change", () => {
  if (paymentMethodSelect.value === "card") {
    cardInfo.style.display = "block";
    cashInfo.style.display = "none";
  } else {
    cardInfo.style.display = "none";
    cashInfo.style.display = "block";
  }
});

// Event listener for submitting the payment form
paymentForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const formData = {
    payment_method: paymentMethodSelect.value,
    amount: document.getElementById("amount").value,
    currency: document.getElementById("currency").value,
  };

  if (formData.payment_method === "card") {
    formData.card_num = document.getElementById("card-number").value;
  } else {
    const cashInputs = document.querySelectorAll(".cash-input");
    const coin_types = {};
    cashInputs.forEach((input) => {
      const value = parseInt(input.value, 10);
      if (value > 0) {
        coin_types[input.getAttribute("data-value")] = value;
      }
    });
    formData.coin_types = coin_types; // Include coin types for cash payments
  }

  try {
    // Fetch the transaction from the endpoint
    const response = await fetch("/api/process-payment/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify(formData),
    });

    const data = await response.json();

    // Display the response data in the terminal box
    document.getElementById("response-container").textContent = JSON.stringify(
      data,
      null,
      2
    );
  } catch (error) {
    console.error("Error:", error);
    document.getElementById("response-container").textContent =
      "Error processing payment";
  }
});

// Function to get the CSRF token for making secure POST requests
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
