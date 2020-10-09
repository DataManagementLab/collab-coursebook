"""
custom JSON class
"""
from base.models import content


class JsonHandler:
    """
    class for outsourced json methods
    """
    @staticmethod
    def create_structures_from_json_data(course, data):
        """
        creates a course structure from json data
        for example: [{'value': 'Thema1', 'id': 1, 'children': [{'value': 'UnterThema1', 'id': 2}]},
        {'value': 'Thema2', 'id': 3}]
        :param Course course: the course where the structures are created
        :param data: the json data
        :return: None
        """
        for i in range(0, len(data)):
            main_topic = data[i]
            topic_name = main_topic['value']
            topic_id = main_topic['id']
            order = str(i + 1)
            topic = content.Topic.objects.get(title=topic_name)
            content.Structure.objects.create(topic=topic, course=course, index=order)
            if 'children' in main_topic.keys():
                children = main_topic['children']
                for j in range(0, len(children)):
                    child = children[j]
                    child_topic_name = child['value']
                    order = str(i + 1) + "/" + str(j + 1)
                    # create child structure
                    topic = content.Topic.objects.get(title=child_topic_name)
                    content.Structure.objects.create(topic=topic, course=course, index=order)
            print(topic_name, topic_id)

    @staticmethod
    def create_json_topics_structure(course):
        """
        creates a json object for usage in the edit structure form view
        :param Course course: course of the structure
        :return: a json object
        """
        # generate json structure from model
        json_response = []
        i = 0
        # save last main topic to append children later in iteration
        last_main_topic = None
        for topic in course.get_sorted_topic_list():
            i += 1
            structure = content.Structure.objects.get(topic=topic, course=course)
            structure_index = structure.index.split('/')
            if len(structure_index) == 1:
                # append the first main topic
                if last_main_topic is not None:
                    json_response.append(last_main_topic)
                # check if a main topic has children
                if len(content.Structure.objects.filter(course=course, index__startswith=str(structure_index[0]))) > 1:
                    last_main_topic = {'value': topic.title, 'id': i, 'children': []}
                else:
                    last_main_topic = {'value': topic.title, 'id': i}
            else:
                last_main_topic['children'].append({'value': topic.title, 'id': i})
        # append the first topic: 'if last_main_topic is not None' does not get called if there is only one main topic
        json_response.append(last_main_topic)
        return json_response
