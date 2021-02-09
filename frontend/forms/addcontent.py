"""Purpose of this file

This file contains forms associated with the addition content.
"""

from django import forms
from django.utils.translation import ugettext as _

from base.models.content import Content


class AddContentForm(forms.ModelForm):
    """Add content form

    This model represents the add form for new content to a topic.
    """

    # pylint: disable=too-few-public-methods
    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        :attr Meta.model: The model to which this form corresponds
        :type Meta.model: Model
        :attr Meta.fields: Including fields into the form
        :type Meta.fields: List[str]
        :attr Meta.widgets: Customization of the model form
        :type Meta.widgets: Dict[str, Model field]
        """
        model = Content
        fields = ['description', 'language', 'tags', 'readonly', 'public']
        widgets = {
            'description': forms.Textarea(attrs={'style': 'height: 100px'}),
            'comment': forms.Textarea
        }


class EditContentForm(forms.ModelForm):
    """Add content form

    This model represents the add form for new content to a topic.
    """

    change_log = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={'style': 'height: 35px'}),
        label=_('Change Log')
    )

    # pylint: disable=too-few-public-methods
    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        :attr Meta.model: The model to which this form corresponds
        :type Meta.model: Model
        :attr Meta.fields: Including fields into the form
        :type Meta.fields: List[str]
        :attr Meta.widgets: Customization of the model form
        :type Meta.widgets: Dict[str, Model field]
        """
        model = Content
        fields = ['description', 'language', 'tags', 'readonly', 'public']
        widgets = {
            'description': forms.Textarea(attrs={'style': 'height: 100px'}),
            'comment': forms.Textarea
        }

    field_order = ['change_log', 'description', 'language', 'tags',
                   'readonly', 'public', 'description', 'comment']
