const FILE_OPTIONS_BUTTON = document.getElementById("id_options_0")
const TEXT_OPTIONS_BUTTON = document.getElementById("id_options_1")

const FILE_FIELD = document.getElementById("id_md")
const TEXT_FIELD = document.getElementById("id_textfield")
const LABEL_FILE = $('label[for="id_md"]')
const LABEL_TEXT = $('label[for="id_textfield"]')

// At the start the markdown text field is disabled to the label is grayed out
LABEL_TEXT.attr("style","opacity:0.5")

function uploadAsFile(event) {
    LABEL_TEXT.attr("style","opacity:0.5")
    TEXT_FIELD.setAttribute('disabled',"true")

    LABEL_FILE.attr("style","opacity:1.0")
    FILE_FIELD.removeAttribute('disabled')
    FILE_FIELD.setAttribute("style","opacity:1.0")
}

function uploadAsText(event) {
    LABEL_FILE.attr("style","opacity:0.5")
    FILE_FIELD.setAttribute('disabled',"true")
    FILE_FIELD.setAttribute("style","opacity:0.5")

    LABEL_TEXT.attr("style","opacity:1.0")
    TEXT_FIELD.removeAttribute('disabled')
}


FILE_OPTIONS_BUTTON.addEventListener('click',uploadAsFile)
TEXT_OPTIONS_BUTTON.addEventListener('click',uploadAsText)
