import json

from django.contrib.auth.models import User
from django.urls import reverse

from base.models import Course, Category, CourseStructureEntry, Topic
from frontend.forms.course import CreateTopicForm
from test.test_cases import MediaTestCase

# TODO test review
class BaseCourseViewTestCase(MediaTestCase):
    """ Base test cases for CourseView and EditCourseStructureView

    Defines the test cases for view  CourseView and EditCourseStructureView
    """

    def setUp(self):
        """Setup

        Sets up the test database.
        """
        super().setUp()

        self.user = User.objects.get(pk=1)

        self.cat = Category.objects.create(title="Category~*")
        self.course1 = Course.objects.create(title='Course Test', description='desc', category=self.cat)
        self.course1.owners.add(self.user.profile)
        self.topic1 = Topic.objects.create(title="Topic1", category=self.cat)
        self.topic2 = Topic.objects.create(title="Topic2", category=self.cat)
        self.topic3 = Topic.objects.create(title="Topic3", category=self.cat)

        course_struc_entry_1 = CourseStructureEntry(course=self.course1, index=1, topic=self.topic1)
        course_struc_entry_2 = CourseStructureEntry(course=self.course1, index=2, topic=self.topic2)
        course_struc_entry_3 = CourseStructureEntry(course=self.course1, index="2/1", topic=self.topic3)
        course_struc_entry_1.save(), course_struc_entry_2.save(), course_struc_entry_3.save()

        self.json_data = [{'value': 'Topic1 (Category~*)', 'id': 2},
                          {'value': 'Topic2 (Category~*)', 'id': 3,
                           'children': [{'value': 'Topic3 (Category~*)', 'id': 4}]}]


class CourseViewTestCase(BaseCourseViewTestCase):
    """ test cases for CourseView

    Defines the test cases for view  CourseView
    """

    # TODO test review views\course.py

    def test_ajax_and_check_course_view(self):
        """CourseView post test case - request is ajax and check is True

        Tests CourseView post if request is ajax and check is True.
        """
        path = reverse('frontend:course', kwargs={
            'pk': self.course1.pk})

        topic_list = [
            {"value": "Topic1 (Category~*)", "id": 2},
            {"value": "Topic2 (Category~*)", "id": 3},
            {"value": "Topic3 (Category~*)", "id": 4}
        ]
        data = {
            'topic_list': json.dumps(topic_list)
        }
        # before the post check the structure
        # self.assertEqual(JsonHandler.topics_structure_to_json(self.course1), self.json_data)
        response = self.client.post(path, data,
                                    **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.status_code, 200)
        # after post the structure of topics should also be accordingly changed
        self.assertEqual(list(CourseStructureEntry.objects.all().values_list("index", flat=True)),
                         ['1', '2', '3'])
        self.assertEqual(list(CourseStructureEntry.objects.all().values_list("topic_id", flat=True)),
                         [2, 3, 4])
        self.assertIsNotNone(CourseStructureEntry.objects.get(index='3', topic=self.topic3))

    def test_bad_response_course_view(self):
        """CourseView post test case - request is ajax and check is false.

        Tests CourseView post if request is ajax and check is false.
        """
        path = reverse('frontend:course', kwargs={
            'pk': self.course1.pk})

        topic_list = [
            {"value": "Topic1 (Category~*)", "id": 2},
            {"value": "Topic2 (Category~*)", "id": 3},
            {"value": "Topic3 (Category~*)", "id": 9}
        ]
        data = {
            'topic_list': json.dumps(topic_list)
        }
        response = self.client.post(path, data,
                                    **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        # it should be a bad response
        self.assertEqual(response.status_code, 400)

    def test_invalid_form_not_ajax_course_view(self):
        """CourseView post test case - form is invalid and request not ajax

        Tests CourseView post if form is invalid and request not ajax.
        """
        path = reverse('frontend:course', kwargs={
            'pk': self.course1.pk})

        topic_list = [
            {"value": "Topic1 (Category~*)", "id": 2},
            {"value": "Topic2 (Category~*)", "id": 3},
            {"value": "Topic3 (Category~*)", "id": 9}
        ]
        data = {
            'topic_list': json.dumps(topic_list)
        }
        response = self.client.post(path, data)
        self.assertContains(response, "form-group is-invalid")

    def test_ajax_and_check_and_ids_course_view(self):
        """CourseView post test case - ajax and check and ids[] are true

        Tests CourseView post if request is ajax and check and ids[] are true.
        """
        path = reverse('frontend:course', kwargs={
            'pk': self.course1.pk})

        topic_list = [
            {"value": "Topic1 (Category~*)", "id": 2},
            {"value": "Topic2 (Category~*)", "id": 3},
            {"value": "Topic3 (Category~*)", "id": 4}
        ]
        data = {
            'topic_list': json.dumps(topic_list),
            'ids[]': [1, 2, 3, 4, 5]
        }
        self.client.post(path, data,
                         **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        ids = Topic.objects.all().values_list("pk", flat=True)
        self.assertEqual(list(ids), [2, 3, 4])


class EditStructureViewTestView(BaseCourseViewTestCase):
    """ edit course structure test cases

    Defines the test cases for view EditCourseStructureView
    """

    def test_edit_course_structure_view(self):
        """EditCourseStructureView post test case - form valid

        Tests EditCourseStructureView post if form is valid.
        """
        path = reverse('frontend:course-edit-structure', kwargs={
            'pk': self.course1.pk})

        form_create_topic = CreateTopicForm(data={'title': 'Topic4', 'category': self.cat.pk})
        # check if the form is valid
        self.assertTrue(form_create_topic.is_valid())

        data = {'title': 'Topic4', 'category': self.cat.pk}  # here should be the id of category
        response = self.client.post(path, data)
        json_response = response.json()
        # the new topic should be added
        self.assertIsNotNone(Topic.objects.get(pk=5))
        # check if the new topic is added to the response data
        self.assertEqual(json_response['topic_id'], 5)

    def test_edit_course_structure_view_invalid(self):
        """EditCourseStructureView post test case - form invalid

        Tests EditCourseStructureView post if form is invalid.
        """
        path = reverse('frontend:course-edit-structure', kwargs={
            'pk': self.course1.pk})
        data = {'title': 'Topic5', 'category': 9}
        form_create_topic = CreateTopicForm(data={'title': 'Topic5', 'category': 9})
        response = self.client.post(path, data)
        # the form should be invalid of our view
        self.assertFalse(form_create_topic.is_valid())
        self.assertContains(response, "form-group is-invalid")


class FavoriteTestCase(BaseCourseViewTestCase):
    """ add_remove_favourites test cases

    Defines the test cases for function based view add_remove_favourites
    """
    def test_add_and_remove_favorite(self):
        """ add_remove_favourites test case - add

        Tests function based view add_remove_favourites when add favorite
        """
        self.assertEqual(self.user.profile.stared_courses.all().count(), 0)

        path = reverse('frontend:favourite_course', kwargs={
            'pk': self.course1.pk})
        data = {'user': self.user,
                'pk': self.course1.pk}
        self.client.post(path, data)
        self.assertEqual(self.user.profile.stared_courses.all().count(), 1)

    def test_remove_favorite(self):
        """add_remove_favourites test case - remove

        Tests function based view add_remove_favourites when remove favorite
        """
        self.assertEqual(self.user.profile.stared_courses.all().count(), 0)

        path = reverse('frontend:favourite_course', kwargs={
            'pk': self.course1.pk})
        data = {'user': self.user,
                'pk': self.course1.pk}
        self.client.post(path, data)
        self.assertEqual(self.user.profile.stared_courses.all().count(), 1)

        self.client.post(path, data)
        self.assertEqual(self.user.profile.stared_courses.all().count(), 0)
