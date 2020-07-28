from django.db import models
from django.utils.translation import gettext_lazy as _

from base.models import Content
from export.mixins import ExportCoursebookMixin


class YTVideoContent(models.Model, ExportCoursebookMixin):
    TYPE = "YouTubeVideo"
    DESC = _("YouTube Video")

    class Meta:
        verbose_name = _("YouTube Video Content")
        verbose_name_plural = _("YouTube Video Contents")

    content = models.OneToOneField(Content, verbose_name=_("Content"), on_delete=models.CASCADE, primary_key=True)
    url = models.URLField(verbose_name=_("Video URL"))

    @property
    def id(self):
        return self.url.split("=")[1]

    def __str__(self):
        return f"{self.DESC}: {self.url}"

    def generate_latex_template(self):
        return r"""
        \href{""" + str(self.url) + """}{""" + str(self.url) + """}
        \\newline
        """


class ImageContent(models.Model, ExportCoursebookMixin):
    TYPE = "Image"
    DESC = _("Single Image")

    class Meta:
        verbose_name = _("Image Content")
        verbose_name_plural = _("Image Contents")

    content = models.OneToOneField(Content, verbose_name=_("Content"), on_delete=models.CASCADE, primary_key=True)
    image = models.ImageField(verbose_name=_("Image"), upload_to='uploads/contents/%Y/%m/%d/')
    source = models.TextField(verbose_name=_("Source"))
    license = models.CharField(verbose_name=_("License"), blank=True, max_length=200)

    def __str__(self):
        return f"{self.content}: {self.image}"

    def generate_latex_template(self):
        return r"""
        \begin{figure}[H]
        \centering
        \includegraphics[width=\textwidth]{""" + str(self.image.path) + r"""}
        \caption{""" + str(self.content.description) + r"""}
        \end{figure}
        """


CONTENT_TYPES = {
    YTVideoContent.TYPE: YTVideoContent,
    ImageContent.TYPE: ImageContent,
}
