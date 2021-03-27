from django.contrib.auth.models import User
from django.test import SimpleTestCase, Client
from django.urls import reverse, resolve
from django.test import RequestFactory, TestCase
from django_cas_ng.views import LoginView

from base.models import Course, Profile, Period, Category, Topic, Content, Comment, CourseStructureEntry

from frontend.views import DeleteComment, EditComment, StartView, CourseView, DashboardView, ProfileView, \
    ProfileEditView, CourseListView, CourseListForCategoryView, CourseListForPeriodView
from frontend.views.search import SearchView


class Test_comment_delete_classed_based_views(TestCase):

    def setUp(self):
        # create
        self.client = Client()
        self.staffuser = User.objects.create(username="testuser", password="testpassword",
                                             first_name="first", last_name="last", is_staff=True, is_superuser=False,
                                             is_active=True)
        self.profile = Profile.objects.get(user=self.staffuser)
        self.client.login(username=self.profile.user.username, password=self.profile.user.password)

        self.period = Period.objects.create(title="Period", start="2020-06-29", end="2020-07-29")
        self.category = Category.objects.create(title="Category")
        self.topic = Topic.objects.create(title="Title", category=self.category)
        self.content = Content.objects.create(topic=self.topic, author=self.profile,
                                              description="D", type="Dummy_Type", language="English")
        self.comment = Comment.objects.create(content=self.content, author=self.profile, text="Comment")
        self.course = Course.objects.create(title="Course", description="D", category=self.category, period=self.period)
        self.structure = CourseStructureEntry.objects.create(course=self.course, index="1", topic=self.topic)

        self.request_delete = RequestFactory().get(
            reverse("frontend:comment-delete", args=[self.course.id, self.topic.id, self.content.id, self.comment.id]))
        self.request_delete.user = self.profile.user  # for factory

        # self.request_edit = RequestFactory().get(reverse("frontend:comment-edit"))

    def test_delete_comment(self):
        view = DeleteComment()
        view.setup(self.request_delete)
        response = DashboardView.as_view()(self.request_delete)
        self.assertEquals(response.status_code, 200)
        # todo delete comment with and without permission


class Test_page_classed_based_views(TestCase):

    def setUp(self):
        # create
        self.client = Client()
        self.staffuser = User.objects.create(username="testuser", password="testpassword",
                                             first_name="first", last_name="last", is_staff=True,
                                             is_superuser=False)
        self.profile = Profile.objects.get(user=self.staffuser)  # wird automatisch angelegt
        self.client.login(username=self.profile.user.username, password=self.profile.user.password)

        self.period = Period.objects.create(title="Period", start="2020-06-29", end="2020-07-29")
        self.category = Category.objects.create(title="Category")
        self.topic = Topic.objects.create(title="Title", category=self.category)
        self.content = Content.objects.create(topic=self.topic, author=self.profile,
                                              description="D", type="Dummy_Type", language="English")
        self.comment = Comment.objects.create(content=self.content, author=self.profile, text="Comment")
        self.course = Course.objects.create(title="Course", description="D", category=self.category,
                                            period=self.period)
        self.structure = CourseStructureEntry.objects.create(course=self.course, index="1", topic=self.topic)

        self.request_index = RequestFactory().get(reverse("frontend:index"))
        self.request_index.user = self.staffuser  # for factory

        self.request_dashboard = RequestFactory().get(reverse("frontend:dashboard"))
        self.request_dashboard.user = self.staffuser  # for factory

    def test_index(self):
        view = LoginView()
        view.setup(self.request_index)
        response = DashboardView.as_view()(self.request_index)
        self.assertEquals(response.status_code, 200)

    def test_dashboard_view(self):
        view = DashboardView()
        view.setup(self.request_dashboard)
        response = DashboardView.as_view()(self.request_dashboard)
        self.assertEquals(response.status_code, 200)

        # check context
        context = view.get_context_data()
        self.assertIn('periods', context)
        self.assertIn('categories', context)
        self.assertIn('view', context)

        # check querysets
        self.assertEquals(context["categories"].get(title=self.category.title), self.category)
        self.assertEquals(len(context["categories"].values()), 1)

        self.assertEquals(context["periods"].get(title=self.period.title), self.period)
        self.assertEquals(len(context["periods"].values()), 1)


class Test_profile_classed_based_views(TestCase):

    def setUp(self):
        # create
        self.client = Client()
        self.staffuser = User.objects.create(username="testuser", password="testpassword",
                                             first_name="first", last_name="last", is_staff=True,
                                             is_superuser=False)
        self.profile = Profile.objects.get(user=self.staffuser)  # wird automatisch angelegt
        self.client.login(username=self.profile.user.username, password=self.profile.user.password)

        self.period = Period.objects.create(title="Period", start="2020-06-29", end="2020-07-29")
        self.category = Category.objects.create(title="Category")
        self.topic = Topic.objects.create(title="Title", category=self.category)
        self.content = Content.objects.create(topic=self.topic, author=self.profile,
                                              description="D", type="Dummy_Type", language="English")
        self.comment = Comment.objects.create(content=self.content, author=self.profile, text="Comment")
        self.course = Course.objects.create(title="Course", description="D", category=self.category,
                                            period=self.period)
        self.structure = CourseStructureEntry.objects.create(course=self.course, index="1", topic=self.topic)

        self.request_profile = RequestFactory().get(reverse("frontend:profile", args=[self.profile.user.id, ]))
        self.request_profile.user = self.staffuser  # for factory

        self.request_profile_edit = RequestFactory().get(reverse("frontend:profile-edit"))
        self.request_profile_edit.user = self.staffuser  # for factory

    def test_profile(self):
        view = ProfileEditView()
        view.setup(self.request_profile)
        self.assertTrue(view.get_queryset().filter(user=self.profile))

        response = ProfileView.as_view()(self.request_profile, pk=self.staffuser.pk)
        self.assertEquals(response.status_code, 200)
        # self.assertTemplateUsed(response,"frontend:profile")  # only useable on client() # todo should be tested?

    def test_profile_edit(self):
        view = ProfileEditView()
        view.setup(self.request_profile_edit)
        response = ProfileEditView.as_view()(self.request_profile_edit)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(view.get_success_url(), self.request_profile.path)
        self.assertEquals(view.get_object(), self.profile)
        # todo how to test form with view?


class Test_search_classed_based_views(TestCase):

    def setUp(self):
        # create
        self.client = Client()
        self.staffuser = User.objects.create(username="testuser", password="testpassword",
                                             first_name="first", last_name="last", is_staff=True,
                                             is_superuser=False)
        self.profile = Profile.objects.get(user=self.staffuser)  # wird automatisch angelegt
        self.client.login(username=self.profile.user.username, password=self.profile.user.password)

        self.period = Period.objects.create(title="Period", start="2020-06-29", end="2020-07-29")
        self.category = Category.objects.create(title="Category")
        self.topic = Topic.objects.create(title="Title", category=self.category)
        self.content = Content.objects.create(topic=self.topic, author=self.profile,
                                              description="D", type="Dummy_Type", language="English")
        self.comment = Comment.objects.create(content=self.content, author=self.profile, text="Comment")
        self.course = Course.objects.create(title="Course", description="D", category=self.category,
                                            period=self.period)
        self.structure = CourseStructureEntry.objects.create(course=self.course, index="1", topic=self.topic)

    def test_searchview_find_course_true(self):
        self.request_search = RequestFactory().get(reverse("frontend:search") + "?q=" + self.course.title)
        self.request_search.user = self.staffuser  # for factory

        view = SearchView()
        view.setup(self.request_search)
        self.assertTrue(view.get_queryset()["courses"].filter(title=self.course.title))

        view.object_list = []
        self.assertIn("search_query", view.get_context_data())

        response = SearchView.as_view()(self.request_search)
        self.assertEquals(response.status_code, 200)

    def test_searchview_find_course_false(self):
        self.request_search = RequestFactory().get(reverse("frontend:search") + "?q=***********")
        self.request_search.user = self.staffuser  # for factory

        view = SearchView()
        view.setup(self.request_search)
        self.assertFalse(view.get_queryset()["courses"].filter(title=self.course.title))

        response = SearchView.as_view()(self.request_search)
        self.assertEquals(response.status_code, 200)

    # todo test for all searching possibilities?


class Test_courses_classed_based_views(TestCase):

    def setUp(self):
        # create
        self.client = Client()
        self.staffuser = User.objects.create(username="testuser", password="testpassword",
                                             first_name="first", last_name="last", is_staff=True,
                                             is_superuser=False)
        self.profile = Profile.objects.get(user=self.staffuser)  # wird automatisch angelegt
        self.client.login(username=self.profile.user.username, password=self.profile.user.password)

        self.period = Period.objects.create(title="Period", start="2020-06-29", end="2020-07-29")
        self.period_fake = Period.objects.create(title="Period_fake", start="2020-06-29", end="2020-07-29")
        self.category = Category.objects.create(title="Category")
        self.category_fake = Category.objects.create(title="Category_Fake")

        self.topic = Topic.objects.create(title="Title", category=self.category)
        self.content = Content.objects.create(topic=self.topic, author=self.profile,
                                              description="D", type="Dummy_Type", language="English")
        self.comment = Comment.objects.create(content=self.content, author=self.profile, text="Comment")
        self.course = Course.objects.create(title="Course", description="D", category=self.category,
                                            period=self.period)
        for i in range(CourseListView.paginate_by):  # to have more than one site
            Course.objects.create(title="Course" + str(i), description="D", category=self.category,
                                  period=self.period)
        self.structure = CourseStructureEntry.objects.create(course=self.course, index="1", topic=self.topic)

        self.request_courses = RequestFactory().get(reverse("frontend:courses"))
        self.request_courses.user = self.staffuser  # for factory

        self.request_category_courses = RequestFactory().get(reverse("frontend:category-courses",
                                                                     args=[self.category.id, ]))
        self.request_category_courses.user = self.staffuser  # for factory

        self.request_period_courses = RequestFactory().get(
            reverse("frontend:period-courses", args=[self.period.id, ]))
        self.request_period_courses.user = self.staffuser  # for factory

    def test_CourseListView(self):
        view = CourseListView()
        view.setup(self.request_courses, **{'sort': 'title-z'})  # ** = kwargs var
        self.assertTrue(len(view.get_queryset()) == 10)
        view.object_list = []
        self.assertEquals(view.get_context_data()["sort"], "Z-A")
        self.assertGreater(view.get_queryset().first().title, "Course")  # sorting is django, so no need for testing

        response = CourseListView.as_view()(self.request_courses)
        self.assertEquals(response.status_code, 200)

    def test_CourseListForCategoryView(self):
        view = CourseListForCategoryView()
        view.setup(self.request_category_courses, **{'pk': self.category.id})  # ** = kwargs var
        view.object_list = []
        view.dispatch(self.request_category_courses)
        self.assertEquals(view.get_context_data()['category'], self.category)
        self.assertTrue(len(view.get_queryset()) == 10)

        response = CourseListForCategoryView.as_view()(self.request_category_courses, pk=self.category.id)
        self.assertEquals(response.status_code, 200)

    def test_CourseListForCategoryView_Fake_category(self):
        view = CourseListForCategoryView()
        view.setup(self.request_category_courses, **{'pk': self.category_fake.id})  # ** = kwargs var
        view.object_list = []
        view.dispatch(self.request_category_courses)
        self.assertEquals(view.get_context_data()['category'], self.category_fake)
        self.assertTrue(len(view.get_queryset()) == 0)

        response = CourseListForCategoryView.as_view()(self.request_category_courses, pk=self.category_fake.id)
        self.assertEquals(response.status_code, 200)

    def test_CourseListForPeriodView(self):
        view = CourseListForPeriodView()
        view.setup(self.request_period_courses, **{'pk': self.period.id})  # ** = kwargs var
        view.object_list = []
        view.dispatch(self.request_period_courses)
        self.assertEquals(view.get_context_data()['period'], self.period)
        self.assertTrue(len(view.get_queryset()) == 10)

        response = CourseListForPeriodView.as_view()(self.request_period_courses, pk=self.period.id)
        self.assertEquals(response.status_code, 200)

    def test_CourseListForPeriodView_fake_period(self):
        view = CourseListForPeriodView()
        view.setup(self.request_period_courses, **{'pk': self.period_fake.id})  # ** = kwargs var
        view.object_list = []
        view.dispatch(self.request_period_courses)
        self.assertEquals(view.get_context_data()['period'], self.period_fake)
        self.assertTrue(len(view.get_queryset()) == 0)

        response = CourseListForPeriodView.as_view()(self.request_period_courses, pk=self.period_fake.id)
        self.assertEquals(response.status_code, 200)


