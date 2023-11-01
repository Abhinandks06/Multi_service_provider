const regForm = document.getElementById('regForm');
regForm.addEventListener("submit", handleEventListener);

// Initailising Input field VIA id
//const usernameInput = document.getElementById("username");
// const emailInput = document.getElementById("email");
const dobInput = document.getElementById('dob');
const dobError = document.getElementById('dobError');
const providernameInput = document.getElementById("providername");
const ownernameInput = document.getElementById("ownername");

// Setting Input Field Listener
providernameInput.addEventListener("blur", validateprovidername);
ownernameInput.addEventListener("blur", validateownername);W
dobInput.addEventListener("blur", validateDob);
//usernameInput.addEventListener("blur", validateusername);
// emailInput.addEventListener("blur", validateEmail);
providernameInput.addEventListener('input', function (event) {
   validateprovidername();
});
dobInput.addEventListener('input', function (event)
 {
    validateDob();
});
ownernameInput.addEventListener('input', function (event)
 {
    validateownername();
});

// passwordInput.addEventListener('input', function (event) {
//   validatepassword1();
// });
// emailInput.addEventListener("input", function(event){
//   validateEmail();
    
// });
// addressInput.addEventListener("input", function(event){
//     validateAddress();
// });
// Function to Handle Form Submission
function validateprovidername() {
    const providernameInput = document.getElementById('providername');
    const providernameError = document.getElementById('providernameError');
    
    const providername = providernameInput.value.trim();
    const minLength = 3;
    const maxLength = 20;
    
    // Regular Expression to check for alphabetic characters only
    const regex = /^[A-Za-z]+$/;
    const match = providername.match(regex);
    const hasNumbersOrSpecialChars = /[0-9!@#$%^&*()_+{}\[\]:;<>,.?~\\]/.test(providername);
    if (providername.trim() === '') {
        providernameError.textContent = "This Field Cannot be empty";
        providernameError.style.color = 'red';
    }
    else if (hasNumbersOrSpecialChars) {
        providernameError.style.color = 'red';
        providernameError.textContent = 'provider name cannot contain numbers or special characters.';
        return false;
    }
    else if (providername.length < minLength) {
        providernameError.style.color = 'red';
        providernameError.textContent = `provider name must be at least ${minLength} characters.`;
        return false;
    } else if (providername.length > maxLength) {
        providernameError.style.color = 'red';
        providernameError.textContent = `provider name cannot exceed ${maxLength} characters.`;
        return false;
    } else if (hasNumbersOrSpecialChars) {
        providernameError.style.color = 'red';
        providernameError.textContent = 'provider name cannot contain numbers or special characters.';
        return false;
    } else if (!match) {
        providernameError.style.color = 'red';
        if (providername.trim() === '') {
            providernameError.textContent = 'This field cannot be empty.';
        } else {
            providernameError.textContent = 'provider name must contain alphabetic characters only.';
        }
        return false;
    } else {
        providernameError.style.color = 'green';
        providernameError.textContent = 'Good'; // Clear the error message
        return true;
    }
}
function validateownername() {
    const ownernameInput = document.getElementById('ownername');
    const ownernameError = document.getElementById('ownernameError');
    
    const ownername = ownernameInput.value.trim();
    const minLength = 1;
    const maxLength = 15;
    const maxSpaces = 1; // Maximum number of blank spaces allowed
    
    if (ownername.trim() === "") {
        ownernameError.textContent = "This Field Cannot be empty";
        ownernameError.style.color = 'red';
        return false;
    } else if (ownername.length < minLength) {
        ownernameError.style.color = 'red';
        ownernameError.textContent = `owner name must be at least ${minLength} character(s).`;
        return false;
    } else if (ownername.length > maxLength) {
        ownernameError.style.color = 'red';
        ownernameError.textContent = `owner name cannot exceed ${maxLength} characters.`;
        return false;
    } else if ((ownername.match(/\s/g) || []).length > maxSpaces) {
        ownernameError.style.color = 'red';
        ownernameError.textContent = `owner name cannot contain more than ${maxSpaces+1} blank spaces.`;
        return false;
    } else if (ownername.charAt(0).match(/[A-Za-z]/) === null) {
        ownernameError.style.color = 'red';
        ownernameError.textContent = 'owner name must start with an alphabetic character.';
        return false;
    } else if (!/^[A-Za-z\s]+$/.test(ownername)) {
        ownernameError.style.color = 'red';
        ownernameError.textContent = 'owner name can only contain alphabetic characters and spaces.';
        return false;
    } else {
        ownernameError.style.color = 'green';
        ownernameError.textContent = 'Good'; // Clear the error message
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
    else if (age > 120) {
        dobError.style.color = 'red';
        dobError.textContent = 'Select a valid age.';
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
// function validateEmail() {
//     const emailError = document.getElementById("email-error");
//     const email = emailInput.value.trim();
//     const regex = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;
//     if (!regex.test(email) || email.length == 0) {
//         emailError.style.color = "red";
//         if (email.length == 0){
//             emailError.textContent = "This Field Cannot be empty";
//         }else{
//             emailError.textContent = "Invalid email address.";
//         }
//         return false;
//     } else {
//         emailError.style.color = "White";
//         emailError.textContent = "Good";
        
//         return true;
//     }
// }