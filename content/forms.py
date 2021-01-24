"""Purpose of this file

This file contains forms associated with the content types.
"""

from django import forms
from django.forms import modelformset_factory
from content.models import YTVideoContent, ImageContent, PDFContent
from content.models import ImageAttachment, TextField, Latex, SingleImageAttachment
from content.widgets import ModifiedClearableFileInput



class AddContentFormYoutubeVideo(forms.ModelForm):
    """Add YouTube video

    This model represents the add form for YouTube videos.
    """

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        Attributes:
            Meta.model (Model): The model to which this form corresponds
            Meta.exclude (List[str]): Excluding fields
        """
        model = YTVideoContent
        exclude = ['content']


class AddContentFormImage(forms.ModelForm):
    """Add image content

    This model represents the add form for image contents.
    """

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        Attributes:
            Meta.model (Model): The model to which this form corresponds
            Meta.exclude (List[str]): Excluding fields
            Meta.widgets (Dict[str, Textarea]): Customization of the model form
        """
        model = ImageContent
        exclude = ['content']
        widgets = {
            'source': forms.Textarea(attrs={'style': 'height: 100px'}),
        }


class AddContentFormAttachedImage(forms.ModelForm):
    """Add attached image

    This model represents the add form for image attachments
    """

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        Attributes:
            Meta.model (Model): The model to which this form corresponds
            Meta.exclude (List[str]): Excluding fields
        """
        model = ImageAttachment
        exclude = ['images', 'content']


class AddContentFormPdf(forms.ModelForm):
    """Add PDF content

    This model represents the add form for PDF contents.
    """

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        Attributes:
            Meta.model (Model): The model to which this form corresponds
            Meta.exclude (List[str]): Excluding fields
            Meta.widgets (Dict[str, Textarea]): Customization of the model form
        """
        model = PDFContent
        exclude = ['license', 'content']
        widgets = {
            'source': forms.Textarea(attrs={'style': 'height: 100px'}),
            'pdf': ModifiedClearableFileInput(attrs={'accept': 'application/pdf'}),
        }


class AddTextField(forms.ModelForm):
    """Add text field

    This model represents the add form for text fields.
    """

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        Attributes:
            Meta.model (Model): The model to which this form corresponds
            Meta.exclude (List[str]): Excluding fields
            Meta.widgets (Dict[str, Textarea]): Customization of the model form
        """
        model = TextField
        exclude = ['content']
        widgets = {
            'source': forms.Textarea(attrs={'style': 'height: 100px', 'placeholder': 'https://www.lipsum.com/'}),
            'textfield': forms.Textarea(attrs={'placeholder': 'Lorem ipsum dolor sit amet, consectetur adipiscing '
                                                              'elit, sed do eiusmod tempor incididunt ut labore et '
                                                              'dolore magna aliqua. Ut enim ad minim veniam, '
                                                              'quis nostrud exercitation ullamco laboris nisi ut '
                                                              'aliquip ex ea commodo consequat. Duis aute irure dolor '
                                                              'in reprehenderit in voluptate velit esse cillum dolore '
                                                              'eu fugiat nulla pariatur. Excepteur sint occaecat '
                                                              'cupidatat non proident, sunt in culpa qui officia '
                                                              'deserunt mollit anim id est laborum.'})
        }


class AddLatex(forms.ModelForm):
    """Add LaTeX

    This model represents the add form for LaTeX code.
    """

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        Attributes:
            Meta.model (Model): The model to which this form corresponds
            Meta.exclude (List[str]): Excluding fields
            Meta.widgets (Dict[str, Textarea]): Customization of the model form
        """
        model = Latex
        exclude = ['content', 'pdf']
        widgets = {
            'source': forms.Textarea(attrs={'style': 'height: 100px', 'placeholder': 'https://ctan.org/pkg/lipsum'}),
            'textfield': forms.Textarea(
                attrs={'placeholder': 'This is a matrix \\\\ \n '
                                      '$ M = \\begin{pmatrix} 1 & 2 & 3\\\\ a & b & c \\end{ pmatrix}$ \\\\ \n'
                                      'This is a table \\\\ \n '
                                      '\\begin{center} \n \\begin{tabular} {||c c c c||} \n \\hline'
                                      'Col1 & Col2 & Col2 & Col3 \\\\ [0.5ex] \n \\hline \n \\hline \n '
                                      '1 & 6 & 87837 & 787 \\\\ \n \\hline \n'
                                      '\\end{tabular} \n \\end{center}'})
        }


class AddSingleImage(forms.ModelForm):
    """Add single image

    This model represents the add form for single images that is used for image attachments.
    """

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        Attributes:
            Meta.model (Model): The model to which this form corresponds
            Meta.exclude (List[str]): Excluding fields
            Meta.widgets (Dict[str, Textarea]): Customization of the model form
        """

        model = SingleImageAttachment
        exclude = []
        widgets = {
            'source': forms.Textarea(attrs={'style': 'height: 100px'}),
        }


# SingleImageFormSet: Image attachment form set
SingleImageFormSet = modelformset_factory(
    SingleImageAttachment,
    fields=("source", "license", "image"),
    extra=0,
    widgets={
        'source': forms.Textarea(attrs={'style': 'height: 100px', 'required': 'true'}),
        'image': ModifiedClearableFileInput(attrs={'required':'true'})
    }
)

# Dict[str, ModelForm]: Contains all available content types form.
CONTENT_TYPE_FORMS = {
    YTVideoContent.TYPE: AddContentFormYoutubeVideo,
    ImageContent.TYPE: AddContentFormImage,
    PDFContent.TYPE: AddContentFormPdf,
    ImageAttachment.TYPE: AddContentFormAttachedImage,
    TextField.TYPE: AddTextField,
    Latex.TYPE: AddLatex,
    SingleImageAttachment.TYPE: AddSingleImage
}
