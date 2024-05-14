document.addEventListener('DOMContentLoaded', function(){

    // Select all input fields that were returned with an "aria-invalid" label after server side
    // form validation
    set_invalid(document.querySelectorAll('[aria-invalid="true"]'))
});


// Add bootstrap class "is-invalid" to invalid fields
function set_invalid(invalidInputs) {
    for(let i = 0; i < invalidInputs.length; i++) {
        invalidInputs[i].className += ' is-invalid';
    }
}




