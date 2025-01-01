document.getElementById('register-form').addEventListener('submit', async function (e) {
    e.preventDefault();

    const name = document.getElementById('name').value;
    const phoneNumber = document.getElementById('phone-number').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    const messageDiv = document.getElementById('message');

    // Clear previous messages
    messageDiv.textContent = '';

    // Basic validation for password matching
    if (password !== confirmPassword) {
        messageDiv.textContent = 'Passwords do not match.';
        return;
    }

    try {
        const response = await fetch('/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: name,
                phone_number: phoneNumber,
                password: password
            })
        });

        if (response.ok) {
            const data = await response.json();
            messageDiv.style.color = 'green';
            messageDiv.textContent = 'Registration successful!';
            // Optionally store the token or redirect to another page
            setTimeout(() => window.location.href = '/login', 100);
        } else {
            const data = await response.json();
            messageDiv.textContent = `Error: ${data.error}`;
        }
    } catch (error) {
        console.error('Error:', error);
        messageDiv.textContent = 'An error occurred. Please try again later.';
    }
});
