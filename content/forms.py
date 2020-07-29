from django import forms
from content.models import YTVideoContent, ImageContent, PdfContent


class AddContentFormYoutubeVideo(forms.ModelForm):
    class Meta:
        model = YTVideoContent
        exclude = ['content']


class AddContentFormImage(forms.ModelForm):
    class Meta:
        model = ImageContent
        exclude = ['content']


class AddContentFormPdf(forms.ModelForm):
    class Meta:
        model = PdfContent
        exclude = ['content']


CONTENT_TYPE_FORMS = {
    YTVideoContent.TYPE: AddContentFormYoutubeVideo,
    ImageContent.TYPE: AddContentFormImage,
    PdfContent.TYPE: AddContentFormPdf
}
