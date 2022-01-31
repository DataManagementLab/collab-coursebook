"""Purpose of this file

This file contains forms associated with the attachments.
"""

from django import forms
from django.forms import BaseModelFormSet

from base.models import Content
from content.attachment.models import ImageAttachment, IMAGE_ATTACHMENT_TYPES
from content.widgets import ModifiedClearableFileInput
from django.utils.translation import gettext_lazy as _


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


class BaseLatexPreviewImageAttachmentFormset(BaseModelFormSet):
    """
    Formset used to override clean().

    Because formset is created with bulk adding in mind, a form in the formset will
    not be validated if it its fields are unchanged. Since an image attachment's file field
    is empty at start and will not be checked by default, a manual check has to be implemented.
    """
    def clean(self):
        super().clean()
        for form in self.forms:
            # Check for form validity; the form is still considered valid if its ImageField is empty
            # (initial state) so after the form is considered valid it still has to be checked again
            if form.is_valid():
                used_form = form.save(commit=False)
                if not used_form.image:
                    raise forms.ValidationError(_('This field is required.'))


# BaseModelFormSet: Image attachment form set, used for rendering LaTeX preview to remove validation for source field
LatexPreviewImageAttachmentFormSet = forms.modelformset_factory(
    ImageAttachment,
    fields=("image",),
    extra=0,
    widgets={
        'image': ModifiedClearableFileInput(attrs={'required': 'true'})
    },
    formset=BaseLatexPreviewImageAttachmentFormset
)
