/*
 This file contains the logic for controlling the behavior of the two radio buttons
 in the 'Options' field of the AddMD form.
*/
let fileButton;
let textButton;
let form_attach;

/**
 * This method updates the AddMD form by replacing the element with the provided label
 * with the element saved in form_attach, if an element with such label exists in the form.
 * The element's position is relative to the position of the 'Options' field in AddMD, so
 * the form can only be updated then the 'Options' field exists.
 * Furthermore, if nothing is saved in form_attach, then the element will simply be
 * detached from the form.
 * The element is detached from the form, instead of just hidden, so that when the user
 * submits the form, client-side validation for the detached element is also removed.

 * @param detachID label of the element to detach
 * @requires 'Options' field and the element with the provided label exists in the form.
*/
function changeForm(detachID) {
    const OPTION_FORM = $('#id_options').parent();
    let form_detach = $('label[for="' + detachID + '"]').parent();
    if (OPTION_FORM.length && form_detach.length) {
        // Append new element to options field
        if (form_attach != null) {
            OPTION_FORM.after(form_attach);
        }
        // Save old element to form_attach for reuse
        form_attach = form_detach.detach();
    }
}

/**
 * Checks which option is currently checked, then updates the form correspondingly.
*/
function updateFormState() {
    if (fileButton.checked) {
        changeForm('id_textfield');
    }
    else if (textButton.checked) {
        changeForm('id_md');
    }
}

/**
 * Adds listener to the two radio buttons in the add form so that
 * they can attach/reattach the corresponding fields when clicked.
*/
function initButtons() {
    fileButton = document.getElementById("id_options_0");
    textButton = document.getElementById("id_options_1");
    fileButton.addEventListener('click',updateFormState);
    textButton.addEventListener('click',updateFormState);
    updateFormState();
}
