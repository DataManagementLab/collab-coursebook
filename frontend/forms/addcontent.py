from django import forms
from base.models.content import Content
from content.models import YTVideoContent, ImageContent


class AddContentForm(forms.ModelForm):
    """
    The Form for adding new content to a topic
    """
    class Meta:  # pylint: disable=too-few-public-methods
        model = Content
        exclude = ['topic', 'author', 'creation_date', 'ratings', 'preview']


class AddContentFormYoutubeVideo(forms.ModelForm):
    class Meta:
        model = YTVideoContent
        exclude = ['content']


class AddContentFormImage(forms.ModelForm):
    class Meta:
        model = ImageContent
        exclude = ['content']
