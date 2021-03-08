"""Purpose of this file

This file contains the test cases for /frontend/views/json.py.
"""

from test.test_cases import BaseCourseViewTestCase
from django.core.exceptions import ValidationError

from frontend.views.json import JsonHandler

from base.models import CourseStructureEntry, Topic


class ValidateTopicsTestCase(BaseCourseViewTestCase):
    """ test cases for JsonHandler.validate_topics

    Defines the test cases for JsonHandler.validate_topics
    """
    def test_validate_topics_correct(self):
        """Validate topics test case - Correct topics

        Tests the function validate_topics if the topics are correct that means the
        topics exists in the database. This means the function return None if the
        validation was successful.
        """
        # Return should be None
        json_data = [{'value': 'Topic1 (Category)', 'id': 2},
                     {'value': 'Topic2 (Category)', 'id': 3,
                      'children': [{'value': 'Topic3 (Category)', 'id': 4}]}]
        self.assertIsNone(JsonHandler.validate_topics(json_data))

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

        Tests the function validate_topics if a main topic is valid but its sub topic is invalid. This means the main
        topic does exists in the data base but a sub topic does not.
        """
        json_data = [{'value': 'Topic1 (Category)', 'id': 2},
                     {'value': 'Topic2 (Category)', 'id': 3,
                      'children': [{'value': 'Topic3 (Category)', 'id': 6}]}]
        self.assertRaises(ValidationError, JsonHandler.validate_topics, json_data)

    def test_validate_topics_main_and_sub_invalid(self):
        """Validate topics test case - Invalid main topic and invalid sub topic

        Tests the function validate_topics if a main topic and its sub topic are invalid.
        This means the main topic does not exists in the data base and the sub topic
        does not either.
        """

        json_data = [{'value': 'Topic1 (Category)', 'id': 2},
                     {'value': 'Topic2 (Category)', 'id': 6,
                      'children': [{'value': 'Topic3 (Category)', 'id': 7}]}]
        self.assertRaises(ValidationError, JsonHandler.validate_topics, json_data)

    def test_validate_topics_many_main_invalid(self):
        """Validate topics test case - many invalid main topics but valid sub topics

        Tests the function validate_topics if many main topics are invalid. This means the topics
        does not exists in the data base but its sub topics exists.
        """

        json_data = [{'value': 'Topic1 (Category)', 'id': 5},
                     {'value': 'Topic2 (Category)', 'id': 8,
                      'children': [{'value': 'Topic3 (Category)', 'id': 4}]},
                     {'value': 'Topic6 (Category)', 'id': 9},
                     {'value': 'Topic7 (Category)', 'id': 10}]
        self.assertRaises(ValidationError, JsonHandler.validate_topics, json_data)

    def test_validate_topics_many_sub_invalid(self):
        """Validate topics test case - Valid main topics but many invalid sub topics

        Tests the function validate_topics if many sub topics are invalid. This means the sub topics
        does not exists in the data base but its main topics exists.
        """

        json_data = [{'value': 'Topic1 (Category)', 'id': 2},
                     {'value': 'Topic2 (Category)', 'id': 3,
                      'children': [{'value': 'Topic3 (Category)', 'id': 4},
                                   {'value': 'Topic6 (Category)', 'id': 9},
                                   {'value': 'Topic7 (Category)', 'id': 10}]}
                     ]
        self.assertRaises(ValidationError, JsonHandler.validate_topics, json_data)


class CleanTestCase(BaseCourseViewTestCase):
    """ test cases for JsonHandlers clean methods

    Defines the test cases for JsonHandler.clean_structure_topic,
    clean_structure_sub_topic, clean_topics
    """

    def add_subtopics(self):
        """Add Subtopics

        Adds 4 subtopics to topic 2
        """
        index = 2
        sub_index = 2
        title = 'Topic'
        title_index = 4
        for i in range(4):
            topic = Topic.objects.create(title=f'{title}{title_index + i}', category=self.cat)
            entry = CourseStructureEntry(course=self.course1,
                                         index=f'{index}/{sub_index + i}', topic=topic)
            entry.save()

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
        title = 'Topic'
        index = 4
        for i in range(3):
            Topic.objects.create(title=f'{title}{index + i}', category=self.cat)
        ids = [1, 2, 3, 4, 5, 6, 7, 8]
        JsonHandler.clean_topics(ids)
        ids = Topic.objects.all().values_list("pk", flat=True)
        # unused ids 1, 5, 6, 7 should be deleted, and 8 has not effect
        self.assertEqual(list(ids), [2, 3, 4])

    def test_clean_structure_sub_topic_no_deletion(self):
        """Clean structure sub topics test case - No deletion

        Tests the function clean_structure_sub_topic if the result of it does not delete any sub
        topics since the main topic does not exists topic in the course structure.
        """
        JsonHandler.clean_structure_sub_topic(self.course1, 2, 2)
        # no topics of the course should be deleted
        ids = self.course1.topics.all().values_list("pk", flat=True)
        self.assertEqual(list(ids), [2, 3, 4])

    def test_clean_structure_sub_topic_deletion_one(self):
        """Clean structure sub topics test case - Deletion of one sub topic

        Tests the function clean_structure_sub_topic if the result of it does delete one sub
        topic since the main topic does exists topic in the course structure.
        """
        JsonHandler.clean_structure_sub_topic(self.course1, 2, 1)
        # the course should only has two topics now
        self.assertEqual(self.course1.topics.all().count(), 2)
        self.assertEqual(list(CourseStructureEntry.objects.all().values_list("index", flat=True)),
                         ['1', '2'])

    def test_clean_structure_sub_topic_deletion_many(self):
        """Clean structure sub topics test case - Deletion of many sub topics

        Tests clean_structure_sub_topic if more than 1 element to be deleted.
        """
        self.add_subtopics()
        # The four new sub topics should be added
        ids_1 = self.course1.topics.all().values_list("pk", flat=True)
        self.assertEqual(list(ids_1), [2, 3, 4, 5, 6, 7, 8])
        JsonHandler.clean_structure_sub_topic(self.course1, 2, 2)
        ids = self.course1.topics.all().values_list("pk", flat=True)
        # the course should be same as before
        self.assertEqual(list(ids), [2, 3, 4])
        self.assertEqual(list(CourseStructureEntry.objects.all().values_list("index", flat=True)),
                         ['1', '2', '2/1'])

    def test_clean_structure_topics_no_deletion(self):
        """Clean structure topics test case - No deletion

        Tests the function clean_structure_sub_topic if the result of it does not delete any
        topics since the topic does not exists in the course structure.
        """
        JsonHandler.clean_structure_topic(self.course1, 5)
        # There should be no topics deleted
        ids = self.course1.topics.all().values_list("pk", flat=True)
        self.assertEqual(list(ids), [2, 3, 4])
        self.assertIsNotNone(CourseStructureEntry.objects.get(index='2/1', topic=self.topic3))

    def test_clean_structure_topics_deletion_one(self):
        """Clean structure topics test case - Deletion of one topic

        Tests the function clean_structure_sub_topic if the result of it does delete a topic
        topics since the topic exists in the course structure.
        """
        JsonHandler.clean_structure_topic(self.course1, 2)
        ids = self.course1.topics.all().values_list("pk", flat=True)
        self.assertEqual(list(ids), [2])

    def test_clean_structure_topics_deletion_many(self):
        """Clean structure topics test case - Deletion of many topic

        Tests the function clean_structure_sub_topic if the result of it does delete many topic
        topics since the topics exists in the course structure.
        """
        self.add_subtopics()
        JsonHandler.clean_structure_topic(self.course1, 2)
        ids = self.course1.topics.all().values_list("pk", flat=True)
        self.assertEqual(list(ids), [2])


class JsonTestCase(BaseCourseViewTestCase):
    """ test cases for JsonHandlers Json Methods

    Defines the test cases for JsonHandler.json_to_topics_structure,
    topics_structure_to_json
    """

    def test_topics_structure_to_json_empty(self):
        """Topics structure to json test case - Empty structure

        Tests the function topics_structure_to_json if it returns an empty list
        if the structure is empty.
        """
        for topic in CourseStructureEntry.objects.all():
            topic.delete()
        length = len(JsonHandler.topics_structure_to_json(self.course1))
        self.assertEqual(length, 0)

    def test_topics_structure_to_json_last_main(self):
        """Topics structure to json test case - Last main topic

        Tests the function topics_structure_to_json if the checked topic is
        the last main topic and is marked as last main topic
        """
        for topic in CourseStructureEntry.objects.all():
            if topic.index != '1':
                topic.delete()
        self.assertEqual(JsonHandler.topics_structure_to_json(self.course1),
                         [{'value': 'Topic1 (Category)', 'id': 2}])

    def test_topics_structure_to_json_many_main(self):
        """Topics structure to json test case - many main topics

        Tests the function topics_structure_to_json if there are many main topics
        """
        for topic in CourseStructureEntry.objects.all():
            if topic.index == '2/1':
                topic.delete()
        index = 3
        title = 'Topic'
        title_index = 4
        for i in range(2):
            topic = Topic.objects.create(title=f'{title}{title_index + i}', category=self.cat)
            entry = CourseStructureEntry(course=self.course1, index=f'{index + i}', topic=topic)
            entry.save()

        self.assertEqual(JsonHandler.topics_structure_to_json(self.course1),
                         [{'value': 'Topic1 (Category)', 'id': 2},
                          {'value': 'Topic2 (Category)', 'id': 3},
                          {'value': 'Topic4 (Category)', 'id': 5},
                          {'value': 'Topic5 (Category)', 'id': 6}
                          ])

    def test_topics_structure_to_json_main_with_sub_one(self):
        """Topics structure to json test case - One main topic with sub topics

        Tests the function topics_structure_to_json if the checked topic is
        the first main topic and is appended to the result and contains children.
        """
        for topic in CourseStructureEntry.objects.all():
            if topic.index == '1':
                topic.delete()
        self.assertEqual(JsonHandler.topics_structure_to_json(self.course1),
                         [{'value': 'Topic2 (Category)', 'id': 3,
                           'children': [{'value': 'Topic3 (Category)', 'id': 4}]}])

    def test_topics_structure_to_json_main_with_sub_many(self):
        """Topics structure to json test case - Many main topic with sub topics

        Tests the function topics_structure_to_json if the many main topics with children
        are correctly parsed.
        """
        index = 1
        title = 'Topic'
        title_index = 4
        sub_index = 1
        for i in range(2):
            topic = Topic.objects.create(title=f'{title}{title_index + i}', category=self.cat)
            entry = CourseStructureEntry(course=self.course1,
                                         index=f'{index}/{sub_index + i}', topic=topic)
            entry.save()
        self.assertEqual(JsonHandler.topics_structure_to_json(self.course1),
                         [{'value': 'Topic1 (Category)', 'id': 2,
                           'children': [{'value': 'Topic4 (Category)', 'id': 5},
                                        {'value': 'Topic5 (Category)', 'id': 6}]},
                          {'value': 'Topic2 (Category)', 'id': 3,
                           'children': [{'value': 'Topic3 (Category)', 'id': 4}]}])

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
        json_data = [{'value': 'Topic2 (Category)', 'id': 3},
                     {'value': 'Topic1 (Category)', 'id': 2,
                     'children': [{'value': 'Topic3 (Category)', 'id': 4}]}]
        JsonHandler.json_to_topics_structure(self.course1, json_data)
        self.assertEqual(list(CourseStructureEntry.objects.all()
                              .values_list("index", flat=True)),
                         ['1', '2', '2/1'])
        self.assertEqual(list(CourseStructureEntry.objects.all()
                              .values_list("topic_id", flat=True)),
                         [2, 3, 4])
        self.assertIsNotNone(CourseStructureEntry.objects.get(index='2/1', topic=self.topic3))
        self.assertIsNotNone(CourseStructureEntry.objects.get(index='1', topic=self.topic2))

    def test_update_json_to_topics_structure_update_main_create_sub(self):
        """Json to topics structure - Update main topic and creating sub topic

        Tests the function json_to_topics_structure that the existing entry will be
        updated with its new order of topic id and the sub topics does not exists,
        therefore a new entry will be created.
        """
        for topic in CourseStructureEntry.objects.all():
            if topic.index == '2/1':
                topic.delete()
        self.test_update_json_to_topics_structure_update_main_sub()

    def test_update_json_to_topics_structure_update_main_sub(self):
        """Json to topics structure - Update main topic and creating sub topic

        Tests the function json_to_topics_structure that the existing entry will be
        updated with its new order of topic id and the sub topics are also updated.
        """
        json_data = [{'value': 'Topic2 (Category)', 'id': 3,
                      'children': [{'value': 'Topic3 (Category)', 'id': 4}]},
                     {'value': 'Topic1 (Category)', 'id': 2}]
        JsonHandler.json_to_topics_structure(self.course1, json_data)
        self.assertEqual(list(CourseStructureEntry.objects.all()
                              .values_list("index", flat=True)),
                         ['1', '2', '1/1'])
        self.assertEqual(list(CourseStructureEntry.objects.all()
                              .values_list("topic_id", flat=True)),
                         [2, 3, 4])
        self.assertIsNotNone(CourseStructureEntry.objects.get(index='1/1', topic=self.topic3))
        self.assertIsNotNone(CourseStructureEntry.objects.get(index='1', topic=self.topic2))

    def test_json_to_topics_structure_new_main(self):
        """Json to topics structure - New main topics

        Tests the function json_to_topics_structure that the new entries will be
        added to the data base and the rest will be updated.
        """
        topic4 = Topic.objects.create(title="Topic4", category=self.cat)
        json_data = [{'value': 'Topic1 (Category)', 'id': 2},
                     {'value': 'Topic2 (Category)', 'id': 3,
                      'children': [{'value': 'Topic3 (Category)', 'id': 4}]},
                     {'value': 'Topic4 (Category)', 'id': 5}]  # entry for a new topic
        JsonHandler.json_to_topics_structure(self.course1, json_data)
        self.assertEqual(list(CourseStructureEntry.objects.all()
                              .values_list("index", flat=True)),
                         ['1', '2', '2/1', '3'])
        self.assertEqual(list(CourseStructureEntry.objects.all()
                              .values_list("topic_id", flat=True)),
                         [2, 3, 4, 5])
        self.assertIsNotNone(CourseStructureEntry.objects.get(index='3', topic=topic4))

    def test_new_children_json_to_topics_structure(self):
        """Json to topics structure - New sub topics

        Tests the function json_to_topics_structure that the new entries will be
        added to the data base and the rest will be updated.
        """
        topic4 = Topic.objects.create(title="Topic4", category=self.cat)
        topic5 = Topic.objects.create(title="Topic5", category=self.cat)

        json_data = [{'value': 'Topic1 (Category)', 'id': 2,
                      'children': [{'value': 'Topic5 (Category)', 'id': 6}]},
                     {'value': 'Topic2 (Category)', 'id': 3,
                      'children': [{'value': 'Topic3 (Category)', 'id': 4},
                                   {'value': 'Topic4 (Category)', 'id': 5}]}
                     ]
        JsonHandler.json_to_topics_structure(self.course1, json_data)
        # the new structure should subject to the new json data
        self.assertEqual(list(CourseStructureEntry.objects.all()
                              .values_list("index", flat=True)),
                         ['1', '2', '2/1', '1/1', '2/2'])
        self.assertEqual(list(CourseStructureEntry.objects.all()
                              .values_list("topic_id", flat=True)),
                         [2, 3, 4, 5, 6])
        self.assertIsNotNone(CourseStructureEntry.objects.get(index='2/2', topic=topic4))
        self.assertIsNotNone(CourseStructureEntry.objects.get(index='1/1', topic=topic5))
