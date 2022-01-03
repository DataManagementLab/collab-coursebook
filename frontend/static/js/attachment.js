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

function test() {
    const numAttachments = parseInt($('#id_form-TOTAL_FORMS').val());
    for (let i = 0 ; i < numAttachments ; i ++) {
        var img = $("img[src='Image-" + i +"']",".toastui-editor-main-container");
        if (img.length) {
            fileInput = document.getElementById("id_form-" + i + "-image").files;
            if (fileInput.length && fileInput[0]['type'].split('/')[0] === 'image' && !(typeof URL_ARRAY[i] === undefined)) {
                img.attr('src',URL_ARRAY[i]);
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

        const id = document.getElementById('id_form-' + children + '-image');
        console.log("Field id:" + children);
        id.onchange = function() {
            console.log("Changes detected.")
            if (!(typeof URL_ARRAY[children] === 'undefined')) {
                    console.log("Revoking old URL entry..");
                    URL.revokeObjectURL(URL_ARRAY[children]);
                    var img = $("img[src='"+ URL_ARRAY[children] + "']",".toastui-editor-main-container");
                    if (img.length) {
                        console.log("Removing url from html..")
                        img.attr('src','Image-'+children);
                    }
            }
            if (id.files.length) {
                console.log("Creating new URL...")
                const url = URL.createObjectURL(id.files[0])
                URL_ARRAY[children] = url;
            }
            test();
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

    if (!(typeof URL_ARRAY[children - 1] === 'undefined')) {
        URL.revokeObjectURL(URL_ARRAY[children - 1]);
        var img = $("img[src='"+ URL_ARRAY[children] + "']",".toastui-editor-main-container");
        if (img.length) {
           img.attr('src','Image-'+(children-1));
        }
        URL_ARRAY.pop();
    }
}