// withdraw.js

async function submitWithdraw() {
    const token = localStorage.getItem('access_token');
    const amount = document.getElementById('withdraw-amount').value;
    const messageDiv = document.getElementById('message');  // Get the message div
    const withdrawInput = document.getElementById('withdraw-amount');  // Get the input field

    // Clear any previous messages
    messageDiv.textContent = '';
    messageDiv.style.color = 'green';  // Reset color to green for success messages

    if (amount) {
        try {
            const response = await fetch('/withdraw/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ amount })
            });

            const data = await response.json();
            if (response.ok) {
                // Display success message
                messageDiv.textContent = `Withdrawal successful! New Balance: ${data.message}`;
                withdrawInput.value = '';  // Clear the input field after success
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
        messageDiv.textContent = 'Please enter a valid amount.';
    }
}
