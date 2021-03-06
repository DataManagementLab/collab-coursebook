"""Purpose of this file

This file contains forms associated with the content.
"""

from django import forms

from base.models import Content

from frontend.forms.history import HistoryForm


class AddContentForm(forms.ModelForm):
    """Add content form

    This model represents the add form for new content to a topic.
    """

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        :attr Meta.model: The model to which this form corresponds
        :type Meta.model: Model
        :attr Meta.fields: Including fields into the form
        :type Meta.fields: str or list[str]
        :attr Meta.widgets: Customization of the model form
        :type Meta.widgets: dict[str, Widget]
        """
        model = Content
        fields = ['description', 'language', 'tags', 'readonly', 'public']
        widgets = {
            'description': forms.Textarea(attrs={'style': 'height: 100px'}),
            'comment': forms.Textarea
        }


class EditContentForm(HistoryForm):
    """Add content form

    This model represents the edit form for changing content of a topic.

    :attr EditContentForm.field_order: The order of the fields
    :type EditContentForm.field_order: list(str)
    """
    field_order = ['change_log', 'description', 'language', 'tags',
                   'readonly', 'public']

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        :attr Meta.model: The model to which this form corresponds
        :type Meta.model: Model
        :attr Meta.fields: Including fields into the form
        :type Meta.fields: str or list[str]
        :attr Meta.widgets: Customization of the model form
        :type Meta.widgets: dict[str, Widget]
        """
        model = Content
        fields = ['description', 'language', 'tags', 'readonly', 'public']
        widgets = {
            'description': forms.Textarea(attrs={'style': 'height: 100px'}),
            'comment': forms.Textarea
        }


class TranslateForm(forms.Form):
    """Translate form

    This model represents form for translating markdown content.

    :attr TranslateForm.TRANSLATE_CHOICE: The translation choices
    :type TranslateForm.TRANSLATE_CHOICE: list[tuple[str, str]]
    :attr TranslateForm.translation: The field to enter the translation
    :type TranslateForm.translation: CharField
    """
    TRANSLATE_CHOICE = [('None', 'Translate into'), ('en', 'English'), ('de', 'German')]
    translation = forms.CharField(label='',
                                  widget=forms.Select(choices=TRANSLATE_CHOICE,
                                                      attrs={'class': 'form-control',
                                                             'style': 'width:auto',
                                                             'onchange': 'this.form.submit();'}))
