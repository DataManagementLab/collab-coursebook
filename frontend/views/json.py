"""Purpose of this file

This file describes the json handling on resources needed for frontend views.
"""

from django.core.exceptions import ValidationError

from base.models import CourseStructureEntry, Topic


class JsonHandler:
    """Json handler

    Handles all json related operations related to frontend views.
    """

    @staticmethod
    def validate_topics(json_data):
        """Validate topics from json data

        Checks if the topics from the json data exists in the database.

        :param json_data: The json data containing topics and sub topics
        :type json_data: list[dict[str, Any]]

        :return: None if all topics in the json data exists
        :rtype: None or ValidationError
        """
        # Main topics
        for topic in json_data:
            if not Topic.objects.filter(id=topic['id']).exists():
                raise ValidationError(f'The topic with the id {topic["id"]} does not exist')
            # Sub topics
            if 'children' in topic:
                for sub_topic in topic['children']:
                    if not Topic.objects.filter(id=sub_topic['id']).exists():
                        raise ValidationError(
                            f'The sub topic with the id {sub_topic["id"]} does not exist')

    @staticmethod
    def json_to_topics_structure(course, json_data):
        """Json to topic structure

        Creates a course structure from the json data and override the current stored
        entries in the database.

        Example json data: [{'id': 1, 'children': [{'id': 3}]},
        {'id': 1}]

        :param course: The Course where the structure should be modified
        :type course: Course
        :param json_data: The json data
        :type json_data: list[dict[str, Any]]

        :return: true if the structure was changed after its call
        :rtype: bool
        """
        course_id = course.id
        index = 0
        # Main topics
        for topic in json_data:
            index += 1
            current_id = topic['id']
            current_index = f'{index}'
            current_topic = CourseStructureEntry.objects.filter(
                index=current_index,
                course_id=course_id)
            # Updates the entry in the data base if it exists, else we create a new entry
            if current_topic.exists():
                current_topic.update(topic_id=current_id)
            else:
                CourseStructureEntry.objects.create(
                    index=current_index,
                    course_id=course_id,
                    topic_id=current_id)
            # Sub topics
            sub_index = 0
            if 'children' in topic:
                for sub_topic in topic['children']:
                    sub_index += 1
                    current_id = sub_topic['id']
                    current_index = f'{index}/{sub_index}'
                    current_topic = CourseStructureEntry.objects.filter(
                        index=current_index,
                        course_id=course_id)
                    # Updates the entry in the data base if it exists, else we create a new entry
                    if current_topic.exists():
                        current_topic.update(topic_id=current_id)
                    else:
                        CourseStructureEntry.objects.create(
                            index=current_index,
                            course_id=course_id,
                            topic_id=current_id)
            # Clean sub topic fragments
            JsonHandler.clean_structure_sub_topic(course=course,
                                                  index=index,
                                                  sub_index=sub_index + 1)
        # Clean topic fragments
        JsonHandler.clean_structure_topic(course=course, index=index + 1)
        return True

    @staticmethod
    def topics_structure_to_json(course):
        """Topic structure to json

        Creates a json object representing the structure of the course from the given course.

        :param course: The course object of the structure
        :type course: Course

        :return: a json object of the topic structure
        :rtype: List[Optional[Dict[str, Union[int, list]]]]
        """
        # Generates json object representing the structure of the model
        json_obj = []
        # Saves last main topic to append its children later
        last_main_topic = None
        for topic in course.get_sorted_topic_list():
            # Course structure
            structure = CourseStructureEntry.objects.get(topic=topic, course=course)
            # Possible sub topic
            structure_index = structure.index.split('/')

            topic_json = {'value': topic.__str__(), 'id': topic.id}

            if len(structure_index) == 1:
                # Appends the first main topic
                if last_main_topic is not None:
                    json_obj.append(last_main_topic)
                # Checks if a main topic has sub topics
                if CourseStructureEntry.objects.filter(
                        course=course,
                        index__startswith=str(structure_index[0])).count() > 1:
                    topic_json['children'] = []
                last_main_topic = topic_json
            else:
                last_main_topic['children'].append(topic_json)

        # Appends the first topic: 'if last_main_topic is not None' does not get
        # called if there is only one main topic
        if last_main_topic is not None:
            json_obj.append(last_main_topic)
        return json_obj

    @staticmethod
    def clean_structure_topic(course, index):
        """Clean structure topic

        Cleans all course structure entries after the given index (include).
        That means all topics starting from the given index and its sub topics
        are removed after this call.

        :param course: The course where we want to clean the entries
        :type course: Course
        :param index: The index where we start to clean
        :type index: int
        """
        course_id = course.id
        topic = CourseStructureEntry.objects.filter(index=f'{index}',
                                                    course_id=course_id)
        while topic.exists():
            topic.delete()
            JsonHandler.clean_structure_sub_topic(course=course, index=index, sub_index=1)
            index += 1
            topic = CourseStructureEntry.objects.filter(index=f'{index}',
                                                        course_id=course_id)

    @staticmethod
    def clean_structure_sub_topic(course, index, sub_index):
        """Clean structure sub topic

        Cleans all course structure entries after the given sub index (include) of
        the given index. That means all sub topics starting from the given sub index
        of the given index are removed after this call.

        :param course: The course where we want to clean the entries
        :type course: Course
        :param index: The index where we start to clean
        :type index: int
        :param sub_index: The sub index where we start
        :type sub_index: int
        """
        course_id = course.id
        topic = CourseStructureEntry.objects.filter(index=f'{index}/{sub_index}',
                                                    course_id=course_id)
        while topic.exists():
            topic.delete()
            sub_index += 1
            topic = CourseStructureEntry.objects.filter(index=f'{index}/{sub_index}',
                                                        course_id=course_id)

    @staticmethod
    def clean_topics(ids):
        """Clean topics

        Cleans the topics if they were not used in the course structure.
        """
        for topic_id in ids:
            if not CourseStructureEntry.objects.filter(topic_id=topic_id).exists():
                Topic.objects.filter(pk=topic_id).delete()
