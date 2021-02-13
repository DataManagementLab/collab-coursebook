"""Purpose of this file

This file contains the test cases for /frontend/views/content.py
"""

from django.test import TestCase
# pylint: disable=imported-auth-user
from django.contrib.auth.models import User

from base.models.content import Topic, Content

from content import models as model
from content import forms as form

from content.forms import SingleImageFormSet

from frontend.views.content import clean_attachment
from frontend.views.validator import Validator

from utils import test_utility


class ContentViewTest(TestCase):
    """Content view test case

    Defines the test cases for the content view.
    """

    def setUp(self):
        """Setup

        Sets up the test database.
        """
        test_utility.setup_database()

    def test_validate_latex(self):
        """Test validate_latex

        Tests that validate_latex compiles the latex code and saves the pdf in the database.
        """
        user = User.objects.first()
        topic = Topic.objects.first()
        content = Content.objects.create(author=user.profile, topic=topic, type=model.Latex.TYPE,
                                         description='this is a descrieption')
        latex_code = form.get_placeholder(model.Latex.TYPE, 'textfield')
        latex = model.Latex.objects.create(textfield=latex_code, content=content)

        self.assertFalse(bool(latex.pdf))
        Validator.validate_latex(user, content, latex, topic.pk)
        self.assertTrue((bool(latex.pdf)))

    def test_clean_attachments(self):
        """Test clean_attachments

        Tests that clean_attachments removes the attachments from the database.
        """
        attachment = test_utility.generate_attachment(2)
        self.assertEqual(attachment.images.count(), 2)

        formset = SingleImageFormSet(queryset=model.SingleImageAttachment.objects.none())
        clean_attachment(attachment, formset)
        self.assertEqual(attachment.images.count(), 0)
        self.assertEqual(model.SingleImageAttachment.objects.count(), 0)
