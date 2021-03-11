"""Purpose of this file

This file contains the test cases for /frontend/views/course.py.
"""
import json

from test.test_cases import BaseCourseViewTestCase
from django.urls import reverse

from base.models import CourseStructureEntry, Topic
from frontend.forms.course import CreateTopicForm


class CourseViewTestCase(BaseCourseViewTestCase):
    """ test cases for CourseView

    Defines the test cases for view  CourseView
    """
    def setUp(self):
        """Setup

        Sets up the test database.
        """
        super().setUp()
        self.path = reverse('frontend:course', kwargs={
            'pk': self.course1.pk})
        topic_list = [
            {"value": "Topic1 (Category~*)", "id": 2},
            {"value": "Topic2 (Category~*)", "id": 3},
            {"value": "Topic3 (Category~*)", "id": 9}
        ]
        self.invalid_data = {
            'topic_list': json.dumps(topic_list)
        }

    def test_ajax_and_check_course_view(self):
        """CourseView post test case - request is ajax and check is True

        Tests CourseView post if request is ajax and check is True.
        """
        topic_list = [
            {"value": "Topic1 (Category~*)", "id": 2},
            {"value": "Topic2 (Category~*)", "id": 3},
            {"value": "Topic3 (Category~*)", "id": 4}
        ]
        data = {
            'topic_list': json.dumps(topic_list)
        }

        response = self.client.post(self.path, data,
                                    **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.status_code, 200)
        # after post the structure of topics should also be accordingly changed
        self.assertEqual(list(CourseStructureEntry.objects.all()
                              .values_list("index", flat=True)),
                         ['1', '2', '3'])
        self.assertEqual(list(CourseStructureEntry.objects.all()
                              .values_list("topic_id", flat=True)),
                         [2, 3, 4])
        self.assertIsNotNone(CourseStructureEntry.objects.get(index='3', topic=self.topic3))

    def test_bad_response_course_view(self):
        """CourseView post test case - request is ajax and check is false.

        Tests CourseView post if request is ajax and check is false.
        """
        response = self.client.post(self.path, self.invalid_data,
                                    **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        # it should be a bad response
        self.assertEqual(response.status_code, 400)

    def test_invalid_form_not_ajax_course_view(self):
        """CourseView post test case - form is invalid and request not ajax

        Tests CourseView post if form is invalid and request not ajax.
        """
        response = self.client.post(self.path, self.invalid_data)
        self.assertContains(response, "form-group is-invalid")

    def test_ajax_and_check_and_ids_course_view(self):
        """CourseView post test case - ajax and check and ids[] are true

        Tests CourseView post if request is ajax and check and ids[] are true.
        """
        topic_list = [
            {"value": "Topic1 (Category~*)", "id": 2},
            {"value": "Topic2 (Category~*)", "id": 3},
            {"value": "Topic3 (Category~*)", "id": 4}
        ]
        data = {
            'topic_list': json.dumps(topic_list),
            'ids[]': [1, 2, 3, 4, 5]
        }
        self.client.post(self.path, data,
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
    def test_add_remove_favorite(self):
        """add_remove_favourites test case

        Tests function based view add_remove_favourites
        """
        self.assertEqual(self.user.profile.stared_courses.all().count(), 0)

        path = reverse('frontend:course', kwargs={
            'pk': self.course1.pk})
        data = {'user': self.user,
                'course_pk': self.course1.pk,
                'save': 'true'}
        self.client.post(path, data)
        self.assertEqual(self.user.profile.stared_courses.all().count(), 1)
        data['save'] = 'false'
        self.client.post(path, data)
        self.assertEqual(self.user.profile.stared_courses.all().count(), 0)
