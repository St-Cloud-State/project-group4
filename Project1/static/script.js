// static/script.js

// Capitalize the rubric field in real-time
document.addEventListener("DOMContentLoaded", function () {
    const rubricField = document.querySelector('input[name="rubric"]');
    if (rubricField) {
        rubricField.addEventListener('input', function () {
            this.value = this.value.toUpperCase();
        });
    }

    // Confirm before submitting any form
    const forms = document.querySelectorAll("form");
    forms.forEach(form => {
        form.addEventListener("submit", function (e) {
            const confirmed = confirm("Are you sure you want to submit?");
            if (!confirmed) {
                e.preventDefault();
            }
        });
    });
});
