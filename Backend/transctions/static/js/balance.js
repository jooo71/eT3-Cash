async function balance() {
    const token = localStorage.getItem('access_token'); // Retrieve access token
    const balanceDiv = document.getElementById('balance-amount'); // Get the balance div
    const messageDiv = document.getElementById('message'); // Get the message div

    // Clear previous messages
    messageDiv.textContent = '';

    try {
        const response = await fetch('/balance/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}` // Add authorization token in headers
            }
        });

        if (response.ok) {
            const data = await response.json();
            // Display the current balance
            balanceDiv.textContent = `$${data.balance.toFixed(2)}`; // Show balance with 2 decimal points
            balanceDiv.style.color = 'green';
        } else if (response.status === 401) {
            // Handle unauthorized access
            messageDiv.textContent = 'Unauthorized: Please log in again.';
            balanceDiv.textContent = ''; // Clear balance if unauthorized
            localStorage.removeItem('access_token'); // Remove invalid token
            // Optionally, redirect to the login page
            window.location.href = '/login'; // Redirect to the login page
        } else {
            // Show an error message if something else went wrong
            const data = await response.json();
            messageDiv.textContent = `Error: ${data.error}`;
        }
    } catch (error) {
        console.error('Error:', error);
        messageDiv.textContent = 'An error occurred. Please try again later.';
    }
}
