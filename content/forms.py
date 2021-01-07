from django import forms

from content.models import YTVideoContent, ImageContent, PdfContent, ImageAttachment, TextField, Latex, SingleImage


class AddContentFormYoutubeVideo(forms.ModelForm):
    class Meta:
        model = YTVideoContent
        exclude = ['content']


class AddContentFormImage(forms.ModelForm):
    class Meta:
        model = ImageContent
        exclude = ['content']
        widgets = {
            'source': forms.Textarea(attrs={'style': 'height: 100px'}),
        }


class AddContentFormAttachedImage(forms.ModelForm):
    class Meta:
        model = ImageAttachment
        exclude = ['images', 'content']
        widgets = {
            'source': forms.Textarea(attrs={'style': 'height: 50px'}),
        }


class AddContentFormPdf(forms.ModelForm):
    class Meta:
        model = PdfContent
        exclude = ['license', 'content']
        widgets = {
            'source': forms.Textarea(attrs={'style': 'height: 100px'}),
        }


class AddTextField(forms.ModelForm):
    class Meta:
        model = TextField
        exclude = ['content']
        widgets = {
            'source': forms.Textarea(attrs={'style': 'height: 100px'}),
        }


class AddLatex(forms.ModelForm):
    class Meta:
        model = Latex
        exclude = ['content', 'pdf']
        widgets = {
            'source': forms.Textarea(attrs={'style': 'height: 100px'}),
        }

class AddSingleImage(forms.ModelForm):
    class Meta:
        model = SingleImage
        exclude = []


CONTENT_TYPE_FORMS = {
    YTVideoContent.TYPE: AddContentFormYoutubeVideo,
    ImageContent.TYPE: AddContentFormImage,
    PdfContent.TYPE: AddContentFormPdf,
    ImageAttachment.TYPE: AddContentFormAttachedImage,
    TextField.TYPE: AddTextField,
    Latex.TYPE: AddLatex,
    SingleImage.TYPE: AddSingleImage
}
