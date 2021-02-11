"""Validator

Represents the validators for the models fields.
"""
import os
import magic
from django.core.exceptions import ValidationError


def validate_pdf(file):
    """Validate PDF

    Validates if the given file is a valid PDF.

    :param file: The file that should be checked
    :type file: file

    :return: an validation error, if it's not a valid pdf
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
