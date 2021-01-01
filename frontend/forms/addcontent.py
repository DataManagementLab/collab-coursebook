from django import forms
from base.models.content import Content


class AddContentForm(forms.ModelForm):
    """
    The Form for adding new content to a topic
    """
    class Meta:  # pylint: disable=too-few-public-methods
        model = Content
        exclude = ['topic', 'author', 'creation_date', 'ratings', 'preview', 'type']
