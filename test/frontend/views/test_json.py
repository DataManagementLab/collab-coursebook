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

    def test_validate_topics_correct(self):
        """Validate topics test case - Correct topics

        Tests the function validate_topics if the topics are correct that means the
        topics exists in the database. This means the function return None if the
        validation was successful.
        """
        # Return should be None
        self.assertIsNone(JsonHandler.validate_topics(self.json_data))

    def test_validate_topics_only_main_invalid(self):
        """Validate topics test case - Invalid main topic but valid sub topics

        Tests the function validate_topics if a only main topic is invalid. This means the topic
        does not exists in the data base but its sub topics exists.
        """

        json_data = [{'value': 'Topic1 (Category)', 'id': 2},
                     {'value': 'Topic2 (Category)', 'id': 6,
                      'children': [{'value': 'Topic3 (Category)', 'id': 4}]}]
        self.assertRaises(ValidationError, JsonHandler.validate_topics, json_data)

    def test_validate_topics_only_sub_invalid(self):
        """Validate topics test case - Valid main topic but invalid sub topic

        Tests the function validate_topics if a only main topic is invalid. This means the main
        topic does exists in the data base but a sub topic does not.
        """
        json_data = [{'value': 'Topic1 (Category)', 'id': 2},
                     {'value': 'Topic2 (Category)', 'id': 3,
                      'children': [{'value': 'Topic3 (Category)', 'id': 6}]}]
        self.assertRaises(ValidationError, JsonHandler.validate_topics, json_data)

    def test_clean_topics_no_deletion(self):
        """Clean topics test case - No deletion

        Tests the function clean_topics if the result of it does not not delete any topics
        since the topics were used in the course structure.
        """
        ids = [2, 3, 4]
        JsonHandler.clean_topics(ids)
        ids = Topic.objects.all().values_list("pk", flat=True)
        # The not used id 1 should still be there
        # See also at setup
        self.assertEqual(list(ids), [1, 2, 3, 4])

    def test_clean_topics_deletion_one(self):
        """Clean topics test case - Deletion of one topic

        Tests the function clean_topics if the result of it deletes one topic
        since the topic were not used in the course structure.
        """
        ids = [1, 2, 3, 4]
        JsonHandler.clean_topics(ids)
        ids = Topic.objects.all().values_list("pk", flat=True)
        # The not used id 1 will now be deleted
        self.assertEqual(list(ids), [2, 3, 4])

    def test_clean_topics_deletion_many(self):
        """Clean topics test case - Deletion of many topics

        Tests the function clean_topics if the result of it deletes many topics
        since the topics were not used in the course structure.
        """
        Topic.objects.create(title="Topic4", category=self.cat)
        ids = [1, 2, 3, 4, 5, 6]
        JsonHandler.clean_topics(ids)
        ids = Topic.objects.all().values_list("pk", flat=True)
        # Unused ids 1 and 5 should be deleted, and 6 has not effect
        self.assertEqual(list(ids), [2, 3, 4])

    def test_clean_structure_sub_topic_no_deletion(self):
        """Clean structure sub topics test case - No deletion

        Tests the function clean_structure_sub_topic if the result of it does not delete any sub
        topics since the main topic does not exists topic in the course structure.
        """
        JsonHandler.clean_structure_sub_topic(self.course1, 2, 2)
        # the course should be same as before
        self.assertEqual(JsonHandler.topics_structure_to_json(self.course1), self.json_data)

    def test_clean_structure_sub_topic_deletion_one(self):
        """Clean structure sub topics test case - Deletion of one sub topic

        Tests the function clean_structure_sub_topic if the result of it does delete one sub
        topic since the main topic does exists topic in the course structure.
        """
        JsonHandler.clean_structure_sub_topic(self.course1, 2, 1)
        # The course should only has two topics now
        self.assertEqual(self.course1.topics.all().count(), 2)

    def test_clean_structure_sub_topic_deletion_many(self):
        """Clean structure sub topics test case - Deletion of many sub topics

        Tests clean_structure_sub_topic if more than 1 element to be deleted.
        """
        index = 2
        sub_index = 2
        title = 'Topic'
        title_index = 4
        for i in range(2):
            topic = Topic.objects.create(title=f'{title}{title_index + i}', category=self.cat)
            entry = CourseStructureEntry(course=self.course1, index=f'{index}/{sub_index + i}', topic=topic)
            entry.save()
        # The two new sub topics should be added
        self.assertEqual(JsonHandler.topics_structure_to_json(self.course1),
                         [{'value': 'Topic1 (Category)', 'id': 2},
                          {'value': 'Topic2 (Category)', 'id': 3,
                           'children': [{'value': 'Topic3 (Category)', 'id': 4},
                                        {'value': 'Topic4 (Category)', 'id': 5},
                                        {'value': 'Topic5 (Category)', 'id': 6}
                                        ]}]
                         )
        JsonHandler.clean_structure_sub_topic(self.course1, 2, 2)
        # The course should be same as before
        self.assertEqual(JsonHandler.topics_structure_to_json(self.course1), self.json_data)

    def test_clean_structure_topics_no_deletion(self):
        """Clean structure topics test case - No deletion

        Tests the function clean_structure_sub_topic if the result of it does not delete any
        topics since the topic does not exists in the course structure.
        """
        JsonHandler.clean_structure_topic(self.course1, 5)
        # There should be no topics deleted
        self.assertEqual(JsonHandler.topics_structure_to_json(self.course1), self.json_data)

    def test_clean_structure_topics_deletion_one(self):
        """Clean structure topics test case - Deletion of one topic

        Tests the function clean_structure_sub_topic if the result of it does delete a topic
        topics since the topic exists in the course structure.
        """
        JsonHandler.clean_structure_topic(self.course1, 2)
        self.assertEqual(JsonHandler.topics_structure_to_json(self.course1),
                         [{'value': 'Topic1 (Category)', 'id': 2}])

    def test_clean_structure_topics_deletion_many(self):
        """Clean structure topics test case - Deletion of many topic

        Tests the function clean_structure_sub_topic if the result of it does delete many topic
        topics since the topics exists in the course structure.
        """
        topic = Topic.objects.create(title="Topic4", category=self.cat)
        entry = CourseStructureEntry(course=self.course1, index="3", topic=topic)
        entry.save()
        JsonHandler.clean_structure_topic(self.course1, 2)
        self.assertEqual(JsonHandler.topics_structure_to_json(self.course1),
                         [{'value': 'Topic1 (Category)', 'id': 2}])

    def test_topics_structure_to_json_empty(self):
        """Topics structure to json test case - Empty structure

        Tests the function topics_structure_to_json if it returns an empty list
        if the structure is empty.
        """
        JsonHandler.clean_structure_topic(self.course1, 1)
        length = len(JsonHandler.topics_structure_to_json(self.course1))
        self.assertEqual(length, 0)

    def test_topics_structure_to_json_last_main(self):
        """Topics structure to json test case - Last main topic

        Tests the function topics_structure_to_json if the checked topic is
        the last main topic and is marked as last main topic
        """
        JsonHandler.clean_structure_topic(self.course1, 2)
        self.assertEqual(JsonHandler.topics_structure_to_json(self.course1),
                         [{'value': 'Topic1 (Category)', 'id': 2}])

    def test_topics_structure_to_json_main_with_sub_one(self):
        """Topics structure to json test case - One main topic with sub topics

        Tests the function topics_structure_to_json if the checked topic is
        the first main topic and is appended to the result and contains children.
        """
        JsonHandler.clean_structure_sub_topic(self.course1, 2, 1)
        self.assertEqual(JsonHandler.topics_structure_to_json(self.course1),
                         [{'value': 'Topic1 (Category)', 'id': 2},
                          {'value': 'Topic2 (Category)', 'id': 3}])

    def test_topics_structure_to_json_main_with_sub_many(self):
        """Topics structure to json test case - Many main topic with sub topics

        Tests the function topics_structure_to_json if the many main topics with children
        are correctly parsed.
        """
        self.assertEqual(JsonHandler.topics_structure_to_json(self.course1), self.json_data)

    def test_json_to_topics_structure_empty(self):
        """Json to topics structure - Empty json data

        Tests the function json_to_topics_structure if the topic list is still empty
        after its call.
        """
        JsonHandler.json_to_topics_structure(self.course1, [])
        self.assertEqual(list(self.course1.topics.all()), [])

    def test_json_to_topics_structure_update_main(self):
        """Json to topics structure - Update main topic

        Tests the function json_to_topics_structure that the existing entry will be
        updated with its new order of topic id.
        """
        json_data = [{'value': 'Topic1 (Category)', 'id': 2}]
        JsonHandler.json_to_topics_structure(self.course1, json_data)
        self.assertEqual(self.course1.topics.all().count(), 1)

    def test_update_json_to_topics_structure_update_main_create_sub(self):
        """Json to topics structure - Update main topic and creating sub topic

        Tests the function json_to_topics_structure that the existing entry will be
        updated with its new order of topic id and the sub topics does not exists,
        therefore a new entry will be created.
        """
        json_data = [{'value': 'Topic2 (Category)', 'id': 3,
                      'children': [{'value': 'Topic3 (Category)', 'id': 4}]},
                     {'value': 'Topic1 (Category)', 'id': 2}]
        JsonHandler.json_to_topics_structure(self.course1, json_data)
        self.assertEqual(JsonHandler.topics_structure_to_json(self.course1), json_data)

    def test_update_json_to_topics_structure_update_main_sub(self):
        """Json to topics structure - Update main topic and creating sub topic

        Tests the function json_to_topics_structure that the existing entry will be
        updated with its new order of topic id and the sub topics are also updated.
        """
        JsonHandler.json_to_topics_structure(self.course1, self.json_data)
        self.assertEqual(JsonHandler.topics_structure_to_json(self.course1), self.json_data)

    def test_json_to_topics_structure_new_main(self):
        """Json to topics structure - New main topics

        Tests the function json_to_topics_structure that the new entries will be
        added to the data base and the rest will be updated.
        """
        Topic.objects.create(title="Topic4", category=self.cat)
        json_data = [{'value': 'Topic1 (Category)', 'id': 2},
                     {'value': 'Topic2 (Category)', 'id': 3,
                      'children': [{'value': 'Topic3 (Category)', 'id': 4}]},
                     {'value': 'Topic4 (Category)', 'id': 5}]  # entry for a new topic
        JsonHandler.json_to_topics_structure(self.course1, json_data)
        self.assertEqual(JsonHandler.topics_structure_to_json(self.course1), json_data)

    def test_new_children_json_to_topics_structure(self):
        """Json to topics structure - New sub topics

        Tests the function json_to_topics_structure that the new entries will be
        added to the data base and the rest will be updated.
        """
        topic4 = Topic.objects.create(title="Topic4", category=self.cat)
        json_data = [{'value': 'Topic1 (Category)', 'id': 2},
                     {'value': 'Topic2 (Category)', 'id': 3,
                      'children': [{'value': 'Topic3 (Category)', 'id': 4},
                                   {'value': 'Topic4 (Category)', 'id': 5}]}
                     ]
        JsonHandler.json_to_topics_structure(self.course1, json_data)
        # The new structure should subject to the new json data
        self.assertEqual(JsonHandler.topics_structure_to_json(self.course1), json_data)
