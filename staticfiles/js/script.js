// Password Toggle Logic
document.addEventListener('DOMContentLoaded', function () {

    // Helper function to toggle password visibility
    function togglePassword(toggleBtnId, passwordInputId) {
        const toggleBtn = document.getElementById(toggleBtnId);
        const passwordInput = document.getElementById(passwordInputId);

        if (toggleBtn && passwordInput) {
            toggleBtn.addEventListener('click', function () {
                // Toggle the type attribute
                const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
                passwordInput.setAttribute('type', type);

                // Toggle the eye icon
                const icon = this.querySelector('i');
                if (icon) {
                    icon.classList.toggle('fa-eye');
                    icon.classList.toggle('fa-eye-slash');
                }
            });
        }
    }

    // Initialize toggles
    togglePassword('togglePwd', 'pwd');       // Login page
    togglePassword('togglePwd1', 'pwd1');     // Signup page (Password)
    togglePassword('togglePwd2', 'pwd2');     // Signup page (Confirm Password)
});
