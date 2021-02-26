/**
 * Retrieve the cookie from the document.
 *
 * @param name the name of the cookie to be searched
 * @return {null} the cookie if it was found
 */
function getCookie(name) {
    // https://docs.djangoproject.com/en/3.1/ref/csrf/
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Sends a request to the given url with its given data and depending on the result of the request, do the specified tasks.
 * The arguments of this function are structured as follows:
 * - url: the url to send the request
 * - data: the data of the request
 * - success: the success task if the request was successfully
 * - error: the error task if the request was successfully
 *
 * @param args the arguments as dictionary
 */
function sendRequest(args) {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });
    $.ajax({
        url: args.url,
        type: 'POST',
        data: args.data,
        success: args.success,
        error: args.error
    });
}