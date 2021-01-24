"""Purpose of this file

This file describes alternative widgets
"""

from django.forms.widgets import ClearableFileInput


class ModifiedClearableFileInput(ClearableFileInput):
    """Widget for clearables file inputs

    This model is an alternative widget for clearable file inputs in formset
    """

    def get_context(self, name, value, attrs):
        ctx = super(ModifiedClearableFileInput, self).get_context(name, value, attrs)

        # If a value is currently entered in the field, entering another value is not required
        if value is not None:
            ctx['widget']['attrs']['required'] = False

        return ctx