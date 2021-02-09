"""Purpose of this file

This file contains forms associated with the content.
"""

from django import forms
from django.utils.translation import ugettext as _

from base.models import Content


class AddContentForm(forms.ModelForm):
    """Add content form

    This model represents the add form for new content to a topic.
    """

    # pylint: disable=too-few-public-methods
    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        :attr Meta.model: The model to which this form corresponds
        :type Meta.model: Model
        :attr Meta.fields: Including fields into the form
        :type Meta.fields: List[str]
        :attr Meta.widgets: Customization of the model form
        :type Meta.widgets: Dict[str, Model field]
        """
        model = Content
        fields = ['description', 'language', 'tags', 'readonly', 'public']
        widgets = {
            'description': forms.Textarea(attrs={'style': 'height: 100px'}),
            'comment': forms.Textarea
        }


class EditContentForm(forms.ModelForm):
    """Add content form

    This model represents the add form for new content to a topic.

    :attr EditContentForm.change_log: The change log field which contains
    a detailed message what was edited
    :type EditContentForm.change_log: CharField
    :attr EditContentForm.field_order: The order of the fields
    :type EditContentForm.field_order: List(str)
    """

    change_log = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={'style': 'height: 35px'}),
        label=_('Change Log')
    )
    field_order = ['change_log', 'description', 'language', 'tags',
                   'readonly', 'public']

    # pylint: disable=too-few-public-methods
    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        :attr Meta.model: The model to which this form corresponds
        :type Meta.model: Model
        :attr Meta.fields: Including fields into the form
        :type Meta.fields: List[str]
        :attr Meta.widgets: Customization of the model form
        :type Meta.widgets: Dict[str, Model field]
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
    :type TranslateForm.TRANSLATE_CHOICE: List[Tuple[str, str]]
    :attr TranslateForm.translation: The field to enter the translation
    :type TranslateForm.translation: CharField
    """
    TRANSLATE_CHOICE = [('None', 'Translate into'), ('en', 'English'), ('de', 'German')]
    translation = forms.CharField(label='',
                                  widget=forms.Select(choices=TRANSLATE_CHOICE,
                                                      attrs={'class': 'form-control',
                                                             'style': 'width:auto',
                                                             'onchange': 'this.form.submit();'}))
