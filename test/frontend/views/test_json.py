from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from frontend.views.json import JsonHandler
from test import utils
from base.models import CourseStructureEntry, Topic, Course, Category
from frontend.views import json
from test.test_cases import MediaTestCase


class JsonHandlerTestCase(MediaTestCase):
    # TODO test review
    def setUp(self):
        super().setUp()

        self.cat = Category.objects.create(title="Category")
        self.course1 = Course.objects.create(title='Course Test', description='desc', category=self.cat)
        self.topic1 = Topic.objects.create(title="Topic1", category=self.cat)
        self.topic2 = Topic.objects.create(title="Topic2", category=self.cat)
        self.topic3 = Topic.objects.create(title="Topic3", category=self.cat)

        course_struc_entry_1 = CourseStructureEntry(course=self.course1, index=1, topic=self.topic1)
        course_struc_entry_2 = CourseStructureEntry(course=self.course1, index=2, topic=self.topic2)
        # TODO: fixed the document of CourseStructureEntry.index, # -> / since we use '/' as splitter
        course_struc_entry_3 = CourseStructureEntry(course=self.course1, index="2/1", topic=self.topic3)
        course_struc_entry_1.save(), course_struc_entry_2.save(), course_struc_entry_3.save()
        # there is already one topic before this set up, so our topics start with 2
        self.json_data = [{'value': 'Topic1 (Category)', 'id': 2},
                          {'value': 'Topic2 (Category)', 'id': 3,
                           'children': [{'value': 'Topic3 (Category)', 'id': 4}]}]

    def test_validate_topics(self):
        # TODO: return of the method validate_topics is "true if ...", is it appropriate?
        json_data2 = [{'value': 'Topic1 (Category)', 'id': 2},
                      {'value': 'Topic2 (Category)', 'id': 3,
                       'children': [{'value': 'Topic3 (Category)', 'id': 6}]}]
        json_data3 = [{'value': 'Topic1 (Category)', 'id': 6},
                      {'value': 'Topic2 (Category)', 'id': 3}]
        self.assertIsNone(JsonHandler.validate_topics(self.json_data))
        # TODO: found a little bug and fixed it
        self.assertRaises(ValidationError, JsonHandler.validate_topics, json_data2)
        self.assertRaises(ValidationError, JsonHandler.validate_topics, json_data3)

    def test_clean_topics(self):
        ids = [1, 2, 3, 4, 5]
        JsonHandler.clean_topics(ids)
        ids = Topic.objects.all().values_list("pk", flat=True)
        # 1 is not used, 5 is unrelated, so only [2, 3, 4] should be left
        self.assertEqual(list(ids), [2, 3, 4])

    def test_clean_structure_sub_topic(self):
        topic4 = Topic.objects.create(title="Topic4", category=self.cat)
        topic5 = Topic.objects.create(title="Topic5", category=self.cat)
        course_struc_entry_4 = CourseStructureEntry(course=self.course1, index="2/2", topic=topic4)
        course_struc_entry_5 = CourseStructureEntry(course=self.course1, index="2/3", topic=topic5)
        course_struc_entry_4.save(), course_struc_entry_5.save()
        # the two new subtopics should be added
        self.assertEqual(JsonHandler.topics_structure_to_json(self.course1),
                         [{'value': 'Topic1 (Category)', 'id': 2},
                          {'value': 'Topic2 (Category)', 'id': 3,
                           'children': [{'value': 'Topic3 (Category)', 'id': 4},
                                        {'value': 'Topic4 (Category)', 'id': 5},
                                        {'value': 'Topic5 (Category)', 'id': 6}
                                        ]}]
                         )
        JsonHandler.clean_structure_sub_topic(self.course1, 2, 2)
        # the course should be same as before
        self.assertEqual(JsonHandler.topics_structure_to_json(self.course1), self.json_data)

    def test_clean_structure_topic(self):
        JsonHandler.clean_structure_topic(self.course1, 2)
        # there should be only topic1 left
        self.assertEqual(JsonHandler.topics_structure_to_json(self.course1),
                         [{'value': 'Topic1 (Category)', 'id': 2}])

    def test_topics_structure_to_json(self):
        self.assertEqual(JsonHandler.topics_structure_to_json(self.course1), self.json_data)

    def test_json_to_topics_structure(self):
        topic4 = Topic.objects.create(title="Topic4", category=self.cat)
        topic5 = Topic.objects.create(title="Topic5", category=self.cat)
        json_data2 = [{'value': 'Topic1 (Category)', 'id': 2},
                      {'value': 'Topic2 (Category)', 'id': 3,
                       'children': [{'value': 'Topic4 (Category)', 'id': 5}]},  # new entry for a new child topic
                      {'value': 'Topic3 (Category)', 'id': 4},  # entry update for a former child topic
                      {'value': 'Topic5 (Category)', 'id': 6}]  # new entry for a new topic
        JsonHandler.json_to_topics_structure(self.course1, json_data2)
        # the new structure should subject to the new json data
        self.assertEqual(JsonHandler.topics_structure_to_json(self.course1), json_data2)
