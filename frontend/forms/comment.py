from django import forms
from django.utils.translation import gettext_lazy as _


from base.models import Comment


class CommentForm(forms.ModelForm):
    """
    Form for entering comments
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Django Meta class
        """
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'cols': 15}),
        }

    def __init__(self, *args, **kwargs):
        """
        constructor overwritten to set form attributes
        :param args: constructor args
        :param kwargs: constructor kwargs
        """
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['text'].label = False
        self.fields['text'].widget.attrs['placeholder'] = _("Your Comment")
