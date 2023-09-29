const regForm = document.getElementById('regForm');
regForm.addEventListener("submit", handleEventListener);

// Initailising Input field VIA id
//const usernameInput = document.getElementById("username");
const emailInput = document.getElementById("email");
const dobInput = document.getElementById('dob');
const dobError = document.getElementById('dobError');
const firstnameInput = document.getElementById("firstname");
const lastnameInput = document.getElementById("lastname");

// Setting Input Field Listener
firstnameInput.addEventListener("blur", validateFirstname);
lastnameInput.addEventListener("blur", validateLastname);W
dobInput.addEventListener("blur", validateDob);
//usernameInput.addEventListener("blur", validateusername);
emailInput.addEventListener("blur", validateEmail);
firstnameInput.addEventListener('input', function (event) {
   validateFirstname();
});
dobInput.addEventListener('input', function (event)
 {
    validateDob();
});
lastnameInput.addEventListener('input', function (event)
 {
    validateLastname();
});

// passwordInput.addEventListener('input', function (event) {
//   validatepassword1();
// });
emailInput.addEventListener("input", function(event){
  validateEmail();
    
});
addressInput.addEventListener("input", function(event){
    validateAddress();
});
// Function to Handle Form Submission
function validateFirstname() {
    const firstnameInput = document.getElementById('firstname');
    const firstnameError = document.getElementById('firstnameError');
    
    const firstname = firstnameInput.value.trim();
    const minLength = 3;
    const maxLength = 20;
    
    // Regular Expression to check for alphabetic characters only
    const regex = /^[A-Za-z]+$/;
    const match = firstname.match(regex);
    const hasNumbersOrSpecialChars = /[0-9!@#$%^&*()_+{}\[\]:;<>,.?~\\]/.test(firstname);
    if (firstname.trim() === '') {
        firstnameError.textContent = "This Field Cannot be empty";
        firstnameError.style.color = 'red';
    }
    else if (hasNumbersOrSpecialChars) {
        firstnameError.style.color = 'red';
        firstnameError.textContent = 'First name cannot contain numbers or special characters.';
        return false;
    }
    else if (firstname.length < minLength) {
        firstnameError.style.color = 'red';
        firstnameError.textContent = `First name must be at least ${minLength} characters.`;
        return false;
    } else if (firstname.length > maxLength) {
        firstnameError.style.color = 'red';
        firstnameError.textContent = `First name cannot exceed ${maxLength} characters.`;
        return false;
    } else if (hasNumbersOrSpecialChars) {
        firstnameError.style.color = 'red';
        firstnameError.textContent = 'First name cannot contain numbers or special characters.';
        return false;
    } else if (!match) {
        firstnameError.style.color = 'red';
        if (firstname.trim() === '') {
            firstnameError.textContent = 'This field cannot be empty.';
        } else {
            firstnameError.textContent = 'First name must contain alphabetic characters only.';
        }
        return false;
    } else {
        firstnameError.style.color = 'green';
        firstnameError.textContent = 'Good'; // Clear the error message
        return true;
    }
}
function validateLastname() {
    const lastnameInput = document.getElementById('lastname');
    const lastnameError = document.getElementById('lastnameError');
    
    const lastname = lastnameInput.value.trim();
    const minLength = 1;
    const maxLength = 15;
    
    if (lastname.trim() === "") {
        lastnameError.textContent = "This Field Cannot be empty";
        lastnameError.style.color = 'red';
        return false;
    } else if (lastname.length < minLength) {
        lastnameError.style.color = 'red';
        lastnameError.textContent = `Last name must be at least ${minLength} characters.`;
        return false;
    } else if (lastname.length > maxLength) {
        lastnameError.style.color = 'red';
        lastnameError.textContent = `Last name cannot exceed ${maxLength} characters.`;
        return false;
    } else if (lastname.charAt(0).match(/[A-Za-z]/) === null) {
        lastnameError.style.color = 'red';
        lastnameError.textContent = 'Last name must start with an alphabetic character.';
        return false;
    } else if (!/^[A-Za-z\s]+$/.test(lastname)) {
        lastnameError.style.color = 'red';
        lastnameError.textContent = 'Last name can only contain alphabetic characters and spaces.';
        return false;
    } else {
        lastnameError.style.color = 'green';
        lastnameError.textContent = 'Good'; // Clear the error message
        return true;
    }
}

function validateDob() {
    const dobInput = document.getElementById('dob');
    const dobError = document.getElementById('dobError');
    
    const dobString = dobInput.value;

    // Check if the input is empty
    if (dobString.trim() === '') {
        dobError.style.color = 'red';
        dobError.textContent = 'Please select a date of birth.';
        return false;
    }

    const dob = new Date(dobString);
    
    // Check if the input is a valid date
    if (isNaN(dob.getTime())) {
        dobError.style.color = 'red';
        dobError.textContent = 'Please enter a valid date of birth.';
        return false;
    }

    // Calculate age
    const today = new Date();
    const age = today.getFullYear() - dob.getFullYear();
    const monthDiff = today.getMonth() - dob.getMonth();

    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < dob.getDate())) {
        age--;
    }

    // Check if age is greater than or equal to 16
    if (age < 16) {
        dobError.style.color = 'red';
        dobError.textContent = 'You must be at least 16 years old to register.';
        return false;
    }

    // Clear the error message and return true if all conditions pass
    dobError.style.color = 'green';
    dobError.textContent = 'Good'; // Clear the error message
    return true;
}

// User Validation
// function validateusername() {
//     const usernameError = document.getElementById("usernameError");
//     const username = event.target.value;
    
//     const regex = /^[a-zA-Z][a-zA-Z0-9_-]{2,19}$/;  // Setting Up Regular Expression
//     const match = username.match(regex);
//     const noMatch = username.match(/\s/)

//     if (!match) {
//         usernameError.style.color = "red";
//         if (username.trim() === "") {
//             usernameError.textContent = "This Field Cannot be empty";
//         }else if (!username.match(/^[a-zA-Z]/)) {
//             usernameError.textContent = " Username must start with a letter.";
//         }else if (!username.match(/[a-zA-Z0-9_-]{2,19}$/)) {
//             usernameError.textContent = " Username must be between 3 and 20 characters and can only contain letters, numbers, underscores, or hyphens.";
//         }else if (username.match(/\s/)){
//             usernameError.textContent = "White Space Not Allowed";
//         }else{
//             usernameError.textContent = " Username must be between 3 and 20 characters and can only contain letters, numbers, underscores, or hyphens.";
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
        if (email.length == 0){
            emailError.textContent = "This Field Cannot be empty";
        }else{
            emailError.textContent = "Invalid email address.";
        }
        return false;
    } else {
        emailError.style.color = "White";
        emailError.textContent = "Good";
        
        return true;
    }
}