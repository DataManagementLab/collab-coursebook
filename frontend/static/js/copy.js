/**
 * Returns the text as the user had copied the text.
 *
 * @param text text be be copied
 */
function copy(text) {
    const tmp = document.createElement('textarea');
    tmp.value = text;
    document.body.appendChild(tmp);
    tmp.select();
    document.execCommand("copy");
    document.body.removeChild(tmp);
}