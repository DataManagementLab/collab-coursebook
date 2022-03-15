"""Purpose of this file

This file contains forms associated with the content types.
"""

from django import forms
from django.utils.translation import gettext_lazy as _

from content.models import MDContent, YTVideoContent, ImageContent, PDFContent
from content.models import TextField, Latex
from content.widgets import ModifiedClearableFileInput

# str: Relative directory path of the forms examples
FORMS_EXAMPLES_DIRECTORY = 'content/templates/form/examples/'

# str: File type of the forms examples
FORMS_EXAMPLES_FILE_TYPE = '.txt'


def get_placeholder(content_type, widget):
    """Get placeholder

    Reads the the file which represents placeholder of the corresponding
    widget of the specified content type. If the file could not be read,
    return an empty string.

    The path of the file structured as follows:
    directory + content type + _ + widget name + file type

    :param content_type: The type of the content of the placeholder
    :type content_type: str
    :param widget: The widget of the placeholder
    :type widget: str

    :return: the placeholder value
    :rtype: str
    """
    try:
        with open(FORMS_EXAMPLES_DIRECTORY +
                  content_type +
                  '_' +
                  widget
                  + FORMS_EXAMPLES_FILE_TYPE) as file:
            return file.read()
    # If file does not exists, return an empty string - no place holder value
    except FileNotFoundError:
        return ''


class AddContentFormYoutubeVideo(forms.ModelForm):
    """Add YouTube video

    This model represents the add form for YouTube videos.
    """

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        :attr Meta.model: The model to which this form corresponds
        :type Meta.model: Model
        :attr Meta.fields: Including fields into the form
        :type Meta.fields: str or list[str]
        """
        model = YTVideoContent
        fields = ['url', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.TextInput(
                attrs={
                    'placeholder': _("Default: 0:00")}),
            'end_time': forms.TextInput(
                attrs={
                    'placeholder': _("Default: 0:00")})
        }


class AddContentFormImage(forms.ModelForm):
    """Add image content

    This model represents the add form for image contents.
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
        model = ImageContent
        fields = ['image', 'source', 'license']
        widgets = {
            'source': forms.Textarea(attrs={'style': 'height: 100px'}),
            'image': ModifiedClearableFileInput(attrs={'required': 'true'})
        }


class AddContentFormPdf(forms.ModelForm):
    """Add PDF content

    This model represents the add form for PDF contents.
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
        model = PDFContent
        fields = ['pdf', 'source', 'license']
        widgets = {
            'source': forms.Textarea(attrs={'style': 'height: 100px'}),
            'pdf': ModifiedClearableFileInput(attrs={'accept': 'application/pdf',
                                                     'required': 'true'}),
        }


class AddTextField(forms.ModelForm):
    """Add text field

    This model represents the add form for text fields.
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
        model = TextField
        fields = ['textfield', 'source']
        widgets = {
            'source': forms.Textarea(
                attrs={
                    'style': 'height: 100px',
                    'placeholder': get_placeholder(TextField.TYPE, 'source')}),
            'textfield': forms.Textarea(
                attrs={
                    'placeholder': get_placeholder(TextField.TYPE, 'textfield')})
        }


class AddLatex(forms.ModelForm):
    """Add LaTeX

    This model represents the add form for LaTeX code.
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
        model = Latex
        fields = ['textfield', 'source']
        widgets = {
            'source': forms.Textarea(
                attrs={
                    'style': 'height: 100px',
                    'placeholder': get_placeholder(Latex.TYPE, 'source')}),
            'textfield': forms.Textarea(
                attrs={'placeholder': get_placeholder(Latex.TYPE, 'textfield')})
        }


class AddMD(forms.ModelForm):
    """Add Markdown

    This model represents the add form for Markdown code.
    """
    CHOICES = [
        ('file', _('Upload an existing Markdown file')),
        ('text', _('Write Markdown with editor')),
    ]
    options = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, initial='file')

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
        model = MDContent
        fields = ['options', 'md', 'textfield', 'source']
        widgets = {
            'source': forms.Textarea(
                attrs={
                    'style': 'height: 100px',
                    'placeholder': get_placeholder(MDContent.TYPE, 'source')}),
            'textfield': forms.Textarea(
                attrs={'placeholder': get_placeholder(MDContent.TYPE, 'textfield'),
                       'required': ''}),
            'md': ModifiedClearableFileInput(attrs={'accept': 'text/markdown',
                                                    'required': ''}),
        }

    def clean(self):
        cleaned_data = self.cleaned_data
        if 'options' in cleaned_data \
                and (cleaned_data['options'] == 'file' or cleaned_data['options'] == 'text'):
            options = cleaned_data['options']
            if options == 'file' and not ('md' in cleaned_data and bool(self.cleaned_data['md'])):
                raise forms.ValidationError(_("You must upload a Markdown file."))
            if options == 'text' \
                    and not ('textfield' in cleaned_data and bool(self.cleaned_data['textfield'])):
                raise forms.ValidationError(_("You must put in some text."))
        else:
            raise forms.ValidationError(_("None of the options were chosen."))


class EditMD(forms.ModelForm):
    """Edit Markdown

    This model represents the edit form for Markdown code, excluding the file field.
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
        model = MDContent
        fields = ['textfield', 'source']
        widgets = {
            'source': forms.Textarea(
                attrs={
                    'style': 'height: 100px',
                    'placeholder': get_placeholder(MDContent.TYPE, 'source')}),
            'textfield': forms.Textarea(
                attrs={'placeholder': get_placeholder(MDContent.TYPE, 'textfield'),
                       'required': ''}),
            'md': ModifiedClearableFileInput(attrs={'accept': 'text/markdown'}),
        }

    def clean(self):
        if not bool(self.cleaned_data['textfield']):
            raise forms.ValidationError(_("You must put in some text."))


# dict[str, ModelForm]: Contains all available content types form.
CONTENT_TYPE_FORMS = {
    YTVideoContent.TYPE: AddContentFormYoutubeVideo,
    ImageContent.TYPE: AddContentFormImage,
    PDFContent.TYPE: AddContentFormPdf,
    TextField.TYPE: AddTextField,
    Latex.TYPE: AddLatex,
    MDContent.TYPE: AddMD,
}
