document.addEventListener('DOMContentLoaded', function () {
    console.log('DOM is ready');
    const passwordInput = document.getElementById('password');
    const usernameInput = document.getElementById('username');
    usernameInput.addEventListener('input', validateusername);
    passwordInput.addEventListener('input', validatePassword);

});
function validateusername() {
    const username = usernameInput.value.trim();
    const usernameError= document.getElementById('usernameerror')
    if (username === '') {
        usernameError.textContent = 'Username is required';
        usernameError.style.color = 'red'; // Set text color to red
        return false;
    } else if (username.length < 5 || username.length > 16) {
        usernameError.textContent = 'Username must be between 5 and 16 characters';
        usernameError.style.color = 'red'; // Set text color to red
        return false;
    } else if (!/^[a-zA-Z_][a-zA-Z0-9_]*$/.test(username)) {
        usernameError.textContent = 'Username can only contain alphabets, numbers, and underscores. It must start with an alphabet or underscore.';
        usernameError.style.color = 'red'; // Set text color to red
        return false;
    } else if (!/[a-zA-Z]/.test(username)) {
        usernameError.textContent = 'Username must contain at least one alphabet character.';
        usernameError.style.color = 'red'; // Set text color to red
        return false;
    }

    usernameError.textContent = ''; // Clear any previous error message
    usernameError.style.color = 'green'; // Reset text color
    return true;
}

function validatePassword() {
    const passwordInput = document.getElementById('password');
    const passwordError = document.getElementById('passworderror');
    const passwordValue = passwordInput.value.trim();

    if (passwordValue === '') {
        passwordError.textContent = 'Password cannot be empty.';
        passwordError.style.color = 'red';
    } else if (!/(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W)/.test(passwordValue)) {
        passwordError.textContent = 'Password must contain at least one number, one lowercase and one uppercase letter, and one special character.';
        passwordError.style.color = 'red';
    } else {
        passwordError.textContent = '';
    }
}

function validateForm() {
    const passwordInput = document.getElementById('password');
    const usernameInput = document.getElementById('username');
    const usernameValue = usernameInput.value.trim();
    const passwordValue = passwordInput.value.trim();

    if (usernameValue === '') {
        alert('Username cannot be empty');
        return false;
    } else if (passwordValue === '') {
        alert('Password cannot be empty.');
        return false;
    } else {
        return true;
    }
}
