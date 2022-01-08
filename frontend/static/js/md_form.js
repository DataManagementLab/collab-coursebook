var fileButton;
var textButton;
var form_attach;

function changeState(detachID) {
    const OPTION_FORM = $('#id_options').parent();
    var form_detach = $('label[for="' + detachID + '"]').parent();
    if (OPTION_FORM.length && form_detach.length) {
        if (form_attach != null) {
            OPTION_FORM.after(form_attach);
        }
        form_attach = form_detach.detach();
    }
}

function updateOptionsState() {
    if (fileButton.checked) {
        changeState('id_textfield');
    }
    else if (textButton.checked) {
        changeState('id_md');
    }
}

function initButtons() {
    fileButton = document.getElementById("id_options_0");
    textButton = document.getElementById("id_options_1");
    fileButton.addEventListener('click',updateOptionsState);
    textButton.addEventListener('click',updateOptionsState);
    updateOptionsState();
}




