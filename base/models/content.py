from django.conf import settings
from django.db import models
from django.db.models import Avg
from django.utils.translation import gettext_lazy as _
from fontawesome_5.fields import IconField

from base.models import Profile
from .social import Rating


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

    title = models.CharField(max_length=200, verbose_name="Title", unique=True)
    description = models.TextField(verbose_name=_("Description"))

    creation_date = models.DateTimeField(verbose_name=_('Creation Date'), auto_now_add=True, blank=True)

    image = models.ImageField(verbose_name=_("Title Image"), blank=True, upload_to='uploads/courses/%Y/%m/%d/')
    topics = models.ManyToManyField("Topic", verbose_name=_("Topics"), through='CourseStructureEntry',
                                    related_name="courses", blank=True)

    owners = models.ManyToManyField(Profile, related_name='owned_courses', verbose_name=_("Owners"))
    restrict_changes = models.BooleanField(verbose_name=_("Edit Restriction"),
                                           help_text=_("Is the course protected and can only be edited by the owners?"),
                                           blank=True, default=False)

    category = models.ForeignKey(Category, verbose_name=_("Category"), related_name="courses", on_delete=models.CASCADE)
    period = models.ForeignKey(Period, verbose_name=_("Period"), related_name="courses",
                               blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title


class Topic(models.Model):
    """
    Topic Model

    title: Name of the topic
    category: category this topic belongs to
    """

    class Meta:
        verbose_name = _("Topic")
        verbose_name_plural = _("Topics")

    title = models.CharField(verbose_name=_("Title"), max_length=200)
    category = models.ForeignKey(Category, verbose_name=_("Category"), related_name="topics", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.category})"

    def get_contents(self, sorted_by, filtered_by):
        """
        It gets all contents belonging to the topic
        :param str sorted_by: by what attribute the results should be sorted
        :param str filtered_by: by what style the results should be filtered
        :return: the contents sorted and filtered
        :rtype: QuerySet
        """
        contents = self.contents.all()
        if filtered_by != 'None' and filtered_by is not None:
            contents = contents.filter(style=filtered_by)
        if sorted_by != 'None' and sorted_by is not None:
            if sorted_by == 'rating':
                contents = sorted(contents, key=lambda x: x.get_rate(), reverse=True)
            else:
                contents = contents.order_by('-' + sorted_by)
        return contents


class Tag(models.Model):
    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    title = models.CharField(verbose_name=_("Title"), max_length=200)
    symbol = IconField(verbose_name=_("Symbol"), help_text=_("Symbol to show with this tag (optional)"), blank=True)

    def __str__(self):
        return self.title


class Content(models.Model):
    """
    Content Model
    file: the File containing the content
    creation_date: date when topic was created
    language: Language the content is written in
    style. The style of the content (like key words, text, graphic, ...)
    author: user that created the content
    parent_topic: the topic the content belongs to/describes
    """

    class Meta:
        verbose_name = _("Content")
        verbose_name_plural = _("Contents")

    topic = models.ForeignKey(Topic, verbose_name=_("Topic"), related_name='contents', on_delete=models.CASCADE)
    author = models.ForeignKey("Profile", verbose_name=_("Author"), on_delete=models.CASCADE, related_name='contents')

    description = models.TextField(verbose_name=_("Description"), blank=True)

    type = models.CharField(verbose_name=_("Type"), max_length=30)

    language = models.CharField(verbose_name=_("Language"), max_length=30, choices=settings.LANGUAGES)
    tags = models.ManyToManyField(Tag, verbose_name=_("Tags"), related_name='contents', blank=True)

    readonly = models.BooleanField(verbose_name=_("Readonly"), help_text=_("Can this content be updated?"),
                                   default=False)
    public = models.BooleanField(verbose_name=_("Show in public courses?"), help_text=_(
        "May this content be displayed in courses that don't require registration?"), default=False)

    creation_date = models.DateTimeField(verbose_name=_('Creation Date'), auto_now_add=True, blank=True)
    preview = models.ImageField(verbose_name=_("Rendered preview"), blank=True, null=True)

    ratings = models.ManyToManyField("Profile", through='Rating')

    def __str__(self):
        return f"{self.type} for {self.topic} by {self.author}"

    def get_rate_num(self):
        """
        Returns the average number of ratings and 0 of no ratings occurred
        :return: average number of ratings
        :rtype: float
        """
        if self.get_rate() is None:
            return 0
        return self.get_rate()

    def get_rate(self):
        rating = Rating.objects.filter(content_id=self.id).aggregate(Avg('rating'))['rating__avg']
        if rating is not None:
            return rating
        return -1

    def get_rate_count(self):
        """
        get total count of ratings
        :return: count of ratings
        :rtype: int
        """
        return self.ratings.count()  # pylint: disable=no-member

    def user_already_rated(self, user):
        """
        check if an user already rated
        :param User user: user
        :return: true if an user already rated a content
        :rtype: bool
        """
        return self.ratings.filter(user_id=user.pk).count() > 0  # pylint: disable=no-member

    def get_user_rate(self, user):
        """
        get the rating of an user
        :param user user: user
        :return: rating of an user
        :rtype: int
        """
        if self.user_already_rated(user):
            content_id = self.id
            return self.ratings.get(user=user).rating_set.first().rating
        return 0

    def rate_content(self, user, rating):
        """
        Rate content
        :param rating: Rating of Content by User
        :param User user: user
        :return: nothing
        """
        Rating.objects.filter(user_id=user.user.id, content_id=self.id).delete()
        rating = Rating.objects.create(user=user, content=self, rating=rating)  # user = profile
        rating.save()
        # pylint: disable=no-member
        self.save()

    def get_index_in_course(self, course):
        """
        The index of the parent topic in the course structure
        :param Course course: the course in which the topic should be searched
        :return: the index in the structure
        :rtype: str
        """
        return CourseStructureEntry.objects.get(course=course, topic=self.topic).index


class CourseStructureEntry(models.Model):
    """
    Structure Model to save the structure of courses
    course: the course whose structure is meant
    index: position that is meant (e.g. "1#2" -> second under topic of the first topic)
    topic: topic at specified position/index
    """

    class Meta:
        verbose_name = _("Course Structure Entry")
        verbose_name_plural = _("Course Structure Entries")

    course = models.ForeignKey(Course, verbose_name=_("Course"), on_delete=models.CASCADE)
    index = models.CharField(verbose_name=_("Index"), max_length=50)
    topic = models.ForeignKey(Topic, verbose_name=_("Topic"), on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.course} -> {self.index}. {self.topic}"
