// buyAirtime.js

async function submitAirtimePurchase() {
    const token = localStorage.getItem('access_token');
    const amount = document.getElementById('airtime-amount').value;
    const messageDiv = document.getElementById('message');  // Get the message div

    // Clear any previous messages
    messageDiv.textContent = '';
    messageDiv.style.color = 'green';  // Reset color to green for success messages

    // Retrieve the user's phone number from localStorage
    const phoneNumber = localStorage.getItem('user_phone_number');  // Ensure this is set during login

    if (amount ) {
        try {
            const response = await fetch('/buyAirtime/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({  amount })
            });

            const data = await response.json();
            if (response.ok) {
                // Display success message
                messageDiv.textContent = `Airtime of ${amount} bought successfully.`;
                messageDiv.style.color = 'green';  // Keep it green for success
                // Clear input fields after success
                document.getElementById('airtime-amount').value = '';  // Clear amount field
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
        messageDiv.textContent = 'Please enter a valid amount.';  // Adjusted message
    }
}
