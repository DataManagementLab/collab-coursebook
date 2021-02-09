import tempfile
import io
from PIL import Image

from django.core.files.images import ImageFile
from django.contrib.auth.models import User

from base.models.content import Category, Topic, Content, Course
import content.forms as form
import content.models as model
from frontend.views.content import validate_latex

# Temporary media directory
MEDIA_ROOT = tempfile.mkdtemp()


def generate_image_file(image_file_number):
    """ Generate image file
    Generates an image file which can be uses for testing

    :param image_file_number: number of the image file to be generated
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


def generate_attachment(image_count):
    """ Generate an Image Attachment.

    Generates an image attachment with the given number of images which can be used for testing

    :param image_count: number of the images to be generated in the attachment
    :type image_count: int

    :return: the generated image file
    :rtype: ImageFile
    """
    attachment = model.ImageAttachment.objects.create()
    for i in range(image_count):
        image = generate_image_file(i)
        s = model.SingleImageAttachment.objects.create(image=image)
        attachment.images.add(s)
    attachment.save()
    return attachment


def setup_database():
    """ Sets up the database for Testing.

    Sets up the database to be used for testing which contains a latex content
    """
    user = User.objects.create()
    cat = Category.objects.create(title="Category")
    Course.objects.create(title='Course', description='desc', category=cat)
    topic = Topic.objects.create(title="Topic", category=cat)
    content = Content.objects.create(author=user.profile, topic=topic, type=model.Latex.TYPE,
                                     description='this is a descrieption')
    latex_code = form.get_placeholder(model.Latex.TYPE, 'textfield')
    latex = model.Latex.objects.create(textfield=latex_code, content=content)
    validate_latex(user, content, latex, topic_id=topic.pk)
