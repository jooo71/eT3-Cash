async function logout() {
    // Remove the access token from localStorage
    localStorage.removeItem('access_token');
    
    // Optionally, you can make a request to your backend to invalidate the token
    try {
        const response = await fetch('/logout/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
            }
        });
        if (response.ok) {
            // Redirect to the login page after successful logout
            window.location.href = '/login';
        } else {
            console.error('Logout failed');
        }
    } catch (error) {
        console.error('Error during logout:', error);
    }

    // Redirect to the login page
    window.location.href = '/login';
}
