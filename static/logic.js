document.addEventListener('DOMContentLoaded', function () {
  const loginForm = document.getElementById('loginForm');
  const emailInput = document.getElementById('email');
  const passwordInput = document.getElementById('password');
  const emailError = document.getElementById('emailError');
  const passwordError = document.getElementById('passwordError');

  function validateEmail(email) {
    // Basic email validation regex
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }

  function validatePassword(password) {
    // Check for minimum length and disallowed characters
    const minLength = 8;
    const hasQuotes = /["]/.test(password);
    return password.length >= minLength && !hasQuotes;
  }

  loginForm.addEventListener('submit', function (event) {
    let isValid = true;

    // Validate email
    if (!validateEmail(emailInput.value)) {
      emailError.textContent = 'Invalid email format';
      isValid = false;
    } else {
      emailError.textContent = '';
    }

    // Validate password
    if (!validatePassword(passwordInput.value)) {
      passwordError.textContent = 'Password must be at least 8 characters and not contain ""';
      isValid = false;
    } else {
      passwordError.textContent = '';
    }

    // Prevent form submission if validation fails
    if (!isValid) {
      event.preventDefault();
    }
  });
});
