document.getElementById('loginForm').addEventListener('submit', async function (event) {
    event.preventDefault(); // Prevent form from submitting normally

    const phone_number = document.getElementById('phone_number').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                phone_number: phone_number,
                password: password
            })
        });

        const data = await response.json();

        if (response.ok) {
            // Successful login
            localStorage.setItem('access_token', data.access); // Store the token if needed
            window.location.href = '/dashboard/'; // Redirect to the dashboard
        } else {
            // Show error message
            document.getElementById('error-message').innerText = data.error;
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('error-message').innerText = 'An error occurred. Please try again.';
    }
});