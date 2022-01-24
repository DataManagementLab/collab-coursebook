let editor;
function initEditor() {
    let textArea = document.getElementById("id_textfield");
    let editorContainer = textArea.insertAdjacentElement('beforebegin',document.createElement('div'));
    editorContainer.classList.add('editor');
    editorContainer.setAttribute('id','editor');
    editor = new toastui.Editor({
      el: document.querySelector('#editor'),
      previewStyle: "vertical",
      height: "450px",
      initialEditType: "markdown",
	  usageStatistics: false,
	  previewHighlight: false,
	  placeholder: "Markdown Script",
    });
    document.getElementById("id_textfield").setAttribute("style","display:none")

    editor.removeToolbarItem("image");

    editor.on("change", function () {
      document.getElementById("id_textfield").value = editor.getMarkdown();
    });
}





