"""Purpose of this file

This file contains forms associated with the content types.
"""

from django import forms
from django.forms import modelformset_factory
from content.models import YTVideoContent, ImageContent, PDFContent
from content.models import ImageAttachment, TextField, Latex, SingleImageAttachment
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

    :param content_type: the type of the content of the placeholder
    :type content_type: str
    :param widget: the widget of the placeholder
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
        :type Meta.fields: List[str]
        """
        model = YTVideoContent
        fields = ['url']


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
        :type Meta.fields: List[str]
        """
        model = ImageContent
        fields = ['image', 'source', 'license']
        widgets = {
            'source': forms.Textarea(attrs={'style': 'height: 100px'}),
            'image': ModifiedClearableFileInput(attrs={'required': 'true'})
        }


class AddContentFormAttachedImage(forms.ModelForm):
    """Add attached image

    This model represents the add form for image attachments
    """

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        :attr Meta.model: The model to which this form corresponds
        :type Meta.model: Model
        :attr Meta.fields: Including fields into the form
        :type Meta.fields: List[str]
        """
        model = ImageAttachment
        fields = []


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
        :type Meta.fields: List[str]
        :attr Meta.widgets: Customization of the model form
        :type Meta.widgets: Dict[str, Model field]
        """
        model = PDFContent
        fields = ['pdf', 'source']
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
        :type Meta.fields: List[str]
        :attr Meta.widgets: Customization of the model form
        :type Meta.widgets: Dict[str, Model field]
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
        :type Meta.fields: List[str]
        :attr Meta.widgets: Customization of the model form
        :type Meta.widgets: Dict[str, Model field]
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



# BaseModelFormset: Image attachment form set
SingleImageFormSet = modelformset_factory(
    SingleImageAttachment,
    fields=("source", "license", "image"),
    extra=0,
    widgets={
        'source': forms.Textarea(attrs={'style': 'height: 100px', 'required': 'true'}),
        'image': ModifiedClearableFileInput(attrs={'required': 'true'})
    }
)

# Dict[str, ModelForm]: Contains all available content types form.
CONTENT_TYPE_FORMS = {
    YTVideoContent.TYPE: AddContentFormYoutubeVideo,
    ImageContent.TYPE: AddContentFormImage,
    PDFContent.TYPE: AddContentFormPdf,
    TextField.TYPE: AddTextField,
    Latex.TYPE: AddLatex,
}
