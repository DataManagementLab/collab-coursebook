"""Purpose of this file

This file describes or defines the basic structure of the course book.
A class that extends the models.Model class may represents a content
content of the course book and can be registered in admin.py.
"""

from django.conf import settings
from django.db import models
from django.db.models import Avg
from django.utils.translation import gettext_lazy as _
from fontawesome_5.fields import IconField

from base.models import Profile
from .social import Rating


class Category(models.Model):
    """Category

    This model represents the category of a course book.

    Attributes:
        Category.title (CharField): Describes the title of the category
        Category.DESC (ImageField): The image file of the category
    """
    title = models.CharField(max_length=150,
                             verbose_name=_("Title"))
    image = models.ImageField(verbose_name=_("Title Image"), blank=True,
                              upload_to='uploads/categories/')

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        Attributes:
            Meta.verbose_name (__proxy__): A human-readable name for the object in singular
            Meta.verbose_name_plural (__proxy__): A human-readable name for the object in plural
            Meta.ordering (List[str]): The default ordering for the object
        """
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ['title']

    def __str__(self):
        """String representation

        return: the string representation of this object.
        rtype: str
        """
        return self.title


class Period(models.Model):
    """Period

    This model represents the period of a course book.

    Attributes:
        Period.title (CharField): Describes the title of the period
        Period.start (DateField): The starting date of the period
        Period.end (DateField): The end date of the period
    """
    title = models.CharField(max_length=150,
                             verbose_name=_("Title"))
    start = models.DateField(verbose_name=_("start"))
    end = models.DateField(verbose_name=_("end"))

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        Attributes:
            Meta.verbose_name (__proxy__): A human-readable name for the object in singular
            Meta.verbose_name_plural (__proxy__): A human-readable name for the object in plural
            Meta.ordering (List[str]): The default ordering for the object
        """
        verbose_name = _("Period")
        verbose_name_plural = _("Periods")
        ordering = ['-end', '-start']

    def __str__(self):
        """String representation

        return: the string representation of this object.
        rtype: str
        """
        return self.title


class Course(models.Model):
    """Course

    This model represents the course of a course book.

    Attributes:
        Course.title (CharField): Describes the title of the course
        Course.description (TextField): The description of the course
        Course.creation_date (DateTimeField): The creation date of the course
        Course.image (ImageField): The image of the course
        Course.topics (ManyToManyField - Topic): Describes the topic content in the course
        Course.owners (ManyToManyField): Describes the people that may change the structure of
        the course
        Course.restrict_changes (ManyToManyField): Describes the changes of the restriction who
        can edit it
        Course.category (ForeignKey - Category): Describes the category of the course
        Course.period (ForeignKey - Period): Describes the period of the course
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

        Attributes:
            Meta.verbose_name (__proxy__): A human-readable name for the object in singular
            Meta.verbose_name_plural (__proxy__): A human-readable name for the object in plural
            Meta.ordering (List[str]): The default ordering for the object
        """
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")
        ordering = ['title']

    def __str__(self):
        """String representation

        return: the string representation of this object.
        rtype: str
        """
        return self.title


class Topic(models.Model):
    """Topic

    This model represents the tag to identify or specify a specific topic of a course book.

    Attributes:
        Topic.title (CharField): Describes the title of the course
        Topic.category (ForeignKey - Category): Describes in which category the topic belongs to
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

        Attributes:
            Meta.verbose_name (__proxy__): A human-readable name for the object in singular
            Meta.verbose_name_plural (__proxy__): A human-readable name for the object in plural
        """
        verbose_name = _("Topic")
        verbose_name_plural = _("Topics")

    def __str__(self):
        """String representation

        return: the string representation of this object.
        rtype: str
        """
        return f"{self.title} ({self.category})"

    def get_contents(self, sorted_by, filtered_by):
        """Get contents

        Returns all contents belonging to the topic.

        Parameters:
            sorted_by (str): By what attribute the results should be sorted
            filtered_by (str): By what style the results should be filtered

        return: the sorted and filtered contents
        rtype: QuerySet
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
    """Topic

    This model represents the topic of a course book.

    Attributes:
        Tag.title (CharField): Describes the title of the course
        Tag.category (IconField): Describes in which category the topic belongs to
    """
    title = models.CharField(verbose_name=_("Title"),
                             max_length=200)
    symbol = IconField(verbose_name=_("Symbol"),
                       help_text=_("Symbol to show with this tag (optional)"),
                       blank=True)

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        Attributes:
            Meta.verbose_name (__proxy__): A human-readable name for the object in singular
            Meta.verbose_name_plural (__proxy__): A human-readable name for the object in plural
        """
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __str__(self):
        """String representation

        return: the string representation of this object.
        rtype: str
        """
        return self.title


class Content(models.Model):
    """Content

    This model represents the content of a course book.

    Attributes:
        Content.topic (ForeignKey - Topic): Describes the topics in the content
        Content.author (ForeignKey - Profile): The user that created the content
        Content.description (TextField): The description of the content
        Content.type (CharField): Describes the type of the content
        Content.language (CharField): Describes the language the content in which the content is
        written
        Content.tags (ManyToManyField - Tag): Describes the tags of the content
        Content.readonly (BooleanField):
            Describes if the content is read only or it can be modified
        Content.public (BooleanField): Describes the content visibility
        Content.attachment (OneToOneField - ImageAttachment):
            Describes the attachment of the content
        Content.creation_date (DateTimeField): Describes when the content was created
        Content.preview (ImageField): The preview image of the content
        Content.ratings (ManyToManyField - Profile): Describes the ratings of the content
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

        Attributes:
            Meta.verbose_name (__proxy__): A human-readable name for the object in singular
            Meta.verbose_name_plural (__proxy__): A human-readable name for the object in plural
        """
        verbose_name = _("Content")
        verbose_name_plural = _("Contents")

    def __str__(self):
        """String representation

        return: the string representation of this object.
        rtype: str
        """
        return f"{self.type} for {self.topic} by {self.author}"

    def get_rate_num(self):
        """Ratings

        Returns the average number of ratings and 0 if there are no ratings presents.

        return: the average number of ratings
        rtype: float
        """
        if self.get_rate() is None:  # TODO How can it returns none?
            return 0
        return self.get_rate()

    def get_rate(self):
        """Ratings

        Returns the average number of ratings and -1 if there are no ratings presents.

        return: the average number of ratings
        rtype: float
        """
        rating = Rating.objects.filter(content_id=self.id).aggregate(Avg('rating'))['rating__avg']
        if rating is not None:
            return rating
        return -1

    def get_rate_count(self):
        """ Ratings count

        Returns the total count of ratings.

        return: the total count of ratings
        rtype: int
        """
        return self.ratings.count()  # pylint: disable=no-member

    def user_already_rated(self, user):
        """Already rated

        Checks if an user already rated.

        Parameters:
            user (User): The user to check

        return: true if an user already rated a content
        rtype: bool
        """
        return self.ratings.filter(user_id=user.pk).count() > 0  # pylint: disable=no-member

    def get_user_rate(self, user):
        """User rating

        Returns the rating of an user.

        Parameters:
            user (User): The user to retrieve the rating

        return: rating of an user
        rtype: int
        """
        if self.user_already_rated(user):
            content_id = self.id
            return self.ratings.get(user=user).rating_set.first().rating
        return 0

    def rate_content(self, user, rating):
        """Content rating

        Returns the rate content by the user.

        Parameters:
            rating (Rating): The rating of content by the user
            user (User) The user of the rating
        """
        Rating.objects.filter(user_id=user.user.id, content_id=self.id).delete()
        rating = Rating.objects.create(user=user, content=self, rating=rating)  # user = profile
        rating.save()
        # pylint: disable=no-member
        self.save()

    def get_index_in_course(self, course):
        """Index in the course structure

        Returns the index of the parent topic in the course structure.

        Parameters:
            course (Course): The course in which the topic should be searched

        return: the index in the structure
        rtype: str
        """
        return CourseStructureEntry.objects.get(course=course, topic=self.topic).index


class CourseStructureEntry(models.Model):
    """Course Structure Entry

    This model represents the structure of the courses.

    Attributes:
        CourseStructureEntry.course (ForeignKey - Course): The course whose structure is meant
        CourseStructureEntry.index (CharField): The position that is meant
        (e.g. "1#2" -> second under topic of the first topic)
        CourseStructureEntry.topic (ForeignKey - Topic): The topic at the specified position/index
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

        Attributes:
            Meta.verbose_name (__proxy__): A human-readable name for the object in singular
            Meta.verbose_name_plural (__proxy__): A human-readable name for the object in plural
        """
        verbose_name = _("Course Structure Entry")
        verbose_name_plural = _("Course Structure Entries")

    def __str__(self):
        """String representation

        return: the string representation of this object.
        rtype: str
        """
        return f"{self.course} -> {self.index}. {self.topic}"
