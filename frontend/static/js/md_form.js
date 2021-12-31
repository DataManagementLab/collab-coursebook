const FILE_OPTIONS_BUTTON = document.getElementById("id_options_0");
const TEXT_OPTIONS_BUTTON = document.getElementById("id_options_1");

const FILE_FIELD = document.getElementById("id_md");
const TEXT_FIELD = document.getElementById("id_textfield");
const LABEL_FILE = $('label[for="id_md"]');
const LABEL_TEXT = $('label[for="id_textfield"]');

var form_attach;
const OPTION_FORM = $('#id_options').parent();


function updateOptionsState() {
    if (FILE_OPTIONS_BUTTON.checked) {
        changeState('id_textfield');
    }
    else if (TEXT_OPTIONS_BUTTON.checked) {
        changeState('id_md');
    }
}

function changeState(detachID) {
    if (form_attach != null) {
        OPTION_FORM.after(form_attach);
    }
    var form_detach = $('label[for="' + detachID + '"]').parent();
    form_attach = form_detach.detach();
}

function disable(button, field) {
    button.attr("style","opacity:0.5");
    button.parent().removeClass('form-required')
    field.setAttribute('disabled',"true");
    field.removeAttribute('required');
}

function enable(button, field) {
    button.attr("style","opacity:1.0");
    button.parent().addClass('form-required')
    field.removeAttribute('disabled');
    field.setAttribute("style","opacity:1.0");
    field.setAttribute('required','');
}

FILE_OPTIONS_BUTTON.addEventListener('click',updateOptionsState);
TEXT_OPTIONS_BUTTON.addEventListener('click',updateOptionsState);
updateOptionsState();




