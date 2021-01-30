"""Purpose of this file

This file contains forms associated with the content.
"""

from django import forms


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
