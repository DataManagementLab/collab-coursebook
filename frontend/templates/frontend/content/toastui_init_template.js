// console.log(id);
// $(".fieldBox").attr('id','test');
var textArea = document.getElementById("id_editor");
// $('label[for="id_editor"]').after("<div class=editor id=editor> </div>");
editorElement = textArea.parentElement.insertAdjacentElement('beforebegin',document.createElement('div'));
editorElement.classList.add('editor');
editorElement.setAttribute('id','editor');
const editor = new toastui.Editor({
      el: document.querySelector('#editor'),
      previewStyle: "vertical",
      height: "300px",
      initialEditType: "wysiwyg",
	  usageStatistics: false,
	  placeholder: "Markdown"
    });
editor.removeToolbarItem("image");
editor.on("change", function () {
      textArea.value = editor.getMarkdown();
    });
// textArea.setAttribute('style','display:none');

