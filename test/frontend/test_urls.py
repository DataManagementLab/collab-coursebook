from django.test import SimpleTestCase

from frontend.urls import BooleanConverter


class BooleanConverterTestCase(SimpleTestCase):
    def setUp(self):
        self.converter = BooleanConverter()

    def test_to_python_true(self):
        value = self.converter.to_python("True")
        self.assertTrue(value)

    def test_to_python_false(self):
        value = self.converter.to_python("False")
        self.assertFalse(value)

    def test_to_python_mixed_case_true(self):
        value = self.converter.to_python("tRuE")
        self.assertTrue(value)

    def test_to_python_mixed_case_false(self):
        value = self.converter.to_python("fAlSe")
        self.assertFalse(value)

    def test_to_python_invalid_value(self):
        value = self.converter.to_python("invalid")
        self.assertFalse(value)

    def test_to_url_true(self):
        value = self.converter.to_url(True)
        self.assertEqual(value, "True")

    def test_to_url_false(self):
        value = self.converter.to_url(False)
        self.assertEqual(value, "False")