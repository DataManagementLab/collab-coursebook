from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from frontend.views.json import JsonHandler
from test import utils
from base.models import CourseStructureEntry, Topic, Course, Category
from frontend.views import json
from test.test_cases import MediaTestCase


class JsonHandlerTestCase(MediaTestCase):
    """ test cases for JsonHandler

    Defines the test cases for JsonHandler
    """

    # TODO test review
    def setUp(self):
        """Setup

        Sets up the test database.
        """
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

    def test_correct_validate_topics(self):
        """Test validate_topics case 1

        Tests validate_topics if topic and sub_topic exist.
        """
        # return should be None
        self.assertIsNone(JsonHandler.validate_topics(self.json_data))

    def test_topic_miss_validate_topics(self):
        """Test validate_topics case 2

        Tests validate_topics if topic doesn't exist but sub_topic exists.
        """

        json_data2 = [{'value': 'Topic1 (Category)', 'id': 2},
                      {'value': 'Topic2 (Category)', 'id': 6,
                       'children': [{'value': 'Topic3 (Category)', 'id': 4}]}]
        # TODO: found a little bug and fixed it
        self.assertRaises(ValidationError, JsonHandler.validate_topics, json_data2)

    def test_topic_miss_validate_topics(self):
        """Test validate_topics case 3

        Tests validate_topics if topic exits but sub_topic doesn't exist.
        """
        json_data2 = [{'value': 'Topic1 (Category)', 'id': 2},
                      {'value': 'Topic2 (Category)', 'id': 3,
                       'children': [{'value': 'Topic3 (Category)', 'id': 6}]}]

        self.assertRaises(ValidationError, JsonHandler.validate_topics, json_data2)

    def test_0_clean_topics(self):
        """Test clean_topics case 1

        Tests clean_topics if 0 element to be deleted.
        """
        ids = [2, 3, 4]
        JsonHandler.clean_topics(ids)
        ids = Topic.objects.all().values_list("pk", flat=True)
        # the not used id 1 should still be there
        self.assertEqual(list(ids), [1, 2, 3, 4])

    def test_1_clean_topics(self):
        """Test clean_topics case 2

        Tests clean_topics if exactly 1 element to be deleted.
        """
        ids = [1, 2, 3, 4]
        JsonHandler.clean_topics(ids)
        ids = Topic.objects.all().values_list("pk", flat=True)
        # the not used id 1 will now be deleted
        self.assertEqual(list(ids), [2, 3, 4])

    def test_more_clean_topics(self):
        """Test clean_topics case 3

        Tests clean_topics if more than 1 element to be deleted.
        """
        Topic.objects.create(title="Topic4", category=self.cat)
        ids = [1, 2, 3, 4, 5, 6]
        JsonHandler.clean_topics(ids)
        ids = Topic.objects.all().values_list("pk", flat=True)
        # unused ids 1 and 5 should be deleted, and 6 has not effect
        self.assertEqual(list(ids), [2, 3, 4])

    def test_0_clean_structure_sub_topic(self):
        """Test clean_structure_sub_topic case 1

        Tests clean_structure_sub_topic if 0 element to be deleted.
        """
        JsonHandler.clean_structure_sub_topic(self.course1, 2, 2)
        # the course should be same as before
        self.assertEqual(JsonHandler.topics_structure_to_json(self.course1), self.json_data)

    def test_1_clean_structure_sub_topic(self):
        """Test clean_structure_sub_topic case 2

        Tests clean_structure_sub_topic if exactly 1 element to be deleted.
        """
        JsonHandler.clean_structure_sub_topic(self.course1, 2, 1)
        # the course should only has two topics now
        self.assertEqual(self.course1.topics.all().count(), 2)

    def test_more_clean_structure_sub_topic(self):
        """Test clean_structure_sub_topic case 3

        Tests clean_structure_sub_topic if more than 1 element to be deleted.
        """
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

    def test_0_clean_structure_topic(self):
        """Test clean_structure_topic case 1

        Tests clean_structure_topic if 0 element to be deleted.
        """
        JsonHandler.clean_structure_topic(self.course1, 5)
        # there should be no topics deleted
        self.assertEqual(JsonHandler.topics_structure_to_json(self.course1), self.json_data)

    def test_1_clean_structure_topic(self):
        """Test clean_structure_topic case 2

        Tests clean_structure_topic if exactly 1 element to be deleted.
        """
        JsonHandler.clean_structure_topic(self.course1, 2)
        self.assertEqual(JsonHandler.topics_structure_to_json(self.course1),
                         [{'value': 'Topic1 (Category)', 'id': 2}])

    def test_more_clean_structure_topic(self):
        """Test clean_structure_topic case 3

        Tests clean_structure_topic if more than 1 element to be deleted.
        """
        topic4 = Topic.objects.create(title="Topic4", category=self.cat)
        course_struc_entry_4 = CourseStructureEntry(course=self.course1, index="3", topic=topic4)
        course_struc_entry_4.save()
        JsonHandler.clean_structure_topic(self.course1, 2)
        self.assertEqual(JsonHandler.topics_structure_to_json(self.course1),
                         [{'value': 'Topic1 (Category)', 'id': 2}])

    def test_0_topics_structure_to_json(self):
        """Test topics_structure_to_json case 1

        Tests topics_structure_to_json if 0 topic in the course
        """
        JsonHandler.clean_structure_topic(self.course1, 1)
        # TODO: under this situation is [None] intended?
        self.assertEqual(JsonHandler.topics_structure_to_json(self.course1), [None])

    def test_1_topics_structure_to_json(self):
        """Test topics_structure_to_json case 2

        Tests topics_structure_to_json if only 1 topic in the course
        """
        JsonHandler.clean_structure_topic(self.course1, 2)
        self.assertEqual(JsonHandler.topics_structure_to_json(self.course1),
                         [{'value': 'Topic1 (Category)', 'id': 2}])

    def test_2_topics_structure_to_json(self):
        """Test topics_structure_to_json case 3

        Tests topics_structure_to_json if more than 1 topic in the course and no child
        """
        JsonHandler.clean_structure_sub_topic(self.course1, 2, 1)
        self.assertEqual(JsonHandler.topics_structure_to_json(self.course1),
                         [{'value': 'Topic1 (Category)', 'id': 2},
                          {'value': 'Topic2 (Category)', 'id': 3}])

    def test_children_topics_structure_to_json(self):
        """Test topics_structure_to_json case 4

        Tests topics_structure_to_json if more than topics in the course and with child(ren)
        """
        self.assertEqual(JsonHandler.topics_structure_to_json(self.course1), self.json_data)

    def test_0_json_to_topics_structure(self):
        """Test json_to_topics_structure case 1

        Tests json_to_topics_structure if given json_data is empty
        """
        JsonHandler.json_to_topics_structure(self.course1, [])
        self.assertEqual(list(self.course1.topics.all()), [])

    def test_1_json_to_topics_structure(self):
        """Test json_to_topics_structure case 2

        Tests json_to_topics_structure if given json_data has only 1 and existing element
        """
        json_data = [{'value': 'Topic1 (Category)', 'id': 2}]
        JsonHandler.json_to_topics_structure(self.course1, json_data)
        self.assertEqual(self.course1.topics.all().count(), 1)

    def test_update_json_to_topics_structure(self):
        """Test json_to_topics_structure case 3

        Tests json_to_topics_structure if given json_data has more than 1 existing element and with update for former
        topics (including child(ren))
        """
        json_data = [{'value': 'Topic2 (Category)', 'id': 3,
                      'children': [{'value': 'Topic3 (Category)', 'id': 4}]},
                     {'value': 'Topic1 (Category)', 'id': 2}]
        JsonHandler.json_to_topics_structure(self.course1, json_data)
        self.assertEqual(JsonHandler.topics_structure_to_json(self.course1), json_data)

    def test_old_json_to_topics_structure(self):
        """Test json_to_topics_structure case 4

        Tests json_to_topics_structure if given json_data has no change to existing structure
        """
        JsonHandler.json_to_topics_structure(self.course1, self.json_data)
        self.assertEqual(JsonHandler.topics_structure_to_json(self.course1), self.json_data)

    def test_new_json_to_topics_structure(self):
        """Test json_to_topics_structure case 5

        Tests json_to_topics_structure if given json_data has new topic entry for the existing structure
        """
        Topic.objects.create(title="Topic4", category=self.cat)
        json_data = [{'value': 'Topic1 (Category)', 'id': 2},
                     {'value': 'Topic2 (Category)', 'id': 3,
                      'children': [{'value': 'Topic3 (Category)', 'id': 4}]},
                     {'value': 'Topic4 (Category)', 'id': 5}]  # entry for a new topic
        JsonHandler.json_to_topics_structure(self.course1, json_data)
        self.assertEqual(JsonHandler.topics_structure_to_json(self.course1), json_data)

    def test_new_children_json_to_topics_structure(self):
        """Test json_to_topics_structure case 6

        Tests json_to_topics_structure if given json_data has new sub topic entry for the existing structure
        """
        topic4 = Topic.objects.create(title="Topic4", category=self.cat)
        json_data = [{'value': 'Topic1 (Category)', 'id': 2},
                     {'value': 'Topic2 (Category)', 'id': 3,
                      'children': [{'value': 'Topic3 (Category)', 'id': 4},
                                   {'value': 'Topic4 (Category)', 'id': 5}]}
                     ]
        JsonHandler.json_to_topics_structure(self.course1, json_data)
        # the new structure should subject to the new json data
        self.assertEqual(JsonHandler.topics_structure_to_json(self.course1), json_data)
