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
            if (child.children !== null && seekRequired(child)) {
                element.classList.add('form-required');
            }
        }
    }
}

/**
 * Recursively seek an required child element if there exists one.
 *
 * @param obj element to check
 * @return {boolean|*} true if element contains a required field
 */
function seekRequired(obj) {
    const elements = obj.children;
    for (let element of elements) {
        for (let child of element.children) {
            if (child.hasAttribute('required')) {
                return true;
            }
            if (child.children !== null) {
                return seekRequired(child);
            }
        }
    }
    return false;
}