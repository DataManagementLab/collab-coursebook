/*
 This file contains the logic for controlling the behavior of the two radio buttons
 in the 'Options' field of the AddMD form.
*/
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
* Reads the uploaded file and copy the text content into the Markdown editor,
* if the file is valid.
*/
function copyFileContentToEditor() {
    let input = $('#id_md');
    const ready = $('#md-ready', '#md-preview-button');
    const loading = $('#md-loading', '#md-preview-button');
    const button = $('#md-preview-button');
    const ERROR_MESSAGE = gettext('Error while reading the file.');
    const CONFIRMATION_MESSAGE = gettext('There is currently text in the editor. Do you really want to replace the content in the editor with the content of the file?');
    const NO_FILES_MESSAGE = gettext("There are no files to read.");
    const INVALID_EXTENSIONS_MESSAGE = gettext("Invalid file extension. Please upload a 'md' file.");
    const SUCCESS_MESSAGE = gettext("Markdown file read successfully.");
    if (input.length && $(input[0].files).length && input[0].files.length){
        if (getExtension(input[0].files[0].name) == 'md') {
            button.attr('disabled','');
            ready.attr('style','display:none;');
            loading.attr('style','display:inline;');
            reader = new FileReader();
            reader.addEventListener('load', () => {
                if (editor.getMarkdown() == '' || window.confirm(CONFIRMATION_MESSAGE)) {
                    TEXT_BUTTON.click();
                    if (typeof reader.result == 'string') {
                        editor.hide();
                        editor.setMarkdown(reader.result);
                        editor.show();
                        showNotification(SUCCESS_MESSAGE, "alert-info");
                    }
                    else {
                        showNotification(ERROR_MESSAGE, "alert-danger");
                    }
                }
            });
            reader.addEventListener('error',() => {
                showNotification(ERROR_MESSAGE, "alert-danger");
            });
            reader.addEventListener('loadend', () => {
                button.removeAttr('disabled');
                loading.attr('style','display:none;');
                ready.attr('style','display:inline;');
            });
            reader.readAsText(document.getElementById('id_md').files[0]);
        }
        else {
            showNotification(INVALID_EXTENSIONS_MESSAGE, "alert-danger");
        }
    }
    else {
        showNotification(NO_FILES_MESSAGE, "alert-danger");
    }

}


