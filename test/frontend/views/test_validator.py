"""Purpose of this file

This file contains the test cases for this /frontend/views/validator.py.
"""
import test.utils as utils
# pylint: disable=imported-auth-user)
from django.contrib.auth.models import User
from django.test import TestCase

from base.models import Topic, Content

import content.models as model
import content.forms as form

from frontend.views.validator import Validator


class ValidatorTestCase(TestCase):
    """Validator test case

    Defines the test cases for the validators.
    """

    def setUp(self):
        """Setup

        Sets up the test database.
        """
        utils.setup_database()

    def test_valid(self):
        """LaTeX test case - valid

        Tests that the function validate_latex compiles the latex code and saves the pdf in
        the database.
        """
        user = User.objects.first()
        topic = Topic.objects.first()
        content = Content.objects.create(author=user.profile, topic=topic, type=model.Latex.TYPE,
                                         description='this is a description')
        latex_code = form.get_placeholder(model.Latex.TYPE, 'textfield')
        latex = model.Latex.objects.create(textfield=latex_code, content=content)

        self.assertFalse(bool(latex.pdf))
        Validator.validate_latex(user, content, latex)
        self.assertTrue((bool(latex.pdf)))
