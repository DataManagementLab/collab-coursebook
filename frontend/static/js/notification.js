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
 * Hides the notification element 
 * @param id the id of the notification element
 */

function hideNotificationCopy(id) {
    $('#notification-copy-'+ id).fadeOut();
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

/**
 * Shows the notification element with the given message. Additionally we can add a class style
 * to the notification which will be added and removed after this call.
 *
 * @param message message of the notification
 * @param clazz optional class style to be added
 * @param id the id of the given element
 */

function showNotificationCopy(message, clazz = "", id) {
    const parent = document.getElementById('notification-copy-'+ id);
    const element = document.getElementById('notification-message-copy-'+ id);

    parent.classList.add(clazz)
    element.innerText = message;

    $('#notification-copy-'+ id).fadeIn();
    setTimeout(function () {
            $('#notification-copy-'+ id).fadeOut();
            parent.classList.remove(clazz);
            element.innerText = "";
        }, TIMEOUT
    );
}