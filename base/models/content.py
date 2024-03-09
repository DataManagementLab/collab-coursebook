"""Purpose of this file

This file describes or defines the basic structure of the course book.
A class that extends the models.Model class may represents a content
content of the course book and can be registered in admin.py.
"""

from django.conf import settings
from django.db import models
from django.db.models import Avg, Count
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

import reversion

from fontawesome_6.fields import IconField

from base.models import Profile

from .social import Rating


class Category(models.Model):
    """Category

    This model represents the category of a course book. A category contains a title and
    optional an image.

    :attr Category.title: The title of the category
    :type Category.title: CharField
    :attr Category.DESC: The image of the category
    :type Category.DESC: ImageField
    """
    title = models.CharField(max_length=150,
                             verbose_name=_("Title"))
    image = models.ImageField(verbose_name=_("Title Image"),
                              blank=True,
                              upload_to='uploads/categories/')

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        :attr Meta.verbose_name: A human-readable name for the object in singular
        :type Meta.verbose_name: __proxy__
        :attr Meta.verbose_name_plural: A human-readable name for the object in plural
        :type Meta.verbose_name_plural: __proxy__
        :attr Meta.ordering: The default ordering for the object
        :type Meta.ordering: list[str]
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

    This model represents the period of a course book. A period contains a title
    and two dates which indicates its start and end point.

    :attr Period.title: The title of the period
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
        :type Meta.ordering: list[str]
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

    This model represents the course of a course book. A course contains a unique title with a
    description, the owners of the course  and an image representing the course. Furthermore
    the creation date and the permission who can change the content of the course will be
    stored.

    A course can contain categories and is assigned by topics. Besides, a period of the course
    can also be defined.

    :attr Course.title: The title of the course
    :type Course.title: CharField
    :attr Course.description: The description of the course
    :type Course.description: TextField
    :attr Course.creation_date: The creation date of the course
    :type Course.creation_date: DateTimeField
    :attr Course.image: The image of the course
    :type Course.image: ImageField
    :attr Course.topics: The topics that the course contains
    :type Course.topics: ManyToManyField - Topic
    :attr Course.owners: The owners of the course which can change the content of the course
    :type Course.owners: ManyToManyField - Profile
    :attr Course.moderators: The moderators of the course which can approve the content of the course
    :type Course.moderators: ManyToManyField - Profile
    :attr Course.restrict_changes: The restriction who can edit the course
    :type Course.restrict_changes: BooleanField
    :attr Content.public: The status of the course if it is public
    :type Content.public: BooleanField
    :attr Course.category: The category of the course
    :type Course.category: ForeignKey - Category
    :attr Course.period: The period of the course
    :type Course.period: ForeignKey - Period
    """
    title = models.CharField(max_length=200,
                             verbose_name=_("Title"),
                             unique=True
                             )
    description = models.TextField(verbose_name=_("Description"))

    creation_date = models.DateTimeField(verbose_name=_('Creation Date'),
                                         default=timezone.now,
                                         blank=True)

    image = models.ImageField(verbose_name=_("Title Image"),
                              blank=True,
                              upload_to='uploads/courses/%Y/%m/%d/')
    topics = models.ManyToManyField("Topic", verbose_name=_("Topics"),
                                    through='CourseStructureEntry',
                                    related_name="courses",
                                    blank=True)

    owners = models.ManyToManyField(Profile,
                                    related_name='owned_courses',
                                    verbose_name=_("Owners"))
    moderators = models.ManyToManyField(Profile,
                                        related_name='moderated_courses',
                                        verbose_name=_("Moderators"),
                                        default=None,
                                        blank=True)
    restrict_changes = models.BooleanField(verbose_name=_("Edit Restriction"),
                                           help_text=_("This course is restricted and "
                                                       "can only be edited by the owners"),
                                           blank=True,
                                           default=False)
    public = models.BooleanField(verbose_name=_("Publicly accessible"),
                                 help_text=_(
                                     "This course can be accessed by unregistered users "),
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
        :type Meta.ordering: list[str]
        """
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")
        ordering = ['title']

    def get_sorted_topic_list(self):
        """Sorted topic list

        Returns a sorted topic query. The order after this call
        is that its sorted by the index of the sub topics.

        :return: the sorted topic list
        :rtype: QuerySet
        """
        return self.topics.order_by('child_topic__index')

    def __str__(self):
        """String representation

        Returns the string representation of this object.

        :return: the string representation of this object
        :rtype: str
        """
        return self.title


class Topic(models.Model):
    """Topic

    This model represents the topic. A topic contains a title and its related category.

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

    def get_contents(self, sorted_by, filtered_by, user=None):
        """Get contents

        Returns all contents belonging to this topic. Additionally the contents
        can be sorted or filtered.

        :param sorted_by: The sorting value which the content should be sorted
        :type sorted_by: str
        :param filtered_by: The filtered value which the content should be filtered
        :type filtered_by: str

        :return: the sorted and filtered contents belonging to this topic
        :rtype: QuerySet[Content]
        """
        # If the user is a moderator, user is set to "" to show all contents
        if user == "":
            contents = self.contents.all()

        # If the user is not a moderator and not logged in, only show unhidden contents
        elif user == None:
            contents = self.contents.all().filter(hidden=False)

        else:
            # filter the contents that are not hidden as well as hidden and authored by the user
            contents = self.contents.all().filter(
                models.Q(hidden=False) | models.Q(author=user))

        # filtered by is a String and represents the decision of the user
        # , how they want to filter the data,
        # e.g. 'Text' means they want to only see all text fields in the topic
        from content.models import CONTENT_TYPES

        if filtered_by is not None and filtered_by != 'None' and filtered_by in CONTENT_TYPES:
            contents = CONTENT_TYPES[filtered_by].filter_by_own_type(contents)

        # the topic can be sorted (even as an addition to filter)
        # the user decides, if they want to sort by rating or by date
        # and the String represent their decision
        if sorted_by != 'None' and sorted_by is not None:
            if sorted_by == 'Rating':
                contents = sorted(
                    contents, key=lambda x: x.get_rate(), reverse=True)
            elif sorted_by == 'Date':
                contents = contents.order_by('-' + 'creation_date')
            else:
                contents = contents.order_by('-' + sorted_by)
        return contents


class Tag(models.Model):
    """Tag

    This model represents the tag to identify or specify a specific topic of a course book.
    A tag contains an title and an optional symbol representing the tag.

    :attr Tag.title: The title of the tag
    :type Tag.title: CharField
    :attr Tag.symbol: The symbol of the tag
    :type Tag.symbol: IconField
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

    This model represents the content of a course book. A content contains topics to which
    it can be assigned. There can be different types of content, which differ from the
    concrete content and presentation. There is an optional description of the content,
    the language in which the content was written and, of course, authors who wrote the content.
    Additionally, tags, markings, whether the document is read-only and whether it is public,
    the creation date, user ratings and a preview of the course are stored.

    :attr Content.topic: The topics of the content
    :type Content.topic: ForeignKey - Topic
    :attr Content.author: The authors of the content
    :type Content.author: ForeignKey - Profile
    :attr Content.description: The description of the content
    :type Content.description: TextField
    :attr Content.type: The content type of the content
    :type Content.type: CharField
    :attr Content.language: The language of the content
    :type Content.language: CharField
    :attr Content.tags: The tags of the content
    :type Content.tags: ManyToManyField - Tag
    :attr Content.readonly: The status of the content if it is read only
    :type Content.readonly: BooleanField
    :attr Content.public: The status of the content if it is public
    :type Content.public: BooleanField
    :attr Content.public: The status of the content if it is approved
    :type Content.public: BooleanField
    :attr Content.approved: The status of the content if it is hidden
    :type Content.approved: BooleanField
    :attr Content.author_message: The message for the author
    :type Content.author_message: TextField
    :attr Content.user_message: The message for the user
    :type Content.user_message: TextField
    :attr Content.creation_date: The creation date of the content
    :type Content.creation_date: DateTimeField
    :attr Content.preview: The preview image of the content
    :type Content.preview: ImageField
    :attr Content.ratings: The ratings from the user to the content
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

    readonly = models.BooleanField(verbose_name=_("Set to Read-Only"),
                                   help_text=_(
                                       "This content shouldn't be edited"),
                                   default=False)
    public = models.BooleanField(verbose_name=_("Show in public courses"),
                                 help_text=_("This content will be displayed in courses "
                                             "that don't require registration"),
                                 default=False)
    approved = models.BooleanField(verbose_name=_("Approved"),
                                   help_text=_(
                                       "This content is approved by a moderator"),
                                   default=False)
    hidden = models.BooleanField(verbose_name=_("Hidden"),
                                 help_text=_(
                                     "This content is hidden in the course by a moderator"),
                                 default=False)
    author_message = models.TextField(verbose_name=_("Author Message"),
                                      help_text=_(
                                          "The message for the author"),
                                      blank=True,
                                      null=True)
    user_message = models.TextField(verbose_name=_("User Message"),
                                    help_text=_("The message for the user"),
                                    blank=True,
                                    null=True)
    creation_date = models.DateTimeField(verbose_name=_('Creation Date'),
                                         default=timezone.now,
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

    # def __str__(self):
    #     """String representation

    #     Returns the string representation of this object.

    #     :return: the string representation of this object
    #     :rtype: str
    #     """
    #     return _('%(title)s for %(topic)s by %(author)s') % {'title': self.type,
    #                                                          'topic': self.topic,
    #                                                          'author': self.author}

    def get_rate_num(self):
        """Average rating

        Returns the average number of ratings and -1 if there are no ratings present.

        :return: the average number of ratings
        :rtype: float
        """
        if self.get_rate() == -1:
            return 0
        return self.get_rate()

    def get_rate_amount(self):
        """Total number of ratings

        Returns the amount number of ratings to this content and 0 if there are no ratings present.

        :return: the amount of ratings
        :rtype: int

        """
        return Rating.objects.filter(content_id=self.id).aggregate(Count('rating'))['rating__count']

    def get_rate(self):
        """Average rating

        Returns the average number of ratings and -1 if there are no ratings present.

        :return: the average number of ratings
        :rtype: float
        """
        rating = Rating.objects.filter(content_id=self.id).aggregate(
            Avg('rating'))['rating__avg']
        if rating is not None:
            return int(rating)
        return -1

    def get_rate_count(self):
        """ Ratings count

        Returns the total count of ratings.

        :return: the total count of ratings
        :rtype: int
        """
        return self.ratings.count()

    def user_already_rated(self, user):
        """Already rated

        Checks if an user already rated.

        :param user: The user to check
        :type user: User

        :return: true if an user already rated a content
        :rtype: bool
        """
        return self.ratings.filter(user_id=user.pk).count() > 0

    def get_user_rate(self, user):
        """User rating

        Returns the rating of an user. If the user has not yet submitted a rating, then
        the returned rating will be 0.

        :param user: The user to retrieve the rating
        :type user: User

        :return: the rating of an user
        :rtype: int
        """
        if self.user_already_rated(user):
            return Rating.objects.filter(content_id=self.id).filter(user_id=user.pk).first().rating
        return 0

    def rate_content(self, user, rating):
        """Content rating

        Rates the content by the given rating of the user.

        :param rating: The rating of content by the user
        :type rating: Rating
        :param user: The user of the rating
        :type user: User
        """
        Rating.objects.filter(user_id=user.user.id,
                              content_id=self.id).delete()
        rating = Rating.objects.create(
            user=user, content=self, rating=rating)  # user = profile
        rating.save()
        self.save()

    def approve_content(self, course, user, approval):
        """Content approval

        Sets the approval of the content by the given approval of the user.

        :param approval: The approval of content by the user
        :type approval: bool
        :param user: The user of the approval
        :type user: User
        """
        if user in course.moderators.all():
            self.approved = approval
            self.author_message = None
            self.user_message = None
            self.save()

    def hide_content(self, course, user, hide, author_message=None, user_message=None):
        """Content hiding

        Sets the hiding of the content by the given hide of the user.

        :param hide: The hide of content by the user
        :type hide: bool
        :param user: The user of the hide
        :type user: User
        """
        if user in course.moderators.all():
            self.hidden = hide
            self.author_message = author_message
            self.user_message = user_message
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

    This model represents the structure of the courses. The course structure consists
    of main topics and each main topics can contain sub topics. The main topics and sub topics
    are differentiated through its index. Sub topics contains the index of the main topic and
    its own index position in the main topic

    For example:

    - 1 is a main topic
    - 1/2 is a second sub topic in the main topic 1

    :attr CourseStructureEntry.course: The course whose structure is meant
    :type CourseStructureEntry.course: ForeignKey - Course
    :attr CourseStructureEntry.index: The position of the (sub) topic
    :type CourseStructureEntry.index: CharField
    :attr CourseStructureEntry.topic: The topic at the specified position/index
    :type CourseStructureEntry.topic: ForeignKey - Topic
    """
    course = models.ForeignKey(Course, verbose_name=_("Course"),
                               on_delete=models.CASCADE)
    index = models.CharField(verbose_name=_("Index"),
                             max_length=50)
    topic = models.ForeignKey(Topic, related_name='child_topic',
                              verbose_name=_("Topic"),
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


# Register models for reversion if it is not already done in admin,
# else we can specify configuration
reversion.register(Course,
                   fields=['title', 'description', 'image', 'topics',
                           'restrict_changes'])

reversion.register(Content,
                   fields=['description', 'language', 'approved',
                           'tags', 'readonly', 'public'],
                   follow=['ImageAttachments'])
