from django import forms
from content.models import YTVideoContent, ImageContent, PdfContent, ImageAttachment, TextField, Latex


class AddContentFormYoutubeVideo(forms.ModelForm):
    class Meta:
        model = YTVideoContent
        exclude = ['content']


class AddContentFormImage(forms.ModelForm):
    class Meta:
        model = ImageContent
        exclude = ['content']


class AddContentFormAttachedImage(forms.ModelForm):
    class Meta:
        model = ImageAttachment
        exclude = ['content']


class AddContentFormPdf(forms.ModelForm):
    class Meta:
        model = PdfContent
        exclude = ['license', 'content']


class AddTextField(forms.ModelForm):
    class Meta:
        model = TextField
        exclude = ['content']


class AddLatex(forms.ModelForm):
    class Meta:
        model = Latex
        exclude = ['content']


CONTENT_TYPE_FORMS = {
    YTVideoContent.TYPE: AddContentFormYoutubeVideo,
    ImageContent.TYPE: AddContentFormImage,
    PdfContent.TYPE: AddContentFormPdf,
    ImageAttachment.TYPE: AddContentFormAttachedImage,
    TextField.TYPE: AddTextField,
    Latex.TYPE: AddLatex
}
