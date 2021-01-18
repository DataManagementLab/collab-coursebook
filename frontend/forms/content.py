"""Purpose of this file

This file contains forms associated with the content.
"""

from django import forms


class TranslateForm(forms.Form):
    """Translate form

    This model represents form for translating markdown content.

    Attributes:
        TranslateForm.TRANSLATE_CHOICE (List[Tuple[str, str]]): The translation choices
        TranslateForm.translation (CharField): The field to enter the translation
    """
    TRANSLATE_CHOICE = [('None', 'Translate into'), ('en', 'English'), ('de', 'German')]
    translation = forms.CharField(label='',
                                  widget=forms.Select(choices=TRANSLATE_CHOICE,
                                                      attrs={'class': 'form-control',
                                                             'style': 'width:auto',
                                                             'onchange': 'this.form.submit();'}))
