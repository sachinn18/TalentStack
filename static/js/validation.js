// This is a placeholder for form validation logic.
// We will attach these functions to our forms to provide client-side validation.

document.addEventListener('DOMContentLoaded', function() {
    // Example: Validate Registration Form
    const registerForm = document.querySelector('form'); // A more specific selector is better
    if (registerForm) {
        registerForm.addEventListener('submit', function(event) {
            let isValid = true;
            
            // Clear previous errors
            const errorMessages = document.querySelectorAll('.error-message');
            errorMessages.forEach(msg => msg.remove());

            // Validate Username
            const username = document.getElementById('username');
            if (username && username.value.trim() === '') {
                isValid = false;
                showError(username, 'Username is required.');
            }

            // Validate Email
            const email = document.getElementById('email');
            if (email && !validateEmail(email.value)) {
                isValid = false;
                showError(email, 'Please enter a valid email address.');
            }

            // Validate Password
            const password = document.getElementById('password');
            if (password && password.value.length < 6) {
                isValid = false;
                showError(password, 'Password must be at least 6 characters long.');
            }

            // Validate Confirm Password
            const confirmPassword = document.getElementById('confirm_password');
            if (confirmPassword && password && confirmPassword.value !== password.value) {
                isValid = false;
                showError(confirmPassword, 'Passwords do not match.');
            }

            if (!isValid) {
                event.preventDefault(); // Stop form submission
            }
        });
    }
});

function validateEmail(email) {
    const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}

function showError(inputElement, message) {
    const error = document.createElement('div');
    error.className = 'error-message';
    error.style.color = 'red';
    error.style.fontSize = '0.8rem';
    error.innerText = message;
    inputElement.parentNode.appendChild(error);
} 