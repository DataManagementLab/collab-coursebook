const FILE_OPTIONS_BUTTON = document.getElementById("id_options_0");
const TEXT_OPTIONS_BUTTON = document.getElementById("id_options_1");

const FILE_FIELD = document.getElementById("id_md");
const TEXT_FIELD = document.getElementById("id_textfield");
console.log(TEXT_FIELD);
const LABEL_FILE = $('label[for="id_md"]');
const LABEL_TEXT = $('label[for="id_textfield"]');
// $('.section-martor').hide();
//const TEST = document.getElementById('martor-textfield');
//ace.edit('martor-textfield').setReadOnly(true);

function updateOptionsState() {
    if (FILE_OPTIONS_BUTTON.checked) {
        disable(LABEL_TEXT, TEXT_FIELD);
        enable(LABEL_FILE, FILE_FIELD);
    }
    else if (TEXT_OPTIONS_BUTTON.checked) {
        disable(LABEL_FILE, FILE_FIELD);
        enable(LABEL_TEXT, TEXT_FIELD);
    }
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
    $('.tab-martor-menu').hide();
}

FILE_OPTIONS_BUTTON.addEventListener('click',updateOptionsState);
TEXT_OPTIONS_BUTTON.addEventListener('click',updateOptionsState);
// updateOptionsState();




