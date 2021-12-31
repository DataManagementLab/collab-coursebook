// console.log(id);
// $(".fieldBox").attr('id','test');
var textArea = document.getElementById("id_textfield");
// $('label[for="id_editor"]').after("<div class=editor id=editor> </div>");
editorElement = textArea.parentElement.insertAdjacentElement('beforebegin',document.createElement('div'));
editorElement.classList.add('editor');
editorElement.setAttribute('id','editor');
const editor = new toastui.Editor({
      el: document.querySelector('#editor'),
      previewStyle: "vertical",
      height: "450px",
      initialEditType: "wysiwyg",
	  usageStatistics: false,
	  placeholder: "Markdown Script"
    });
editor.removeToolbarItem("image");
editor.on("change", function () {
      textArea.value = editor.getMarkdown();
    });
// Function from md_form.js
updateOptionsState();

// textArea.setAttribute('style','display:none');

