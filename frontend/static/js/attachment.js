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

        // Add listener to update URL when attachment changes
        // IS_MARKDOWN is a const declared in dynamic_attachment.html
        if (IS_MARKDOWN) {
            if (attachment.length) {
                addAttachmentEvent(attachment,children);
            }
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

    // Remove corresponding URL when attachment is removed
    if (IS_MARKDOWN) {
        if (URL_ARRAY[children - 1] != null) {
            revertAttachmentLinks(children-1);
            URL_ARRAY.pop();
        }
    }
}