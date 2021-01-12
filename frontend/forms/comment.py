"""Purpose of this file

This file contains forms associated with the comments.
"""

from django import forms
from django.utils.translation import gettext_lazy as _

from base.models import Comment


class CommentForm(forms.ModelForm):
    """Comment form

    This model represents form for entering comments.
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta options

        This class handles all possible meta options that you can give to this model.

        Attributes:
            Meta.model (Model): The model to which this form corresponds
            Meta.exclude (List[str]): Excluding fields
        """
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'cols': 15}),
        }

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['text'].label = False
        self.fields['text'].widget.attrs['placeholder'] = _("Your Comment")
