/**
 * Generates the menu list item for the item.
 * @param item item to be added to the list
 * @returns {string} html list item
 */
function buildItem(item) {
    // HTML code
    let html = "<li class='dd-item dd3-item' data-id='" + item.id + "'>";
    html += "\n";
    // Drag option
    html += "<div class='dd-handle dd3-handle'>Drag</div>";
    html += "\n";
    // Remove option
    html += "<a href='#' class='close close-assoc-file' data-dismiss='alert' aria-label='close'>&times;</a>"
    html += "\n";
    html += "<div class='dd3-content'>" + item.value + "</div>";

    // Sub topics
    if (item.children) {
        html += "<ol class='dd-list'>";
        $.each(item.children, function (index, sub) {
            html += buildItem(sub);
        });
        html += "</ol>";
    }
    html += "</li>";
    return html;
}

/**
 * Appends the new topic to the last of the nestable list.
 *
 * @param value the given topic to append
 * @param id id of the topic
 */
function addItem(value, id) {
    // Creates item
    const item = {value: value, id: id}

    // Adds to HTML
    const placeholder = document.getElementById('dd-empty-placeholder');
    placeholder.innerHTML += buildItem(item);
}

/**
 * Removes the clicked item for the nestable list.
 * @param event event
 */
function removeItem(event) {
    // Finds the closest list item to the clicked location
    const element = $(this).closest('li')
    // Removes the element with the given id
    const id = element.attr('data-id');
    $("#nestable3").nestable('remove', id);
}

/**
 * Parses the items from the string
 * @param obj the json object to be parsed
 */
function parseItems(obj) {
    // Cannot parse an empty json object
    if (obj === '[null]') {
        return;
    }
    // Parses json, dynamically generate a nestable list
    const placeholder = document.getElementById('dd-empty-placeholder');
    $.each(JSON.parse(obj), function (index, item) {
        // Adds to HTML
        placeholder.innerHTML += buildItem(item);
    });
}

/**
 * Cleans the nestable list from containing an empty class - 'dd-empty' which causes some bugs.
 * This bug occurs if the nestable list is initialized with an empty list and it will automatically
 * add an div with the class 'dd-empty' which represents an empty class and causes conflicts with
 * drag & drop items.
 */
function cleanNestable() {
    // Remove empty class from nestable to prevent bugs
    const dd_empty = document.getElementsByClassName("dd-empty");
    for (let i = 0; i < dd_empty.length; i++) {
        dd_empty[i].parentNode.removeChild(dd_empty[i]);
    }
}