/**
 * Inserts an extra class which marks the label as required input.
 *
 * @param clazz div class name containing the label of the form field
 */
function markRequired(clazz) {
    const elements = document.getElementsByClassName(clazz);
    for (let element of elements) {
        for (let child of element.children) {
            if (child.hasAttribute('required')) {
                element.classList.add('form-required');
            }
        }
    }
}