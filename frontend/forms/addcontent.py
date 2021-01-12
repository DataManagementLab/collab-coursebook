"""Purpose of this file

This file contains forms associated with the addition content.
"""

from django import forms
from base.models.content import Content


class AddContentForm(forms.ModelForm):
    """Add content form

    This model represents the add form for new content to a topic.
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta options

        This class handles all possible meta options that you can give to this model.

        Attributes:
            Meta.model (Model): The model to which this form corresponds
            Meta.exclude (List[str]): Excluding fields
            Meta.widgets (Dict[str, Textarea]): Customization of the model form
        """
        model = Content
        exclude = ['attachment', 'topic', 'author', 'creation_date', 'ratings', 'preview', 'type']
        widgets = {
            'description': forms.Textarea(attrs={'style': 'height: 100px'}),
        }
