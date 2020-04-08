from django.db import models
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ['title']

    title = models.CharField(max_length=150, verbose_name=_("Title"))
    image = models.ImageField(verbose_name=_("Title Image"), blank=True, upload_to='uploads/categories/')

    def __str__(self):
        return self.title


class Period(models.Model):
    class Meta:
        verbose_name = _("Period")
        verbose_name_plural = _("Periods")
        ordering = ['-end', '-start']

    title = models.CharField(max_length=150, verbose_name=_("Title"))
    start = models.DateField(verbose_name=_("start"))
    end = models.DateField(verbose_name=_("end"))

    def __str__(self):
        return self.title


class Course(models.Model):
    """
    Course Model
    title: name of the course
    creation_date: date and time of creation
    description: short description of the course
    owner: people that may change the structure of the course
    """
    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")
        ordering = ['title']

    title = models.CharField(max_length=200, verbose_name="Title")
    description = models.TextField(verbose_name=_("Description"))

    creation_date = models.DateTimeField(verbose_name=_('Creation Date'), auto_now_add=True, blank=True)

    image = models.ImageField(verbose_name=_("Title Image"), blank=True, upload_to='uploads/courses/%Y/%m/%d/')
    #topic_list = models.ManyToManyField(Topic, through='Structure')

    owners = models.ManyToManyField("Profile", related_name='owned_courses', verbose_name=_("Owners"))
    restrict_changes = models.BooleanField(verbose_name=_("Edit Restriction"),
        help_text=_("Is the course protected and can only be edited by the owners?"), blank=True, default=False)

    category = models.ForeignKey(Category, verbose_name=_("Category"), related_name="courses", on_delete=models.CASCADE)
    period = models.ForeignKey(Period, verbose_name=_("Period"), related_name="courses",
        blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title
