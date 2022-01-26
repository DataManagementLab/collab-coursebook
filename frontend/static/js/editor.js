/**
@ Editor used: ToastUI Editor version 3.1.2 | Mon Dec 27 2021
@ For further reference:
    https://nhn.github.io/tui.editor/latest/ [1]
    https://ui.toast.com/tui-editor [2]
    https://github.com/nhn/tui.editor [3]
*/
// Instance of markdown editor
let editor;
/**
* Creates an instance of ToastUI Editor and bind it to the Textfield where the user
* writes Markdown.
*
* @param args Options when creating an instance of the editor, see [1] for the options.
*/
function initEditor(args) {
    let textArea = document.getElementById("id_textfield");
    let editorContainer = textArea.insertAdjacentElement('beforebegin',document.createElement('div'));
    editorContainer.classList.add('editor');
    editorContainer.setAttribute('id','editor');
    // Setting up some basic options
    args['el'] = document.querySelector('#editor');
    args['usageStatistics'] = false;
    editor = new toastui.Editor(args)
    // Hide the textfield because the user will input text through the editor now
    // The text that is sent to the server is still the text in Textfield, not in editor.
    document.getElementById("id_textfield").setAttribute("style", "display:none")
    // Remove 'Attach image' button of editor because we use the Image Attachment application
    editor.removeToolbarItem("image");
    // When user writes something in editor, the text is also written in Textfield
    editor.on("change", function () {
      document.getElementById("id_textfield").value = editor.getMarkdown();
    });
}





