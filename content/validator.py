import os
import magic
from django.core.exceptions import ValidationError


# TODO dokumentation
def validate_is_pdf(file):
    valid_types = ['application/pdf']
    file_type = magic.from_buffer(file.read(1024), mime=True)
    if file_type not in valid_types:
        raise ValidationError('Unsupported file type.')
    valid_file_extensions = ['.pdf']
    ext = os.path.splitext(file.name)[1]
    if ext.lower() not in valid_file_extensions:
        raise ValidationError('Unacceptable file extension.')

