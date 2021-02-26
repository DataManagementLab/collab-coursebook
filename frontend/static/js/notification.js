/**
 * Hides the notification element.
 */
function hideNotification() {
    $('#notification').fadeOut();
}

/**
 * Shows the notification element with the given message.
 * @param message message of the notification
 */
function showNotification(message) {
    document.getElementById('notification-message').innerText = message;
    $('#notification').fadeIn();
    setTimeout(function () {
            $('#notification').fadeOut();
        }, 5000
    );
}