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

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        :attr Meta.model: The model to which this form corresponds
        :type Meta.model: Model
        :attr Meta.fields: Including fields into the form
        :type Meta.fields: list[str]
        :attr Meta.widgets: Customization of the model form
        :type Meta.widgets: dict[str, Widget]
        """
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'cols': 15}),
        }

    def __init__(self, *args, **kwargs):
        """Initializer

        Initialize the comment form with pre configuration for the label and placeholder.

        :type request: HttpRequest
        :param args: The arguments
        :type args: Any
        :param kwargs: The keyword arguments
        :type kwargs: dict[str, Any]
        """
        super().__init__(*args, **kwargs)
        self.fields['text'].label = False
        self.fields['text'].widget.attrs['placeholder'] = _("Your Comment")
