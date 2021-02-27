"""Purpose of this file

This files is used as a collection utility operation for testing purpose.
"""

import tempfile
import io

from PIL import Image

from django.core.files.images import ImageFile

from django.contrib.auth.models import User  # pylint: disable=imported-auth-user

from base.models.content import Category, Topic, Content, Course

import content.forms as form
import content.models as model
from content.attachment.models import ImageAttachment

from frontend.views.validator import Validator

# Temporary media directory
MEDIA_ROOT = tempfile.mkdtemp()


def generate_image_file(image_file_number):
    """ Generate image file
    Generates an image file which can be uses for testing

    :param image_file_number: The number of the image file to be generated.
    :type image_file_number: int

    :return: the generated image file
    :rtype: ImageFile
    """
    # https://gist.github.com/guillaumepiot/817a70706587da3bd862835c59ef584e

    file = io.BytesIO()
    image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
    image.save(file, 'png')
    file.name = f'test{image_file_number}.png'
    file.seek(0)
    return ImageFile(file)


def generate_attachment(content, image_count):
    """ Generate an Image Attachment.

    Generates an image attachment with the given number of images which can be used for testing.
    :param content: The content to which the images get attached
    :type content: Content
    :param image_count: The number of the images to be generated in the attachment
    :type image_count: int
    """
    for i in range(image_count):
        image = generate_image_file(i)
        ImageAttachment.objects.create(content=content, image=image)


def setup_database():
    """Setup database

    Sets up the database to be used for testing which contains a latex content.
    """
    user = User.objects.create()
    cat = Category.objects.create(title="Category")
    Course.objects.create(title='Course', description='desc', category=cat)
    Topic.objects.create(title="Topic", category=cat)
    content = create_content(model.Latex.TYPE)
    content.save()
    latex_code = form.get_placeholder(model.Latex.TYPE, 'textfield')
    latex = model.Latex.objects.create(textfield=latex_code, content=content)
    Validator.validate_latex(user, content, latex)


def create_content(content_type):
    """Create content

    :param content_type: The type of the content
    :type content_type: str

    Create a dummy content with the given content type.

    :return: the created content
    :rtype: Content
    """
    return Content.objects.create(author=User.objects.first().profile,
                                  topic=Topic.objects.first(),
                                  type=content_type,
                                  description='this is a description',
                                  language='de')
