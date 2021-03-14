"""Purpose of this file
This file contains forms associated with the version control history.
"""

from django import forms
from django.utils.translation import gettext_lazy as _


class HistoryForm(forms.ModelForm):
    """History form

    This model represents the history form which enables a change log option
    to note the changes made. The change log contains a detailed message what
    was edited.

    :attr HistoryForm.change_log: The change log
    :type HistoryForm.change_log: CharField
    """
    change_log = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={'style': 'height: 35px'}),
        label=_('Change Log'), help_text=_('Please write down your changes of this content')
    )
