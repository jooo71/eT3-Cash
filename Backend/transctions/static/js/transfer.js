// transfer.js

async function transfer() { // Updated function name
    const token = localStorage.getItem('access_token'); // Retrieve the access token from local storage
    const amount = document.getElementById('transfer-amount').value; // Get the transfer amount from the input field
    const recipientPhone = document.getElementById('recipient-phone').value; // Get the recipient's phone number from the input field
    const messageDiv = document.getElementById('message');  // Get the message div for displaying messages

    // Clear any previous messages
    messageDiv.textContent = '';
    messageDiv.style.color = 'green';  // Reset color to green for success messages

    // Check if the amount and recipient phone are provided
    if (amount && recipientPhone) {
        try {
            const response = await fetch('/transfer/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`  // Include the access token in the request header
                },
                body: JSON.stringify({
                    recipient_phone: recipientPhone, // Send recipient phone number
                    amount: amount // Send transfer amount
                })
            });

            const data = await response.json();
            if (response.ok) {
                // Display success message with recipient's name
                messageDiv.textContent = `Successfully transferred ${amount} to ${data.recipient_name}.`;
                messageDiv.style.color = 'green';  // Keep it green for success
                // Clear input fields after success
                document.getElementById('transfer-amount').value = '';  // Clear amount field
                document.getElementById('recipient-phone').value = '';  // Clear recipient phone field
            } else {
                // Display error message if there's an error
                messageDiv.style.color = 'red';  // Set color to red for error messages
                messageDiv.textContent = `Error: ${data.error}`; // Show the error message from the server response
            }
        } catch (error) {
            console.error('Error:', error);
            messageDiv.style.color = 'red'; // Set message color to red on error
            messageDiv.textContent = 'An error occurred. Please try again later.'; // Generic error message
        }
    } else {
        messageDiv.style.color = 'red'; // Set message color to red for validation errors
        messageDiv.textContent = 'Please enter a valid amount and recipient phone number.'; // Prompt user to provide input
    }
}
