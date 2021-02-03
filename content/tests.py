"""Purpose of this file

This file contains the test cases for this package.
"""

import io

import shutil

import tempfile

from PIL import Image

# pylint: disable=imported-auth-user
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse

from base.models import Content, Category, Course, Topic

import content.models as model

# Temporary media directory
MEDIA_ROOT = tempfile.mkdtemp()


def generate_image_file(image_file_number):
    """ Generate image file
    Generates an image file which can be uses for testing

    :param image_file_number: number of the image file to be generated
    :type image_file_number: int

    :return: the generated image file
    :rtype: io.BytesIO
    """
    # https://gist.github.com/guillaumepiot/817a70706587da3bd862835c59ef584e
    file = io.BytesIO()
    image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
    image.save(file, 'png')
    file.name = f'test{image_file_number}.png'
    file.seek(0)
    return file


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class ContentTypesTestCase(TestCase):
    """Image attachment test case

    This test case tests model ImageAttachment.
    """

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
        Tests that the Post request with the given path and data redirects to
        the content page of the newly created Content

        :param path: The path used for the POST request
        :type path: str
        :param data: The data of the content to be created used for the post
        request
        :type data: dict
        """
        response = self.client.post(path, data)
        self.assertEqual(response.status_code, 302)
        response_path = reverse('frontend:content', kwargs={
            'course_id': 1, 'topic_id': 1, 'pk': 1
        })
        self.assertEqual(response.url, response_path)

    def test_add_textfield(self):
        """Test add TextField

        Tests that a Textfield gets created and saved properly after sending a POST request
        to content-add and that the POST request redirects to the content page.
        """
        path = reverse('frontend:content-add', kwargs={
            'course_id': 1, 'topic_id': 1, 'type': 'Textfield'
        })
        data = {
            'language': 'de',
            'textfield': 'Lorem ipsum',
            'source': 'src',
            'form-TOTAL_FORMS': '0',
            'form-INITIAL_FORMS': '0'
        }
        self.post_redirects_to_content(path, data)
        self.assertEqual(model.TextField.objects.count(), 1)
        content = model.TextField.objects.first()
        self.assertEqual(content.textfield, "Lorem ipsum")

    def test_add_latex(self):
        """Test add Latex

        Tests that a Latex Content gets created and saved properly after sending a POST
        request to content-add and that the POST request redirects to the content page.
        """
        path = reverse('frontend:content-add', kwargs={
            'course_id': 1, 'topic_id': 1, 'type': 'Latex'
        })
        data = {
            'language': 'de',
            'textfield': '\\textbf{Test}',
            'source': 'src',
            'form-TOTAL_FORMS': '0',
            'form-INITIAL_FORMS': '0'
        }
        self.post_redirects_to_content(path, data)
        self.assertEqual(model.Latex.objects.count(), 1)
        content = model.Latex.objects.first()
        self.assertEqual(content.textfield, '\\textbf{Test}')
        self.assertTrue(bool(content.pdf))

    def test_attachments(self):
        """Test add Latex

        Tests that Image Attachments get created and saved properly after sending a POST
        request to content-add and that the POST request redirects to the content page.
        """
        path = reverse('frontend:content-add', kwargs={
            'course_id': 1, 'topic_id': 1, 'type': 'Textfield'
        })
        img0 = generate_image_file(0)
        img1 = generate_image_file(1)
        data = {
            'language': 'de',
            'textfield': 'Lorem ipsum',
            'source': 'src',
            'form-0-source': 'src 0',
            'form-0-image': img0,
            'form-1-source': 'src 1',
            'form-1-image': img1,
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0'
        }
        self.post_redirects_to_content(path, data)
        self.assertEqual(model.TextField.objects.count(), 1)
        text = model.TextField.objects.get(pk=1)
        self.assertEqual(text.textfield, "Lorem ipsum")
        self.assertEqual(model.SingleImageAttachment.objects.count(), 2)
        content = Content.objects.first()
        self.assertEqual(content.attachment.images.count(), 2)
        for image_attachment in content.attachment.images.all():
            self.assertTrue(bool(image_attachment.image))
