// Capture version selection from dropdowns and display the custom modal
document.querySelectorAll('.version-dropdown').forEach(dropdown => {
    dropdown.addEventListener('change', function () {
        const selectedVersion = this.value;
        if (selectedVersion) {
            // Display the custom modal
            const modal = document.getElementById('passwordModal');
            modal.classList.add('show');

            const okBtn = document.getElementById('modalOkBtn');
            const cancelBtn = document.getElementById('modalCancelBtn');
            const passwordInput = document.getElementById('rootPasswordInput');

            // Clear the input field
            passwordInput.value = '';

            // Handle OK button click
            okBtn.onclick = function () {
                const rootPassword = passwordInput.value;
                if (rootPassword) {
                    alert(`Root password accepted. Selected version: ${selectedVersion}`);
                    modal.classList.remove('show'); // Hide modal after submission
                } else {
                    alert("Root password is required.");
                }
                $.ajax({
                    url: '/process',
                    type: 'POST',
                    data: { 'idk': rootPassword, "version":selectedVersion },
                    error: function(error) {
                        console.log(error);
                    }
                });
    
            };

            // Handle Cancel button click
            cancelBtn.onclick = function () {
                modal.classList.remove('show'); // Hide modal on cancel
            };
        }
    });
});
