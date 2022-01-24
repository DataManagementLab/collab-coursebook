// Max attachments
const MAX_ATTACHMENT = 20;

// Restore deleted values
const STACK = [];

const ADD_BUTTON = document.getElementById("add-item-button")
const REMOVE_BUTTON = document.getElementById("remove-item-button")

// Number of children
const CHILDREN = $('#items-form-container').children().length;

// Beginning Visibility
ADD_BUTTON.style.visibility = CHILDREN < MAX_ATTACHMENT ? "visible" : "hidden";
REMOVE_BUTTON.style.visibility = CHILDREN === 0 ? "hidden" : "visible";

const URL_ARRAY = [];

function updateAttachmentLinks() {
    if ($('#id_form-TOTAL_FORMS').length) {
    console.log("Replacing all instances of image attachments with corresponding link..");
    const numAttachments = parseInt($('#id_form-TOTAL_FORMS').val());
    for (let i = 0 ; i < numAttachments ; i ++) {
        var img = $("img[src='Image-" + i +"']",".toastui-editor-main-container");
        if (img.length) {
            //fileInput = document.getElementById("id_form-" + i + "-image").files;
            if (/*fileInput.length && fileInput[0]['type'].split('/')[0] === 'image' && */URL_ARRAY[i] != null) {
                img.attr('src',URL_ARRAY[i]);
            }

        }
    }
    }
}

function revertAttachmentLinks(index) { // Assuming element at index is not undefined
    console.log("Revoking old URL entry..");
    URL.revokeObjectURL(URL_ARRAY[index]);
    var img = $("img[src='"+ URL_ARRAY[index] + "']",".toastui-editor-main-container");
    if (img.length) {
       console.log("Removing url from html..")
       img.attr('src','Image-'+ index);
    }
    delete URL_ARRAY[index];
}

function validateInput(input) {
   return input.files.length && input.files[0]['type'].split('/')[0] === 'image';
}

function generateNewAttachmentURLs(id, children) {

            console.log("Generating new URL...");
            const url = URL.createObjectURL(id.files[0]);
            URL_ARRAY[children] = url;
}

function addAttachmentEvent(attachment, id) {
    // Assume attachment exists
    attachment.on("change",function() {
        console.log("Changes detected.");
        if (URL_ARRAY[id] != null) {
            revertAttachmentLinks(id);
        }
        if (validateInput(this)) {
            generateNewAttachmentURLs(this,id);
            updateAttachmentLinks();
        }
    });
}

function generateExistingAttachmentURLs() {
    if ($('#id_form-TOTAL_FORMS').length) {
    const numAttachments = parseInt($('#id_form-TOTAL_FORMS').val());
    console.log("There are " + numAttachments + " attachments.");
    for (let i = 0 ; i < numAttachments ; i ++) {
        var attachment = $('#id_form-' + i + '-image');
        if (attachment.length && attachment.parent().length && attachment.parent().parent().length) {
            var existingURL = $("a",attachment.parent().parent());
            if (existingURL.length) {
                console.log("Populating URL_ARRAY at pos " + i);
                URL_ARRAY[i] = existingURL.attr("href");
            }
            addAttachmentEvent(attachment,i);
        }
    }
    }
}


/**
 * Adds an attachment form to the current attachment div. Additionally
 * update the visibility of the add and remove button depending on the
 * number of visible attachment forms.
 *
 * @param event event
 */
function addAttachment(event) {
    event.preventDefault();

    REMOVE_BUTTON.style.visibility = "visible";

    // Number of children
    const children = $('#items-form-container').children().length;

    // Update visibility of add attachment button
    if (children + 1 === MAX_ATTACHMENT) {
        // After this operation we increased the number of children by one
        ADD_BUTTON.style.visibility = "hidden";
    }

    // Add an image attachment form
    if (MAX_ATTACHMENT !== children) {
        const tmplMarkup = $('#item-template').html();
        const compiledTmpl = tmplMarkup.replace(/__prefix__/g, children);

        // Add form
        $('div#items-form-container').append(compiledTmpl);

        if (STACK.length > 0) {
            const value = STACK.pop();
            const id = document.getElementById('id_form-' + children + '-id');
            id.setAttribute('value', value);
        }

        // Restore value
        if (STACK.length > 0) {
            const id = document.getElementById('id_form-' + (children - 1) + '-id');
            id.setAttribute('value', STACK.pop());
        }

        // Update form count
        $('#id_form-TOTAL_FORMS').attr('value', children + 1);
        const attachment = $('#id_form-' + children + '-image');
        if (attachment.length) {
            console.log("Field id:" + children);
            addAttachmentEvent(attachment,children);
        }
    }
}

/**
 * Removes an attachment form to the current attachment div. Additionally
 * update the visibility of the add and remove button depending on the
 * number of visible attachment forms.
 * @param event event
 */
function removeAttachment(event) {
    event.preventDefault();

    ADD_BUTTON.style.visibility = "visible";

    // Number of children
    const children = $('#items-form-container').children().length;

    // Update visibility of add attachment button
    if (children - 1 === 0) {
        // After this operation we decreased the number of children by one
        REMOVE_BUTTON.style.visibility = "hidden";
    }

    // Revert option
    const id = document.getElementById('id_form-' + (children - 1) + '-id');
    const value = id.getAttribute('value');

    if (value !== null) {
        STACK.push(value);
    }

    // Remove last child
    const container = document.getElementById('items-form-container');

    container.removeChild(container.lastElementChild);

    // Update form count
    $('#id_form-TOTAL_FORMS').attr('value', children - 1);

    if (URL_ARRAY[children - 1] != null) {
        revertAttachmentLinks(children-1);
        URL_ARRAY.pop();
    }
}