"""Purpose of this file

This file describes the frontend views related to profiles.
"""

from django import forms

from base.models import Profile

from content.widgets import ModifiedClearableFileInput


class AddProfile(forms.ModelForm):
    """Add Profile

    This model represents the add form for user profiles.
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
        model = Profile
        fields = ['bio', 'pic']
        widgets = {
            'bio': forms.Textarea(attrs={'style': 'height: 100px'}),
            'pic': ModifiedClearableFileInput(attrs={'required': 'true'}),
        }
