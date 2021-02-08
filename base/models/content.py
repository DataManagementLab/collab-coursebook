"""Purpose of this file

This file describes or defines the basic structure of the course book.
A class that extends the models.Model class may represents a content
content of the course book and can be registered in admin.py.
"""

from django.conf import settings
from django.db import models
from django.db.models import Avg
from django.utils.translation import gettext_lazy as _

import reversion

from fontawesome_5.fields import IconField

from base.models import Profile
from .social import Rating


class Category(models.Model):
    """Category

    This model represents the category of a course book.

    :attr Category.title: Describes the title of the category
    :type Category.title: CharField
    :attr Category.DESC: The image file of the category
    :type Category.DESC: ImageField
    """
    title = models.CharField(max_length=150,
                             verbose_name=_("Title"))
    image = models.ImageField(verbose_name=_("Title Image"), blank=True,
                              upload_to='uploads/categories/')

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        :attr Meta.verbose_name: A human-readable name for the object in singular
        :type Meta.verbose_name: __proxy__
        :attr Meta.verbose_name_plural: A human-readable name for the object in plural
        :type Meta.verbose_name_plural: __proxy__
        :attr Meta.ordering: The default ordering for the object
        :type Meta.ordering: List[str]
        """
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ['title']

    def __str__(self):
        """String representation

        Returns the string representation of this object.

        :return: the string representation of this object
        :rtype: str
        """
        return self.title


class Period(models.Model):
    """Period

    This model represents the period of a course book.

    :attr Period.title: Describes the title of the period
    :type Period.title: CharField
    :attr Period.start: The starting date of the period
    :type Period.start: DateField
    :attr Period.end: The end date of the period
    :type Period.end: DateField
    """
    title = models.CharField(max_length=150,
                             verbose_name=_("Title"))
    start = models.DateField(verbose_name=_("start"))
    end = models.DateField(verbose_name=_("end"))

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        :attr Meta.verbose_name: A human-readable name for the object in singular
        :type Meta.verbose_name: __proxy__
        :attr Meta.verbose_name_plural: A human-readable name for the object in plural
        :type Meta.verbose_name_plural: __proxy__
        :attr Meta.ordering: The default ordering for the object
        :type Meta.ordering: List[str]
        """
        verbose_name = _("Period")
        verbose_name_plural = _("Periods")
        ordering = ['-end', '-start']

    def __str__(self):
        """String representation

        Returns the string representation of this object.

        :return: the string representation of this object
        :rtype: str
        """
        return self.title


class Course(models.Model):
    """Course

    This model represents the course of a course book.

    :attr Course.title: Describes the title of the course
    :type Course.title: CharField
    :attr Course.description: The description of the course
    :type Course.description: TextField
    :attr Course.creation_date: The creation date of the course
    :type Course.creation_date: DateTimeField
    :attr Course.image: The image of the course
    :type Course.image: ImageField
    :attr Course.topics: Describes the topic content in the course
    :type Course.topics: ManyToManyField - Topic
    :attr Course.owners: Describes the people that may change the structure of
    the course
    :type Course.owners: ManyToManyField - Profile
    :attr Course.restrict_changes: Describes the changes of the restriction who
    can edit it
    :type Course.restrict_changes: BooleanField
    :attr Course.category: Describes the category of the course
    :type Course.category: ForeignKey - Category
    :attr Course.period: Describes the period of the course
    :type Course.period: ForeignKey - Period
    """
    title = models.CharField(max_length=200,
                             verbose_name="Title",
                             unique=True)
    description = models.TextField(verbose_name=_("Description"))

    creation_date = models.DateTimeField(verbose_name=_('Creation Date'),
                                         auto_now_add=True,
                                         blank=True)

    image = models.ImageField(verbose_name=_("Title Image"),
                              blank=True,
                              upload_to='uploads/courses/%Y/%m/%d/')
    topics = models.ManyToManyField("Topic", verbose_name=_("Topics"),
                                    through='CourseStructureEntry',
                                    related_name="courses",
                                    blank=True)

    owners = models.ManyToManyField(Profile, related_name='owned_courses',
                                    verbose_name=_("Owners"))
    restrict_changes = models.BooleanField(verbose_name=_("Edit Restriction"),
                                           help_text=_("Is the course protected and "
                                                       "can only be edited by the owners?"),
                                           blank=True,
                                           default=False)

    category = models.ForeignKey(Category,
                                 verbose_name=_("Category"),
                                 related_name="courses",
                                 on_delete=models.CASCADE)
    period = models.ForeignKey(Period,
                               verbose_name=_("Period"),
                               related_name="courses",
                               blank=True,
                               null=True,
                               on_delete=models.SET_NULL)

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        :attr Meta.verbose_name: A human-readable name for the object in singular
        :type Meta.verbose_name: __proxy__
        :attr Meta.verbose_name_plural: A human-readable name for the object in plural
        :type Meta.verbose_name_plural: __proxy__
        :attr Meta.ordering: The default ordering for the object
        :type Meta.ordering: List[str]
        """
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")
        ordering = ['title']

    def __str__(self):
        """String representation

        Returns the string representation of this object.

        :return: the string representation of this object
        :rtype: str
        """
        return self.title


class Topic(models.Model):
    """Topic

    This model represents the tag to identify or specify a specific topic of a course book.

    :attr Topic.title: Describes the title of the course
    :type Topic.title: CharField
    :attr Topic.category: Describes in which category the topic belongs to
    :type Topic.category: ForeignKey - Category
    """
    title = models.CharField(verbose_name=_("Title"),
                             max_length=200)
    category = models.ForeignKey(Category,
                                 verbose_name=_("Category"),
                                 related_name="topics",
                                 on_delete=models.CASCADE)

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        :attr Meta.verbose_name: A human-readable name for the object in singular
        :type Meta.verbose_name: __proxy__
        :attr Meta.verbose_name_plural: A human-readable name for the object in plural
        :type Meta.verbose_name_plural: __proxy__
        """
        verbose_name = _("Topic")
        verbose_name_plural = _("Topics")

    def __str__(self):
        """String representation

        Returns the string representation of this object.

        :return: the string representation of this object
        :rtype: str
        """
        return f"{self.title} ({self.category})"

    def get_contents(self, sorted_by, filtered_by):
        """Get contents

        Returns all contents belonging to the topic.

        :param sorted_by: By what attribute the results should be sorted
        :type sorted_by: str
        :param filtered_by: By what style the results should be filtered
        :type filtered_by: str

        :return: the sorted and filtered contents
        :rtype: QuerySet
        """
        contents = self.contents.all()
        if filtered_by != 'None' and filtered_by is not None:
            if filtered_by == 'Text':
                contents = contents.filter(textfield__isnull=False)
            elif filtered_by == 'Latex':
                contents = contents.filter(latex__isnull=False)
            elif filtered_by == 'Image':
                contents = contents.filter(imagecontent__isnull=False)
            elif filtered_by == 'YouTube-Video':
                contents = contents.filter(ytvideocontent__isnull=False)
            elif filtered_by == 'PDF':
                contents = contents.filter(pdfcontent__isnull=False)
            else:
                contents = contents.filter()
        if sorted_by != 'None' and sorted_by is not None:
            if sorted_by == 'Rating':
                contents = sorted(contents, key=lambda x: x.get_rate(), reverse=True)
            elif sorted_by == 'Date':
                contents = contents.order_by('-' + 'creation_date')
            else:
                contents = contents.order_by('-' + sorted_by)
        return contents


class Tag(models.Model):
    """Topic

    This model represents the topic of a course book.

    :attr Tag.title: Describes the title of the course
    :type Tag.title: CharField
    :attr Tag.category: Describes in which category the topic belongs to
    :type Tag.category: IconField
    """
    title = models.CharField(verbose_name=_("Title"),
                             max_length=200)
    symbol = IconField(verbose_name=_("Symbol"),
                       help_text=_("Symbol to show with this tag (optional)"),
                       blank=True)

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        :attr Meta.verbose_name: A human-readable name for the object in singular
        :type Meta.verbose_name: __proxy__
        :attr Meta.verbose_name_plural: A human-readable name for the object in plural
        :type Meta.verbose_name_plural: __proxy__
        """
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __str__(self):
        """String representation

        Returns the string representation of this object.

        :return: the string representation of this object
        :rtype: str
        """
        return self.title


class Content(models.Model):
    """Content

    This model represents the content of a course book.

    :attr Content.topic: Describes the topics in the content
    :type Content.topic: ForeignKey - Topic
    :attr Content.author: The user that created the content
    :type Content.author: ForeignKey - Profile
    :attr Content.description: The description of the content
    :type Content.description: TextField
    :attr Content.type: Describes the type of the content
    :type Content.type: CharField
    :attr Content.language: Describes the language the content in which the content is
    written
    :type Content.language: CharField
    :attr Content.tags: Describes the tags of the content
    :type Content.tags: ManyToManyField - Tag
    :attr Content.readonly: Describes if the content is read only or it can be modified
    :type Content.readonly: BooleanField
    :attr Content.public BooleanField: Describes the content visibility
    :type Content.public: BooleanField
    :attr Content.attachment: Describes the attachment of the content
    :type Content.attachment: OneToOneField - ImageAttachment
    :attr Content.creation_date: Describes when the content was created
    :type Content.creation_date: DateTimeField
    :attr Content.preview: The preview image of the content
    :type Content.preview: ImageField
    :attr Content.ratings: Describes the ratings of the content
    :type Content.ratings: ManyToManyField - Profile
    """
    topic = models.ForeignKey(Topic, verbose_name=_("Topic"),
                              related_name='contents',
                              on_delete=models.CASCADE)
    author = models.ForeignKey("Profile", verbose_name=_("Author"),
                               on_delete=models.CASCADE,
                               related_name='contents')

    description = models.TextField(verbose_name=_("Description"),
                                   blank=True)

    type = models.CharField(verbose_name=_("Type"), max_length=30)

    language = models.CharField(verbose_name=_("Language"),
                                max_length=30,
                                choices=settings.LANGUAGES)
    tags = models.ManyToManyField(Tag,
                                  verbose_name=_("Tags"),
                                  related_name='contents',
                                  blank=True)

    readonly = models.BooleanField(verbose_name=_("Readonly"),
                                   help_text=_("Can this content be updated?"),
                                   default=False)
    public = models.BooleanField(verbose_name=_("Show in public courses?"),
                                 help_text=
                                 _("May this content be displayed in courses "
                                   "that don't require registration?"),
                                 default=False)

    attachment = models.OneToOneField('content.ImageAttachment',
                                      verbose_name=_("Attachment"),
                                      on_delete=models.CASCADE,
                                      blank=True,
                                      null=True)
    creation_date = models.DateTimeField(verbose_name=_('Creation Date'),
                                         auto_now_add=True,
                                         blank=True)
    preview = models.ImageField(verbose_name=_("Rendered preview"),
                                blank=True,
                                null=True)

    ratings = models.ManyToManyField("Profile",
                                     through='Rating')

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        :attr Meta.verbose_name: A human-readable name for the object in singular
        :type Meta.verbose_name: __proxy__
        :attr Meta.verbose_name_plural: A human-readable name for the object in plural
        :type Meta.verbose_name_plural: __proxy__
        """
        verbose_name = _("Content")
        verbose_name_plural = _("Contents")

    def __str__(self):
        """String representation

        Returns the string representation of this object.

        :return: the string representation of this object
        :rtype: str
        """
        return f"{self.type} for {self.topic} by {self.author}"

    def get_rate_num(self):
        """Ratings

        Returns the average number of ratings and -1 if there are no ratings present.

        :return: the average number of ratings
        :rtype: float
        """
        if self.get_rate() is None:
            return 0
        return self.get_rate()

    def get_rate(self):
        """Ratings

        Returns the average number of ratings and -1 if there are no ratings present.

        :return: the average number of ratings
        :rtype: float
        """
        rating = Rating.objects.filter(content_id=self.id).aggregate(Avg('rating'))['rating__avg']
        if rating is not None:
            return rating
        return -1

    def get_rate_count(self):
        """ Ratings count

        Returns the total count of ratings.

        :return: the total count of ratings
        :rtype: int
        """
        # pylint: disable=no-member
        return self.ratings.count()

    def user_already_rated(self, user):
        """Already rated

        Checks if an user already rated.

        :param user: The user to check
        :type user: User

        :return: true if an user already rated a content
        :rtype: bool
        """
        # pylint: disable=no-member
        return self.ratings.filter(user_id=user.pk).count() > 0

    def get_user_rate(self, user):
        """User rating

        Returns the rating of an user.

        :param user: The user to retrieve the rating
        :type user: User

        :return: the rating of an user
        :rtype: int
        """
        # pylint: disable=W0612
        if self.user_already_rated(user):
            content_id = self.id
            return self.ratings.get(user=user).rating_set.first().rating
        return 0

    def rate_content(self, user, rating):
        """Content rating

        Returns the rate content by the user.

        :param rating: The rating of content by the user
        :type rating: Rating
        :param user: The user of the rating
        :type user: User
        """
        Rating.objects.filter(user_id=user.user.id, content_id=self.id).delete()
        rating = Rating.objects.create(user=user, content=self, rating=rating)  # user = profile
        rating.save()
        # pylint: disable=no-member
        self.save()

    def get_index_in_course(self, course):
        """Index in the course structure

        Returns the index of the parent topic in the course structure.

        :param course: The course in which the topic should be searched
        :type course: Course

        :return: the index in the structure
        :rtype: str
        """
        return CourseStructureEntry.objects.get(course=course, topic=self.topic).index


class CourseStructureEntry(models.Model):
    """Course Structure Entry

    This model represents the structure of the courses.

    :attr CourseStructureEntry.course: The course whose structure is meant
    :type CourseStructureEntry.course: ForeignKey - Course
    :attr CourseStructureEntry.index: The position that is meant (e.g. "1#2" -> second under topic
    of the first topic)
    :type CourseStructureEntry.index: CharField
    :attr CourseStructureEntry.topic: The topic at the specified position/index
    :type CourseStructureEntry.topic: ForeignKey - Topic
    """
    course = models.ForeignKey(Course, verbose_name=_("Course"),
                               on_delete=models.CASCADE)
    index = models.CharField(verbose_name=_("Index"),
                             max_length=50)
    topic = models.ForeignKey(Topic, verbose_name=_("Topic"),
                              on_delete=models.DO_NOTHING)

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        :attr Meta.verbose_name: A human-readable name for the object in singular
        :type Meta.verbose_name: __proxy__
        :attr Meta.verbose_name_plural: A human-readable name for the object in plural
        :type Meta.verbose_name_plural: __proxy__
        """
        verbose_name = _("Course Structure Entry")
        verbose_name_plural = _("Course Structure Entries")

    def __str__(self):
        """String representation

        Returns the string representation of this object.

        :return: the string representation of this object
        :rtype: str
        """
        return f"{self.course} -> {self.index}. {self.topic}"


# Register models for reversion if it is not already done in admin, else we can specify configuration
reversion.register(Course,
                   fields=['title', 'description', 'image', 'topics',
                           'owners', 'restrict_changes', 'category', 'period'])

reversion.register(Content,
                   fields=['author', 'description', 'language',
                           'tags', 'readonly', 'public', 'attachment'])
