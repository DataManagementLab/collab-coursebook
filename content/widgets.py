"""Purpose of this file

This file describes alternative widgets.
"""

from django.forms.widgets import ClearableFileInput


class ModifiedClearableFileInput(ClearableFileInput):
    """Widget for clearable file inputs

    This model represents an alternative widget for clearable file inputs in formset.

    :attr ModifiedClearableFileInput.template_name: The path to the html template
    :type ModifiedClearableFileInput.template_name: str
    """

    template_name = 'frontend/widgets/modified_clearable_file_input.html'

    def get_context(self, name, value, attrs):
        """Get context

        Clearable File Input Widget, which adapts to already inputted files at editing time.

       :param name: The name of the field
       :type name: str
       :param value: The value of the field e.g. ImageField: Image
       :type value: Any
       :param attrs: The the attributes of the widget
       :type attrs: dict[str, Any]

       :return: the context of the widget
       :rtype: dict
        """
        ctx = super().get_context(name, value, attrs)
        # If a value is currently entered in the field, entering another value is not required
        if value is not None:
            ctx['widget']['attrs']['required'] = False

        return ctx
