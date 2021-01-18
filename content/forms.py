"""Purpose of this file

This file contains forms associated with the content types.
"""

from django import forms
from django.forms import modelformset_factory

from content.models import YTVideoContent, ImageContent, PDFContent
from content.models import ImageAttachment, TextField, Latex, SingleImageAttachment


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
            'pdf': forms.FileInput(attrs={'accept': 'application/pdf'}),
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
            'source': forms.Textarea(attrs={'style': 'height: 100px', 'placeholder': 'https://www.uni-bielefeld.de'
                                                                                     '/lili/forschung/projekte/archiv'
                                                                                     '/L2-pro/text.html'}),
            'textfield': forms.Textarea(attrs={'placeholder': 'Den Körper trainieren viele Menschen. Aber wer '
                                                              'trainiert auch sein Gehirn? „Das Gehirn muss genauso '
                                                              'trainiert werden wie der Körper“, sagt Professor '
                                                              'Siegfried Lehrl von der Universität '
                                                              'Erlangen-Nürnberg. Denn wissenschaftliche '
                                                              'Untersuchungen haben gezeigt, dass wir die '
                                                              'Leistungsfähigkeit unseres Gehirns um 10 bis 15% '
                                                              'steigern können, wenn wir einige Wochen lang täglich '
                                                              'zehn Minuten unser Gehirn trainieren.'})
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
                attrs={'placeholder': 'Quisque ullamcorper placerat ipsum. '
                                      'Cras nibh. Morbi vel justo vitae lacus tincidunt ultrices. '
                                      'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. '
                                      'In hac habitasse platea dictumst. Integer tempus convallis augue. '
                                      'Etiam facilisis. Nunc elementum fermentum wisi. Aenean placerat. '
                                      'Ut imperdiet, enim sed gravida sollicitudin, felis odio placerat quam, '
                                      'ac pulvinar elit purus eget enim. Nunc vitae tortor. Proin tempus nibh sit '
                                      'amet nisl. '
                                      'Vivamus quis tortor vitae risus porta vehicula. \\br '
                                      'Fusce mauris. Vestibulum '
                                      'luctus nibh at lectus. Sed bibendum, nulla a faucibus semper, '
                                      'leo velit ultricies tellus, ac venenatis arcu wisi vel nisl. Vestibulum diam. '
                                      'Aliquam pellentesque, augue quis sagittis posuere, turpis lacus congue quam, '
                                      'in hendrerit risus eros eget felis. Maecenas eget erat in sapien mattis '
                                      'porttitor. Vestibulum porttitor. Nulla facilisi. Sed a turpis eu lacus commodo '
                                      'facilisis. Morbi fringilla, wisi in dignissim interdum, justo lectus sagittis '
                                      'dui, et vehicula libero dui cursus dui. Mauris tempor ligula sed lacus. Duis '
                                      'cursus enim ut augue. Cras ac magna. Cras nulla. Nulla egestas. Curabitur a '
                                      'leo. Quisque egestas wisi eget nunc. Nam feugiat lacus vel est. Curabitur '
                                      'consectetuer. \\br '
                                      'Suspendisse vel felis. Ut lorem lorem, interdum eu, '
                                      'tincidunt sit amet, laoreet vitae, arcu. Aenean faucibus pede eu ante. '
                                      'Praesent enim elit, rutrum at, molestie non, nonummy vel, nisl. Ut lectus '
                                      'eros, malesuada sit amet, fermentum eu, sodales cursus, magna. Donec eu purus. '
                                      'Quisque vehicula, urna sed ultricies auctor, pede lorem egestas dui, '
                                      'et convallis elit erat sed nulla. Donec luctus. Curabitur et nunc. Aliquam '
                                      'dolor odio, commodo pretium, ultricies non, pharetra in, velit. Integer arcu '
                                      'est, nonummy in, fermentum faucibus, egestas vel, odio.'})
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
        'source': forms.Textarea(attrs={'style': 'height: 25px', 'required': 'true'}),
        'image': forms.FileInput(attrs={'required': 'true'})
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
