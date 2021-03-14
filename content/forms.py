"""Purpose of this file

This file contains forms associated with the content types.
"""

from django import forms

from content.models import YTVideoContent, ImageContent, PDFContent
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


# dict[str, ModelForm]: Contains all available content types form.
CONTENT_TYPE_FORMS = {
    YTVideoContent.TYPE: AddContentFormYoutubeVideo,
    ImageContent.TYPE: AddContentFormImage,
    PDFContent.TYPE: AddContentFormPdf,
    TextField.TYPE: AddTextField,
    Latex.TYPE: AddLatex,
}
