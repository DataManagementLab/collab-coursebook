let editor;
function initEditor() {
    let textArea = document.getElementById("id_textfield");
    let editorContainer = textArea.insertAdjacentElement('beforebegin',document.createElement('div'));
    editorContainer.classList.add('editor');
    editorContainer.setAttribute('id','editor');
    editor = new toastui.Editor({
      el: document.querySelector('#editor'),
      previewStyle: "vertical",
      height: "450px",
      initialEditType: "markdown",
	  usageStatistics: false,
	  previewHighlight: false,
	  placeholder: "Markdown Script",
    });
    document.getElementById("id_textfield").setAttribute("style","display:none")
    // Remove image button because image attachments system is used to embed image
    editor.removeToolbarItem("image");

    editor.on("change", function () {
      document.getElementById("id_textfield").value = editor.getMarkdown();
      // Look for any attachment-embedding code and change the code to the corresponding URL if the URL exists
      updateAttachmentLinks();
    });
}

const URL_ARRAY = [];

/**
 * Replaces all attachment-embedding codes inside the preview window of the editor
 * with the URLs of the corresponding image attachments that are saved in the
 * memory of the browser, if such URLs exist in URL_ARRAY.
 *
 */
function updateAttachmentLinks() {
    if ($('#id_form-TOTAL_FORMS').length) {
        const numAttachments = parseInt($('#id_form-TOTAL_FORMS').val());
        for (let i = 0 ; i < numAttachments ; i ++) {
            // Find all the places where the embedding code is in the editor container
            var img = $("img[src='Image-" + i + "']",".toastui-editor-main-container");
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
 *
 */
function revertAttachmentLinks(index) {
    // Assuming element at index is not undefined
    URL.revokeObjectURL(URL_ARRAY[index]);
    var img = $("img[src='"+ URL_ARRAY[index] + "']",".toastui-editor-main-container");
    if (img.length) {
       img.attr('src','Image-'+ index);
    }
    delete URL_ARRAY[index];
}

/**
 * Checks if a given <input> element currently has a file and if that file is an image, based
 * on its MIME type.
 * @param input HTMLInputElement
 * @return True if input has a file and that file is an image, False otherwise
 */
function validateInput(input) {
   return input.files.length && input.files[0]['type'].split('/')[0] === 'image';
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
        // Generate new URL only when attachment is valid
        if (validateInput(this)) {
            generateNewAttachmentURLs(this,id);
            updateAttachmentLinks();
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
 *
*/
function generateExistingAttachmentURLs() {
    if ($('#id_form-TOTAL_FORMS').length) {
        const numAttachments = parseInt($('#id_form-TOTAL_FORMS').val());
        for (let i = 0 ; i < numAttachments ; i ++) {
            var attachment = $('#id_form-' + i + '-image');
            // If attachment actually exists, i.e the edit form has no error loading
            if (attachment.length && attachment.parent().length && attachment.parent().parent().length) {
                // Get existing URL from the "Currently" field of the attachment
                var existingURL = $("a",attachment.parent().parent());
                if (existingURL.length) {
                    URL_ARRAY[i] = existingURL.attr("href");
                }
                // Add listener to react to changes
                addAttachmentEvent(attachment,i);
            }
        }
    }
}

