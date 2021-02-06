"""Purpose of this file

This file contains the test cases for /frontend/views/content.py
"""
from django.test import TestCase

from django.contrib.auth.models import User
from base.models.content import Topic, Content
from content import models as model
from content import forms as form
from content.forms import SingleImageFormSet
from frontend.views.content import validate_latex, clean_attachment
from utility import test_utility


class ContentViewTest(TestCase):
    def setUp(self):
        """
        Sets up the test database
        """
        test_utility.setup_database()

    def test_validate_latex(self):
        user = User.objects.first()
        topic = Topic.objects.first()
        content = Content.objects.create(author=user.profile, topic=topic, type=model.Latex.TYPE,
                                         description='this is a descrieption')
        latex_code = form.get_placeholder(model.Latex.TYPE, 'textfield')
        latex = model.Latex.objects.create(textfield=latex_code, content=content)

        self.assertFalse(bool(latex.pdf))
        validate_latex(user, content, latex, topic.pk)
        self.assertTrue((bool(latex.pdf)))

    def test_clean_attachments(self):
        attachment = test_utility.generate_attachment(2)
        self.assertEqual(attachment.images.count(), 2)

        formset = SingleImageFormSet(queryset=model.SingleImageAttachment.objects.none())
        clean_attachment(attachment, formset)
        self.assertEqual(attachment.images.count(), 0)
        self.assertEqual(model.SingleImageAttachment.objects.count(), 0)
