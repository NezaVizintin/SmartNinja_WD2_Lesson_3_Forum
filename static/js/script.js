/*
The code sets the document.cookie variable to "foo=bar;".
If this is not set, an alert will be shown.

document.cookie = "foo=bar;";
if (!document.cookie) {
    alert("This website requires cookies to function properly");
}*/

// Disable form submission if there are invalid fields
(function () {
    'use strict';
    window.addEventListener('load', function () {
        var form = document.getElementById('loginForm');
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);

        document.getElementById('input-name').addEventListener('blur', event => {

        let uname = event.target.value;
          var res = fetch('validation/user-exists/' + uname)

          res.then(r => {
            return r.json();
          }).then(user_is_valid => {
              if(!user_is_valid){
                event.target.classList.add('is-invalid');
                event.target.classList.remove('is-valid');
              }else{
                event.target.classList.add('is-valid');
                event.target.classList.remove('is-invalid');
              }
            })
          .catch(e => {
            console.error('error making http request', e)
          })
      })
//        // Show success message on form submission
//        document.getElementById('loginForm').addEventListener('submit', function (event) {
//            event.preventDefault();
//            document.getElementById('successMessage').style.display = 'block';
//        });
    }, false);
})();