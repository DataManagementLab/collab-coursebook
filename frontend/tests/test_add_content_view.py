"""Purpose of this file

This file contains the test cases for /frontend/forms/content.py - AddContentView.
"""

import shutil

from django.test import TestCase, override_settings
# pylint: disable=imported-auth-user
from django.contrib.auth.models import User
from django.urls import reverse

from base.models import Content

from content.models import TextField, Latex, SingleImageAttachment

from utils import test_utils
from utils.test_utils import MEDIA_ROOT


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class AddContentViewTestCase(TestCase):
    """Add content test case

    Defines the test cases for the add content view.
    """

    def setUp(self):
        """Setup

        Sets up the test database.
        """
        test_utils.setup_database()
        self.client.force_login(User.objects.get(pk=1))

    @classmethod
    def tearDownClass(cls):
        """Teat down class

        Deletes the generated files after running the utility.
        """
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def post_redirects_to_content(self, path, data):
        """Post redirection to content

        Tests that the Post request with the given path and data redirects to
        the content page of the newly created Content.

        :param path: The path used for the POST request
        :type path: str
        :param data: The data of the content to be created used for the post request
        :type data: dict
        """
        response = self.client.post(path, data)
        self.assertEqual(response.status_code, 302)
        response_path = reverse('frontend:content', kwargs={
            'course_id': 1, 'topic_id': 1, 'pk': 2
        })
        self.assertEqual(response.url, response_path)

    def test_add_textfield(self):
        """Test add TextField

        Tests that a Textfield gets created and saved properly after sending
        a POST request to content-add and that the POST request redirects to
        the content page.
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
        self.assertEqual(TextField.objects.count(), 1)
        content = TextField.objects.first()
        self.assertEqual(content.textfield, "Lorem ipsum")

    def test_add_latex(self):
        """Test add Latex

        Tests that a Latex Content gets created and saved properly after sending
        a POST request to content-add and that the POST request redirects to the
        content page.
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
        self.assertEqual(Latex.objects.count(), 2)
        content = Latex.objects.get(pk=2)
        self.assertEqual(content.textfield, '\\textbf{Test}')
        self.assertTrue(bool(content.pdf))

    def test_add_attachments(self):
        """Test add Latex

        Tests that Image Attachments get created and saved properly after sending
        a POST request to content-add and that the POST request redirects to
        the content page.
        """
        path = reverse('frontend:content-add', kwargs={
            'course_id': 1, 'topic_id': 1, 'type': 'Textfield'
        })
        img0 = test_utils.generate_image_file(0)
        img1 = test_utils.generate_image_file(1)
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
        self.assertEqual(TextField.objects.count(), 1)
        text = TextField.objects.first()
        self.assertEqual(text.textfield, "Lorem ipsum")
        self.assertEqual(SingleImageAttachment.objects.count(), 2)
        content = Content.objects.get(pk=text.content_id)
        self.assertEqual(content.attachment.images.count(), 2)
        for image_attachment in content.attachment.images.all():
            self.assertTrue(bool(image_attachment.image))
