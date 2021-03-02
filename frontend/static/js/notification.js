/**
 * The timeout value for fade out.
 * @type {number}
 */
const TIMEOUT = 5000;

/**
 * Hides the notification element.
 */
function hideNotification() {
    $('#notification').fadeOut();
}

/**
 * Shows the notification element with the given message. Additionally we can add a class style
 * to the notification which will be added and removed after this call.
 *
 * @param message message of the notification
 * @param clazz optional class style to be added
 */
function showNotification(message, clazz = "") {
    const parent = document.getElementById('notification');
    const element = document.getElementById('notification-message');

    parent.classList.add(clazz)
    element.innerText = message;

    $('#notification').fadeIn();
    setTimeout(function () {
            $('#notification').fadeOut();
            parent.classList.remove(clazz);
            element.innerText = "";
        }, TIMEOUT
    );
}