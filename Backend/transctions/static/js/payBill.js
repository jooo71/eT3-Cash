// payBill.js

async function payBill() {
    const token = localStorage.getItem('access_token');
    const billType = document.getElementById('bill-type').value;
    const amount = document.getElementById('bill-amount').value;
    const messageDiv = document.getElementById('message');  // Get the message div
    const billTypeInput = document.getElementById('bill-type');  // Get the bill type input field
    const billInput = document.getElementById('bill-amount');  // Get the bill amount input field

    // Clear any previous messages
    messageDiv.textContent = '';
    messageDiv.style.color = 'green';  // Reset color to green for success messages

    if (billType && amount) {
        try {
            const response = await fetch('/payBill/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ bill_type: billType, amount })
            });

            const data = await response.json();
            if (response.ok) {
                // Display success message
                messageDiv.textContent = `Bill paid successfully! Type: ${billType}, Amount: ${data.message}`;
                billTypeInput.value = '';  // Clear the bill type input field after success
                billInput.value = '';  // Clear the amount input field after success
            } else {
                // Display error message
                messageDiv.style.color = 'red';  // Set color to red for error messages
                messageDiv.textContent = `Error: ${data.error}`;
            }
        } catch (error) {
            console.error('Error:', error);
            messageDiv.style.color = 'red';
            messageDiv.textContent = 'An error occurred. Please try again later.';
        }
    } else {
        messageDiv.style.color = 'red';
        messageDiv.textContent = 'Please enter a valid bill type and amount.';
    }
}
