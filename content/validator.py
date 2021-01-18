"""Validator

Represents the validators for the models fields.
"""
import os
import magic
from django.core.exceptions import ValidationError


def validate_is_pdf(file):
    """

    Validates the PDF upload if the the file is a valid PDF.

    Args:
        file (TODO): TODO

    Returns: TODO

    """
    valid_types = ['application/pdf']
    file_type = magic.from_buffer(file.read(1024), mime=True)
    if file_type not in valid_types:
        raise ValidationError('Unsupported file type.')
    valid_file_extensions = ['.pdf']
    ext = os.path.splitext(file.name)[1]
    if ext.lower() not in valid_file_extensions:
        raise ValidationError('Unacceptable file extension.')
