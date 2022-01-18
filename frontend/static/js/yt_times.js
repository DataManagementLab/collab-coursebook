/**
 * Changes the states of the start and end element input fields to visible or invisible depending on their current state and
 * resets their values if setting them to invisible.
 */
function changeState() {
    var startElement = document.getElementById("id_startTime").parentElement;
    var endElement = document.getElementById("id_endTime").parentElement;
    startElement.style.display = startElement.style.display === "block" ? "none" : "block"; 
    endElement.style.display = endElement.style.display === "block" ? "none" : "block";

    if (startElement.style.display === "none") document.getElementById("id_startTime").value = 0;
    if (endElement.style.display === "none") document.getElementById("id_endTime").value = 0;
}

/**
 * Adds a listener to the checkbox with changeState() and initializes the input fields as invisible unless either has a 
 * non-zero value
 */
function initButtons() {
    var checkBox = document.getElementById("id_option");
    checkBox.addEventListener('click',changeState);

    var startElement = document.getElementById("id_startTime");
    var endElement = document.getElementById("id_endTime");

    startElement.parentElement.style.display = "none"
    endElement.parentElement.style.display = "none"

    valStartTime = startElement.value
    valEndTime = endElement.value

    if (valStartTime > 0 || valEndTime > 0) {
        checkBox.checked = true;
        changeState();
    }

}