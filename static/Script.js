// Client-side validations

// Login validation
function validateLogin() {
    let email = document.getElementById("loginEmail").value;
    let password = document.getElementById("loginPassword").value;

    if (email === "" || password === "") {
        alert("All fields are required!");
        return false;
    }
    if (password.length < 6) {
        alert("Password must be at least 6 characters.");
        return false;
    }

    // Redirect to home page after successful login
    window.location.href = "home.html";
    return false; // prevent default submission
}

// Register validation
function validateRegister() {
    let name = document.getElementById("name").value;
    let email = document.getElementById("regEmail").value;
    let password = document.getElementById("regPassword").value;
    let confirmPassword = document.getElementById("confirmPassword").value;

    if (!name || !email || !password || !confirmPassword) {
        alert("All fields are required!");
        return false;
    }
    if (password.length < 6) {
        alert("Password must be at least 6 characters.");
        return false;
    }
    if (password !== confirmPassword) {
        alert("Passwords do not match!");
        return false;
    }

    alert("Registration Successful!");
    window.location.href = "login.html"; // Redirect after registration
    return false;
}

// Diabetes form validation - 8 fields
function validateForm() {
    let pregnancies = document.getElementById("pregnancies").value;
    let glucose = document.getElementById("glucose").value;
    let bp = document.getElementById("bp").value;
    let skinThickness = document.getElementById("skinThickness").value;
    let insulin = document.getElementById("insulin").value;
    let bmi = document.getElementById("bmi").value;
    let dpf = document.getElementById("dpf").value;
    let age = document.getElementById("age").value;

    if (
        pregnancies === "" || glucose === "" || bp === "" ||
        skinThickness === "" || insulin === "" || bmi === "" ||
        dpf === "" || age === ""
    ) {
        alert("Please fill all fields!");
        return false;
    }

    if (pregnancies < 0) { alert("Pregnancies must be 0 or more!"); return false; }
    if (glucose < 50) { alert("Glucose should be at least 50!"); return false; }
    if (bp < 50) { alert("Blood Pressure should be at least 50!"); return false; }
    if (skinThickness < 0) { alert("Skin Thickness cannot be negative!"); return false; }
    if (insulin < 0) { alert("Insulin cannot be negative!"); return false; }
    if (bmi <= 0) { alert("BMI must be greater than 0!"); return false; }
    if (dpf < 0) { alert("Diabetes Pedigree Function cannot be negative!"); return false; }
    if (age < 1) { alert("Age must be valid!"); return false; }

    alert("Form Submitted Successfully!");
    return true;
}
