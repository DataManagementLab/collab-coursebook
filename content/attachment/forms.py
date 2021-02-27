"""Purpose of this file

This file contains forms associated with the attachments.
"""

from django import forms

from base.models import Content
from content.attachment.models import ImageAttachment, IMAGE_ATTACHMENT_TYPES
from content.widgets import ModifiedClearableFileInput


class AdminImageAttachmentForm(forms.ModelForm):
    """Admin image attachment form

    This model represents the add form for image attachments in the admin panel.
    """

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        :attr Meta.model: Describes whether this model is an abstract model (class)
        :type Meta.model: bool
        :attr Meta.fields: Including fields into the form
        :type Meta.fields: str or list[str]
        """
        model = ImageAttachment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        """Initializer

        Initialize the admin image attachment form with pre configuration for the queryset which
        should only contains content types that allows embedded attachments..

        :param args: The arguments
        :type args: Any
        :param kwargs: The keyword arguments
        :type kwargs: dict[str, Any]
        """
        super().__init__(*args, **kwargs)
        self.fields['content'].queryset = Content.objects.filter(type__in=IMAGE_ATTACHMENT_TYPES)


# BaseModelFormset: Image attachment form set
ImageAttachmentFormSet = forms.modelformset_factory(
    ImageAttachment,
    fields=("source", "license", "image"),
    extra=0,
    widgets={
        'source': forms.Textarea(attrs={'style': 'height: 100px', 'required': 'true'}),
        'image': ModifiedClearableFileInput(attrs={'required': 'true'})
    }
)
