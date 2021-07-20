from django import forms
from django.utils.translation import gettext_lazy as _


class AcceptPrivacyNoteForm(forms.Form):
    accept = forms.BooleanField(label=_("I accept the privacy note"),
                                help_text=_("(required to use this website)"))
