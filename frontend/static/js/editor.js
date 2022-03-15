/**
@ Editor used: ToastUI Editor version 3.1.2 | Mon Dec 27 2021
@ For further reference:
    https://nhn.github.io/tui.editor/latest/ [1]
    https://ui.toast.com/tui-editor [2]
    https://github.com/nhn/tui.editor [3]
*/
// Instance of markdown editor
let editor;

// Attachment list for editor
const ATTACHMENT_LIST = document.createElement('div');

// Array containing the URLs to the attachments for previewing
const URL_ARRAY = [];

// Help texts for add image button of editor
const HELP_TEXT = gettext('You can only add valid attachments.')
                    + '<br>'
                    + gettext('Invalid attachments will be grayed out.');
const EMPTY_TEXT = gettext('There are currently no attachments');
const ATTACHMENT_TEXT = gettext('Attachment');
// Allowed image extensions
const ALLOWED_EXTENSIONS = ['png','jpeg','jpg'];



/**
* Adds a button to insert attachment with the given ID to ATTACHMENT_LIST
* ID = -1 is reserved for the message that gets display when there are no attachments.
*
* @param id id of the attachment
*/
function appendAttachmentToList(id) {
    let button = document.createElement('button');
    button.classList.add('list-group-item');
    button.classList.add('list-group-item-action');
    button.setAttribute('type', 'button');
    button.setAttribute('style', 'margin-bottom: 1px');
    button.setAttribute('disabled','');
    // -1 is reserved for 'No attachments'
    if (id == -1)
        button.innerHTML = "There are currently no attachments."
    else {
        button.innerHTML = ATTACHMENT_TEXT + ' ' + id;
        button.addEventListener('click', () => {
            editor.eventEmitter.emit('command', 'addImage', {imageUrl: 'Image-' + id, altText: ''});
        });
    }
    ATTACHMENT_LIST.appendChild(button);
}

/**
* Removes the last button from ATTACHMENT_LIST, if there is at least 1 button currently in the list, i.e there are
* more than 2 elements in the list, since the list always contains 2 elements:
* the tooltip text and the text indicating no attachments.
*
* @requires There is at least one button on the list, also if there are more than 2 elements in the list.
*
*/
function popAttachmentFromList() {
    if (ATTACHMENT_LIST.children.length > 2)
        ATTACHMENT_LIST.removeChild(ATTACHMENT_LIST.lastElementChild);
        // Show the text indicating no attachments if there are no buttons left
        if (ATTACHMENT_LIST.children.length == 2)
            ATTACHMENT_LIST.children[1].style.display = '';
}

/**
* Creates an instance of ToastUI Editor and bind it to the Textfield where the user
* writes Markdown.
*
* @param args Options when creating an instance of the editor, see [1] for the options.
*/
function initEditor(args) {
    // Create container for editor
    let textArea = document.getElementById("id_textfield");
    let editorContainer = textArea.insertAdjacentElement('beforebegin',document.createElement('div'));
    editorContainer.classList.add('editor');
    editorContainer.setAttribute('id','editor');

    // Setting up some basic options
    args['el'] = document.querySelector('#editor');
    args['usageStatistics'] = false;
    editor = new toastui.Editor(args)

    // Hide the textfield because the user will input text through the editor now
    // The text that is sent to the server is still the text in Textfield, not in editor.
    document.getElementById("id_textfield").setAttribute("style", "display:none")

    // Remove 'Attach image' button of editor because we use the Image Attachment application
    editor.removeToolbarItem("image");

    // Initialize attachment list
    let helpTextBox = document.createElement('div');
    helpTextBox.innerHTML = HELP_TEXT;
    ATTACHMENT_LIST.setAttribute('id', 'markdown-attachment-list');
    ATTACHMENT_LIST.appendChild(helpTextBox);
    ATTACHMENT_LIST.classList.add('list-group');
    const NUM_ATTACHMENTS = parseInt($('#id_form-TOTAL_FORMS').val());
    for (let i = -1; i < NUM_ATTACHMENTS; i ++)
        appendAttachmentToList(i);
    if (NUM_ATTACHMENTS > 0)
        ATTACHMENT_LIST.children[1].style.display = 'none';

    // Add modified 'Attach image' button
    let imageButtonIndex = {
        groupIndex: 3,
        listIndex: 3,
    };
    let imageButton = {
        name: 'modified_image',
        tooltip: 'Insert image',
        className: 'image toastui-editor-toolbar-icons',
        popup: {
            body: ATTACHMENT_LIST,
            style: {width: 'auto'},
        },
    };
    editor.insertToolbarItem(imageButtonIndex, imageButton);

    // When user writes something in editor, the text is also written in Textfield
    editor.on("change", function () {
      document.getElementById("id_textfield").value = editor.getMarkdown();
      // Look for any attachment-embedding code and change the code to the corresponding URL if the URL exists
      updateAttachmentLinks();
    });
}

/**
 * Replaces all attachment-embedding codes inside the preview window of the editor
 * with the URLs of the corresponding image attachments that are saved in the
 * memory of the browser, if such URLs exist in URL_ARRAY.
 */
function updateAttachmentLinks() {
    if ($('#id_form-TOTAL_FORMS').length) {
        const NUM_ATTACHMENTS = parseInt($('#id_form-TOTAL_FORMS').val());
        for (let i = 0 ; i < NUM_ATTACHMENTS ; i ++) {
            // Find all the places where the embedding code is in the editor container
            let img = $("img[src='Image-" + i + "']",".toastui-editor-main-container");
            // If the URL exists and instances of the embedding code are found in the attachment, then replace
            if (img.length) {
                if (URL_ARRAY[i] != null) {
                    img.attr('src',URL_ARRAY[i]);
                }
            }
        }
    }
}

/**
 * Revokes the URL of the attachment saved in the memory of the browser, specified by the index argument,
 * effectively removing access to that attachment.
 * More specifically, the function:
 * - revokes the URL to the attachment.
 * - replaces all the instance of the URL in the preview window of the
 * editor with its attachment-embedding code;
 * - removes the URL from URL_ARRAY, which contains valid URLs of the temporarily saved attachments.
 * @param index index of the URL inside URL_ARRAY, which also implies the corresponding attachment-embedding code
 */
function revertAttachmentLinks(index) {
    // Assuming element at index is not undefined
    URL.revokeObjectURL(URL_ARRAY[index]);
    let img = $("img[src='"+ URL_ARRAY[index] + "']",".toastui-editor-main-container");
    if (img.length) {
       img.attr('src','Image-'+ index);
    }
    delete URL_ARRAY[index];
}

/**
* Returns the extension of a file name.
* @param filename name of the file
* @returns extension of the file
*/
function getExtension(filename) {
    return filename.substring(filename.lastIndexOf('.')+1, filename.length) || filename;
}

/**
 * Checks if a given <input> element currently has a file and if that file is an image with an allowed extension,
 * based on its MIME type and ALLOWED_EXTENSIONS.
 * @param input HTMLInputElement
 * @return True if input has a file and that file is an image, False otherwise
 */
function validateInput(input) {
   return input.files.length
        && input.files[0]['type'].split('/')[0] === 'image'
        && ALLOWED_EXTENSIONS.includes(getExtension(input.files[0].name));
}

/**
 * Creates an URL for the first file of the given <input> element and
 * saves it to the given index in URL_ARRAY for further use.
 * @param input HTMLInputElement input
 * @param idx index to save URL to.
 */
function generateNewAttachmentURLs(input, idx) {
    const url = URL.createObjectURL(input.files[0]);
    URL_ARRAY[idx] = url;
}

/**
 * This function adds an event to the attachment, so that everytime it changes
 * (more specifically, the file underlying changes), the URL of the old attachment
 * will get removed and replaced by the URL of the new attachment, if the attachment.
 * Else the URL will get replaced by its attachment-embedding code.
 * @param attachment attachment to add event to
 * @param id index of the old URL in URL_ARRAY, which also indicates index of the attachment in the list of attachments
 * @requires attachment.length
*/
function addAttachmentEvent(attachment, id) {
    // Assume attachment exists
    attachment.on("change",function() {
        // Revert old attachment URL
        if (URL_ARRAY[id] != null) {
            revertAttachmentLinks(id);
        }
        // Change name of the attachment in the list
        ATTACHMENT_LIST.children[id+2].innerHTML = ATTACHMENT_TEXT + ' ' + id;
        if (this.files.length)
            ATTACHMENT_LIST.children[id+2].innerHTML += ": " + this.files[0].name;
        // Generate new URL only when attachment is valid
        if (validateInput(this)) {
            generateNewAttachmentURLs(this,id);
            updateAttachmentLinks();
            ATTACHMENT_LIST.children[id+2].removeAttribute('disabled');
        }
        else {
            ATTACHMENT_LIST.children[id+2].setAttribute('disabled','');
        }
    });
}

/**
 * Creates, for each attachment that already was in the form when it was loaded,
 * an object URL, and saves that URL to URL_ARRAY for further use.
 * The function then adds a listener to the existing attachment so the URL of the
 * attachment is changed corresponding to attachment change.
 * This function is developed to use when loading the edit form, because in an add
 * form there should be no existing attachments.
*/
function generateExistingAttachmentURLs() {
    if ($('#id_form-TOTAL_FORMS').length) {
        const numAttachments = parseInt($('#id_form-TOTAL_FORMS').val());
        for (let i = 0 ; i < numAttachments ; i ++) {
            let attachment = $('#id_form-' + i + '-image');
            // If attachment actually exists, i.e the edit form has no error loading
            if (attachment.length && attachment.parent().length && attachment.parent().parent().length) {
                // Get existing URL from the "Currently" field of the attachment
                let existingURL = $("a",attachment.parent().parent());
                if (existingURL.length) {
                    let url_string = existingURL.attr("href");
                    URL_ARRAY[i] = url_string;
                    // Update name of the attachment in the attachment list
                    ATTACHMENT_LIST.children[i+2].innerHTML += ": " + url_string.split('\\').pop().split('/').pop();
                }
                // Add listener to react to changes
                addAttachmentEvent(attachment,i);
                // Enable buttons to insert images in editor
                ATTACHMENT_LIST.children[i+2].removeAttribute('disabled');
            }
        }
    }
}