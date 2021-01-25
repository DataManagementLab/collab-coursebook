from django.test import TestCase, override_settings
import io
from base.models.content import Category, Course, Topic
from django.contrib.auth.models import User
from django.urls import reverse
from content.models import ImageAttachment
import tempfile
import shutil
from PIL import Image

MEDIA_ROOT = tempfile.mkdtemp()


# Create your tests here.
def generate_image_file():
    """ Generate image file
    Generates an image file which can be uses for testing

    :return: the generated image file
    :rtype: io.BytesIO
    """
    # https://gist.github.com/guillaumepiot/817a70706587da3bd862835c59ef584e
    file = io.BytesIO()
    image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
    image.save(file, 'png')
    file.name = 'test.png'
    file.seek(0)
    return file


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class SomeTest(TestCase):
    def setUp(self):
        """
        Sets up the test database
        """
        User.objects.create_superuser("admin")
        cat = Category.objects.create(title="Category")
        Course.objects.create(title="Course", description="description", category=cat)
        Topic.objects.create(title="Topic", category=cat)
        self.client.force_login(User.objects.get(pk=1))

    @classmethod
    def tearDownClass(cls):
        """
        Deletes the generated files after running the tests.
        """
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def post_redirects_to_content(self, path, data):
        """
        Tests that the Post request with the given path and data redirects to the content page of the newly
        created Content

        :param path: The path used for the POST request
        :type path: str
        :param data: The data of the content to be created used for the post request
        :type data: dict
        """
        response = self.client.post(path, data)
        self.assertEqual(response.status_code, 302)
        response_path = reverse('frontend:content', kwargs={
            'course_id': 1, 'topic_id': 1, 'pk': 1
        })
        self.assertEqual(response.url, response_path)

    def test_add_ImageAttachment(self):
        """Test add ImageAttachment

        Tests that an ImageAttachment gets created and saved properly after sending a POST request to content-add
        and that the POST request redirects to the content page.
        """
        path = reverse('frontend:content-add', kwargs={
            'course_id': 1, 'topic_id': 1, 'type': 'ImageAttachment'
        })
        img = generate_image_file()
        data = {
            'language': 'de',
            'image': img,
            'source': 'src',
        }
        self.post_redirects_to_content(path, data)
        self.assertEqual(ImageAttachment.objects.count(), 1)
        content = ImageAttachment.objects.first()
        self.assertTrue(bool(content.image))
        self.assertEqual(content.source, "src")
