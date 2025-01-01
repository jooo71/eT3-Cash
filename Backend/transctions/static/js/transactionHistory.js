async function transactionHistory() {
    const token = localStorage.getItem('access_token');
    const messageDiv = document.getElementById('message');  // Get the message div
    const transactionBody = document.getElementById('transaction-body');

    // Clear previous messages
    messageDiv.textContent = '';

    try {
        const response = await fetch('/transactionHistory/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        });

        const data = await response.json();
        if (response.ok) {
            // Clear existing transactions
            transactionBody.innerHTML = '';

            // Populate table with transactions
            data.transactions.forEach(transaction => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${new Date(transaction.date).toLocaleString()}</td>
                    <td>${transaction.transaction_type}</td>
                    <td>${transaction.amount}</td>
                    <td>${transaction.recipient || 'N/A'}</td>
                    
                `;
                transactionBody.appendChild(row);
            });
        } else {
            // Display error message if there's an error
            messageDiv.style.color = 'red';
            messageDiv.textContent = `Error: ${data.error}`;
        }
    } catch (error) {
        console.error('Error:', error);
        messageDiv.style.color = 'red';
        messageDiv.textContent = 'An error occurred. Please try again later.';
    }
}

function goBack() {
    window.location.href = '/dashboard'; // Redirect to dashboard or previous page
}

// Fetch transaction history when the page loads
window.onload = transactionHistory;
