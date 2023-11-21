/*
*  FIX BUG
*
* if user enters name in field and clicks away it works fine
* but if the user clicks on the field, enters a name and clicks on the button the validation messages overlap
* (the class removal function doesn't trigger - button click event interrupts the function)
*
* */

(() => {
    "use strict";

    let formSignUp = document.getElementById("form-sign-up")

    formSignUp.addEventListener('submit', (event) => {
            // prevent submission
            if (!formSignUp.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
        }, false);

    // changes validation message when user deselects input field
    document.getElementById("input-name").addEventListener("blur", async (event) => {
        // get username input from page
        let inputName = event.target.value;
        let invalidNameElement = document.getElementById("validity-response-name-invalid");

        // if input field has content
        if (inputName.trim() !== "") {
            try {
                // send a request to the server to check if the username exists in the database
                let response = await fetch(`validation/user-exists/${inputName}`);
                let userValidation = await response.json(); // boolean - does the user exist in the database

                // if user is new (does not exist in the database already)
                if (!userValidation) {
                    // show VALID message
                    event.target.classList.add("is-valid");
                    event.target.classList.remove("is-invalid");

                    // change invalid message back to DEFAULT
                    //invalidNameElement.textContent = "Enter username"
                }
                // if user already exists - show INVALID message
                else {
                    // change invalid message
                    invalidNameElement.textContent = "Username already exists";

                    // show invalid message
                    event.target.classList.add("is-invalid");
                    event.target.classList.remove("is-valid");
                }
            // if there is a connection issue display error
            } catch (error) {
                console.error("Error making HTTP request", error);
            }
        }
        // if field is empty
        else {
            // change invalid message
            invalidNameElement.textContent = "Enter username";

            // show INVALID message only if the field is not empty
            event.target.classList.add("is-invalid");
            event.target.classList.remove("is-valid");
        }
    });
})();