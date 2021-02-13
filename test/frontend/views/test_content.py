"""Purpose of this file

This file contains the test cases for /frontend/forms/content.py.
"""
import test.utils as utils

# pylint: disable=imported-auth-user)
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

import content.forms as form
import content.models as model

from frontend.views.content import clean_attachment
from test.test_cases import MediaTestCase


class CleanAttachmentTestCase(TestCase):
    """Clean attachment test case

    Defines the test cases for the function clean_attachment.
    """

    def setUp(self):
        """Setup

        Sets up the test database.
        """
        utils.setup_database()

    def test_successful(self):
        """Test successful

        Tests that clean_attachments removes the attachments from the database.
        """
        attachment = utils.generate_attachment(2)
        self.assertEqual(attachment.images.count(), 2)

        formset = form.SingleImageFormSet(queryset=model.SingleImageAttachment.objects.none())
        clean_attachment(attachment, formset)
        self.assertEqual(attachment.images.count(), 0)
        self.assertEqual(model.SingleImageAttachment.objects.count(), 0)


class AddContentViewTestCase(MediaTestCase):
    """Add content test case

    Defines the test cases for the add content view.
    """

    def setUp(self):
        """Setup

        Sets up the test database.
        """
        super().setUp()
        self.client.force_login(User.objects.get(pk=1))

    def post_redirects_to_content(self, path, data):
        """POST redirection to content

        Tests the function post that the POST request with the given path and data redirects to
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
        """POST test case - add TextField

        Tests the function post that a Textfield gets created and saved properly after sending
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
        self.assertEqual(model.TextField.objects.count(), 1)
        content = model.TextField.objects.first()
        self.assertEqual(content.textfield, "Lorem ipsum")

    def test_add_latex(self):
        """POST test case -  add LaTeX

        Tests the function post that a LaTeX Content gets created and saved properly after sending
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
        self.assertEqual(model.Latex.objects.count(), 2)
        content = model.Latex.objects.get(pk=2)
        self.assertEqual(content.textfield, '\\textbf{Test}')
        self.assertTrue(bool(content.pdf))

    def test_add_attachments(self):
        """POST test case - add attachments

        Tests the function post that Image Attachments get created and saved properly after sending
        a POST request to content-add and that the POST request redirects to
        the content page.
        """
        path = reverse('frontend:content-add', kwargs={
            'course_id': 1, 'topic_id': 1, 'type': 'Textfield'
        })
        img0 = utils.generate_image_file(0)
        img1 = utils.generate_image_file(1)
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
        text = model.TextField.objects.first()
        self.assertEqual(text.textfield, "Lorem ipsum")
        self.assertEqual(model.SingleImageAttachment.objects.count(), 2)
        content = model.Content.objects.get(pk=text.content_id)
        self.assertEqual(content.attachment.images.count(), 2)
        for image_attachment in content.attachment.images.all():
            self.assertTrue(bool(image_attachment.image))
