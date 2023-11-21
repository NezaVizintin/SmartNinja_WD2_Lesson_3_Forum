/*
The code sets the document.cookie variable to "foo=bar;".
If this is not set, an alert will be shown.

document.cookie = "foo=bar;";
if (!document.cookie) {
    alert("This website requires cookies to function properly");
}*/

// Disable form submission if there are invalid fields
(() => {
    "use strict";

    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    const forms = document.querySelectorAll('.needs-validation');

    // Loop over them
    Array.prototype.slice.call(forms).forEach((form) => {

        // when submit is triggered
        form.addEventListener('submit', (event) => {
            // prevent submission
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
})();