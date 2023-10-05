document.addEventListener('DOMContentLoaded', function () {
    console.log('DOM is ready');
    const form = document.getElementById('your-form-id');
    const passwordInput = document.getElementById('password');
    const cpassInput = document.getElementById('cpass');
    const mobInput = document.getElementById('mobile');
    passwordInput.addEventListener('input', validatePassword);
    cpassInput.addEventListener('input', validateConfirmPassword);
    mobInput.addEventListener('input', validatePhone);
    // const usernameInput = document.getElementById("username");
    const emailInput = document.getElementById("email");
    const dobInput = document.getElementById('dob');
    const firstnameInput = document.getElementById("firstname");
    const lastnameInput = document.getElementById("lastname");
    
    firstnameInput.addEventListener("blur", validateFirstname);
    lastnameInput.addEventListener("blur", validateLastname);
    dobInput.addEventListener("blur", validateDob);
    // usernameInput.addEventListener("blur", validateUsername);
    emailInput.addEventListener("blur", validateEmail);
});

function validatePassword() {
    const passwordInput = document.getElementById('password');
    const passwordError = document.getElementById('passwordError');
    const passwordValue = passwordInput.value.trim();

    if (passwordValue === '') {
        passwordError.textContent = 'Password cannot be empty.';
        passwordError.style.color = 'red';
    } else if (!/(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W)/.test(passwordValue)) {
        passwordError.textContent = 'Password must contain at least one number, one lowercase and one uppercase letter, and one special character.';
        passwordError.style.color = 'red';
    } else {
        passwordError.textContent = 'Good';
        passwordError.style.color = 'green';
    }
}

function validatePhone() {
    const mobileInput = document.getElementById('mobile');
    const mobileError = document.getElementById('mobileerror');
    const mobileValue = mobileInput.value.trim();

    // Regular expression pattern for a valid 10-digit mobile phone number
    const mobilePattern = /^[0-9]{10}$/;

    if (mobileValue === '') {
        mobileError.textContent = 'Mobile number cannot be empty.';
        mobileError.style.color = 'red';
    } else if (mobileValue.length !== 10 || !/^[0-9]+$/.test(mobileValue)) {
        mobileError.textContent = 'Please enter a valid 10-digit numeric mobile number.';
        mobileError.style.color = 'red';
    } else if (!mobilePattern.test(mobileValue)) {
        mobileError.textContent = 'Please enter a valid 10-digit mobile number.';
        mobileError.style.color = 'red';
    } else {
        mobileError.textContent = 'Good';
        mobileError.style.color = 'white';
    }
}

// Add an event listener to trigger validation on input
const mobileInput = document.getElementById('mobile');
mobileInput.addEventListener('input', validatePhone);


function validateConfirmPassword() {
    const passwordInput = document.getElementById('password');
    const cpassInput = document.getElementById('cpass');
    const cpassError = document.getElementById('cpasserror');
    const passwordValue = passwordInput.value.trim();
    const cpassValue = cpassInput.value.trim();

    if (cpassValue === '') {
        cpassError.textContent = 'Confirm Password cannot be empty.';
        cpassError.style.color = 'red';
    } else if (!/(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W)/.test(passwordValue)) {
        cpassError.textContent = 'Password must contain at least one number, one lowercase and one uppercase letter, and one special character.';
        cpassError.style.color = 'red';
    } else if (cpassValue !== passwordValue) {
        cpassError.textContent = 'Passwords do not match.';
        cpassError.style.color = 'red';
    } else {
        cpassError.textContent = 'Good';
        cpassError.style.color = 'green';
    }
}
function checkSelectedState() {
    const stateSelect = document.getElementById('state');
    const selectedState = stateSelect.value;

    if (selectedState === '') {
        alert('Please select a state.');
         } else {
        console.log('Selected state: ' + selectedState);
    }
}
// function validateUsername() {
//     const usernameError = document.getElementById("UsernameError");
//     const username = usernameInput.value;
    
//     const regex = /^[a-zA-Z][a-zA-Z0-9_-]{2,19}$/;  // Setting Up Regular Expression
//     const match = username.match(regex);
//     const noMatch = username.match(/\s/)

//     if (!match) {
//         usernameError.style.color = "red";
//         if (username.trim() === "") {
//             usernameError.textContent = "This Field Cannot be empty";
//         } else if (!username.match(/^[a-zA-Z]/)) {
//             usernameError.textContent = "Username must start with a letter.";
//         } else if (!username.match(/[a-zA-Z0-9_-]{2,19}$/)) {
//             usernameError.textContent = "Username must be between 3 and 20 characters and can only contain letters, numbers, underscores, or hyphens.";
//         } else if (username.match(/\s/)) {
//             usernameError.textContent = "Whitespace not allowed.";
//         } else {
//             usernameError.textContent = "Username must be between 3 and 20 characters and can only contain letters, numbers, underscores, or hyphens.";
//         }
//         return false;
//     } else {
//         usernameError.style.color = "green";
//         usernameError.textContent = "Good";  // Clear the error message
//         return true;
//     }
// }

// E-Mail Validation
function validateEmail() {
    const emailError = document.getElementById("email-error");
    const email = emailInput.value.trim();
    const regex = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;
    if (!regex.test(email) || email.length == 0) {
        emailError.style.color = "red";
        if (email.length == 0) {
            emailError.textContent = "This Field Cannot be empty";
        } else {
            emailError.textContent = "Invalid email address.";
        }
        return false;
    } else {
        emailError.style.color = "white";
        emailError.textContent = "Good";
        return true;
    }
}
function validateForm() {
    const passwordInput = document.getElementById('password');
    const cpassInput = document.getElementById('cpass');
    const mobInput = document.getElementById('mobile');
    const stateSelect = document.getElementById('state'); // Get the state select element
    const passwordValue = passwordInput.value.trim();
    const cpassValue = cpassInput.value.trim();
    const mobValue = mobInput.value.trim();
    const selectedState = stateSelect.value; // Get the selected state value

    if (passwordValue === '') {
        alert('Password cannot be empty.');
        return false;
    } else if (cpassValue === '') {
        alert('Confirm Password cannot be empty.');
        return false;
    } else if (cpassValue !== passwordValue) {
        alert('Passwords do not match.');
        return false;
    } else if (mobValue === '') {
        alert('Phone number cannot be empty.');
        return false;
    } else if (selectedState === '') { // Check if no state is selected
        alert('Please select a state.');
        return false;
    } else {
        return true;
    }
}
