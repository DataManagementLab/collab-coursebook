"""Purpose of this file

This file describes the validators needed for the models.
"""
import os
import re
import magic

from django.core.exceptions import ValidationError


class Validator:  # pylint: disable=too-few-public-methods)
    """Validator

    Handles all validation related operation related to models.
    """

    @staticmethod
    def validate_pdf(file):
        """Validate PDF

        Validates if the given file is a valid PDF.

        :param file: The file that should be checked
        :type file: file

        :return: a validation error, if the file is not a valid pdf
        :rtype: None or ValidationError

        """
        valid_types = ['application/pdf']
        file_type = magic.from_buffer(file.read(1024), mime=True)
        if file_type not in valid_types:
            raise ValidationError('Unsupported file type.')
        valid_file_extensions = ['.pdf']
        ext = os.path.splitext(file.name)[1]
        if ext.lower() not in valid_file_extensions:
            raise ValidationError('Unacceptable file extension.')

    @staticmethod
    def validate_youtube_url(url):
        """Validate YouTube url

        Validates if the given url is a valid YouTube url.

        :param url: The url to be checked
        :param url: str

        :return: a validation error if the given url is not a valid YouTube link
        :rtype: None or ValidationError
        """
        valid_url = re.match(r"^(http(s)?://)?(www\.|m\.)?youtu(\.?)be(\.com)?/.*", url)
        if valid_url is None:
            raise ValidationError('Invalid URL')
