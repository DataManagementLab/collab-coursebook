var checkBox;

function changeState(ID) {
    //const OPTION_FORM = $('#id_options').parent();
    //var form_detach = $('label[for="' + detachID + '"]').parent();
    //if (OPTION_FORM.length && form_detach.length) {
    //    if (form_attach != null) {
    //        OPTION_FORM.after(form_attach);
    //    }
    //    form_attach = form_detach.detach();
    //}

    const element = document.getElementById(ID);
    element.style.display = element.style.display === "block" ? "none" : "block";
}

function initButtons() {
    checkBox = document.getElementById("id_option");
    checkBox.addEventListener('click',updateOptionsState);
    changeState('id_startTime');
    changeState('id_endTime');
}