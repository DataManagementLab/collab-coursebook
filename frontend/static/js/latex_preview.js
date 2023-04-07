// URL of the latest PDF for previewing
let currentURL;
/**
 * Submits the necessary data to the server requesting a preview PDF of the
 * LaTeX content.
 * If the request is successful, the PDF sent from the server is saved into
 * memory and given an URL for access.
 * If the request is unsuccessful, the server sends back a response containing
 * the reason for failure.
 *
 * @param args data for the Ajax request
 * @returns jqXHR object which implements the Promise object
 */
function sendPreviewRequest(args) {
    // Get preview frame
    const previewFrame = document.getElementById("preview_frame");
    // Remove visibility of the preview frame every time a preview request is sent
    previewFrame.setAttribute("style","display:none")
    // Get form data
    const form = document.getElementsByClassName("post-form")[0];
    const formData = new FormData(form);
    // Add key to the form to indicate a preview request is sent
    formData.set('latex-preview', true);
    // Delete csrf token; for each call of the function a new csrf token must be generated
    formData.delete('csrfmiddlewaretoken');
    // Get CSRF token
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });
    // Ajax request
    return $.ajax({
        xhrFields: {responseType: 'blob'},
        url: args.url,
        type: "POST",
        data: formData,
        contentType: false,
        processData: false,
        success: function (data, status, jqxhr) {
            reason = jqxhr.statusText;
            if (reason == "OK") {
                data.name = "preview.pdf";
                newURL = URL.createObjectURL(data);
                // Destroy old preview before generating url for new preview, if an old preview exists
                if (currentURL != null)
                    URL.revokeObjectURL(currentURL);
                // Update url in the preview frame
                previewFrame.setAttribute("src", newURL)
                currentURL = newURL;
                const message = gettext("Preview successfully generated.");
                showNotification(message, "alert-info");
                // Return visibility for preview frame
                previewFrame.removeAttribute("style");
            }
            else {
                const message = gettext("Failed to generate preview - reason: " + reason + ".");
                showNotification(message, "alert-danger");
            }
        },
        error: function (data) {
            const message = gettext("Error during data transfer to the server - status: %s");
            showNotification(interpolate(message, [data.status]), "alert-danger");
        },
    });
}
