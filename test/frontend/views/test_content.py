"""Purpose of this file

This file contains the test cases for /frontend/forms/content.py.
"""


from test import utils
from test.test_cases import MediaTestCase

from unittest import skip

from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from base.models import Content, Course

import content.forms as form
import content.models as model
from content.attachment.forms import ImageAttachmentFormSet
from content.attachment.models import ImageAttachment

from frontend.forms import AddContentForm
from frontend.views.content import clean_attachment


class CleanAttachmentTestCase(TestCase):
    """Clean attachment test case

    Defines the test cases for the function clean_attachment.
    """

    def setUp(self):
        """Setup

        Sets up the test database.
        """
        utils.setup_database()

    def test_successful(self):
        """Test successful

        Tests that clean_attachments removes the attachments from the database.
        """
        content = Content.objects.first()
        utils.generate_attachment(content, 2)
        self.assertEqual(content.ImageAttachments.count(), 2)

        formset = ImageAttachmentFormSet(queryset=ImageAttachment.objects.none())
        clean_attachment(content, formset)
        self.assertEqual(content.ImageAttachments.count(), 0)
        self.assertEqual(ImageAttachment.objects.count(), 0)


class AddContentViewTestCase(MediaTestCase):
    """Add content test case

    Defines the test cases for the add content view.
    """

    def post_redirects_to_content(self, path, data):
        """POST redirection to content

        Tests the function post that the POST request with the given path and data redirects to
        the content page of the newly created Content.

        :param path: The path used for the POST request
        :type path: str
        :param data: The data of the content to be created used for the post request
        :type data: dict
        """
        response = self.client.post(path, data)
        self.assertEqual(response.status_code, 302)
        response_path = reverse('frontend:content', kwargs={
            'course_id': 1, 'topic_id': 1, 'pk': 2
        })
        self.assertEqual(response.url, response_path)

    def test_add_md_text(self):
        """POST test case - add Markdown

        Tests the function post that a Markdown content gets created by text and saved properly
        after sending a POST request to content-add
        and that the POST request redirects to the content page.
        """
        path = reverse('frontend:content-add', kwargs={
            'course_id': 1, 'topic_id': 1, 'type': 'MD'
        })
        data = {
            'options': 'text',
            'language': 'de',
            'source': 'src',
            'form-TOTAL_FORMS': '0',
            'form-INITIAL_FORMS': '0',
            'textfield': 'test text'
        }
        self.post_redirects_to_content(path, data)
        self.assertEqual(model.MDContent.objects.count(), 1)
        content = model.MDContent.objects.first()
        self.assertTrue(bool(content.md))
        self.assertEqual(content.source, "src")
        self.assertEqual(content.textfield, "test text")
        self.assertEqual(content.textfield,content.md.open().read().decode('utf-8'))

    def test_add_md_file(self):
        """POST test case - add Markdown

        Tests the function post that a Markdown content gets created by file and saved properly
        after sending
        a POST request to content-add and that the POST request redirects to
        the content page.
        """
        path = reverse('frontend:content-add', kwargs={
            'course_id': 1, 'topic_id': 1, 'type': 'MD'
        })
        test_file = SimpleUploadedFile("test_file.md",b"test text")
        data = {
            'options': 'file',
            'language': 'de',
            'source': 'src',
            'form-TOTAL_FORMS': '0',
            'form-INITIAL_FORMS': '0',
            'md': test_file,
        }
        self.post_redirects_to_content(path, data)
        self.assertEqual(model.MDContent.objects.count(), 1)
        content = model.MDContent.objects.first()
        self.assertTrue(bool(content.md))
        self.assertTrue(content.md.name,"test_file")
        self.assertEqual(content.source, "src")
        self.assertEqual(content.textfield, "test text")
        self.assertEqual(content.textfield,content.md.open().read().decode('utf-8'))

    def test_add_md_file_options(self):
        """POST test case - add Markdown

        Tests the function post that:
        a Markdown content gets created by file when both file and text are inputted
        and the option "Upload by file" is chosen.
        The content should then be saved properly after sending a POST request to content-add
        and that the POST request redirects to the content page.
        """
        path = reverse('frontend:content-add', kwargs={
            'course_id': 1, 'topic_id': 1, 'type': 'MD'
        })
        test_file = SimpleUploadedFile("test_file.md",b"AB")
        data = {
            'options': 'file',
            'language': 'de',
            'source': 'src',
            'form-TOTAL_FORMS': '0',
            'form-INITIAL_FORMS': '0',
            'md': test_file,
            'textfield': 'B'
        }
        self.post_redirects_to_content(path, data)
        self.assertEqual(model.MDContent.objects.count(), 1)
        content = model.MDContent.objects.first()
        self.assertTrue(bool(content.md))
        self.assertTrue(content.md.name,"test_file")
        self.assertEqual(content.source, "src")
        self.assertEqual(content.textfield, "AB")
        self.assertEqual(content.textfield,content.md.open().read().decode('utf-8'))

    def test_add_md_text_options(self):
        """POST test case - add Markdown

        Tests the function post that:
        a Markdown content gets created by text when both file and text are inputted
        and the option "Upload by text" is chosen.
        The content should then be saved properly after sending a POST request to content-add
        and that the POST request redirects to the content page.
        """
        path = reverse('frontend:content-add', kwargs={
            'course_id': 1, 'topic_id': 1, 'type': 'MD'
        })
        test_file = SimpleUploadedFile("test_file.md", b"AB")
        data = {
            'options': 'text',
            'language': 'de',
            'source': 'src',
            'form-TOTAL_FORMS': '0',
            'form-INITIAL_FORMS': '0',
            'md': test_file,
            'textfield': 'B'
        }
        self.post_redirects_to_content(path, data)
        self.assertEqual(model.MDContent.objects.count(), 1)
        content = model.MDContent.objects.first()
        self.assertTrue(bool(content.md))
        self.assertEqual(content.source, "src")
        self.assertEqual(content.textfield, "B")
        self.assertEqual(content.textfield, content.md.open().read().decode('utf-8'))

    def test_add_textfield(self):
        """POST test case - add TextField

        Tests the function post that a Textfield gets created and saved properly after sending
        a POST request to content-add and that the POST request redirects to
        the content page.
        """
        path = reverse('frontend:content-add', kwargs={
            'course_id': 1, 'topic_id': 1, 'type': 'Textfield'
        })
        data = {
            'language': 'de',
            'textfield': 'Lorem ipsum',
            'source': 'src',
            'form-TOTAL_FORMS': '0',
            'form-INITIAL_FORMS': '0'
        }
        self.post_redirects_to_content(path, data)
        self.assertEqual(model.TextField.objects.count(), 1)
        content = model.TextField.objects.first()
        self.assertEqual(content.textfield, "Lorem ipsum")

    @skip('Need Youtube API Key')
    def test_add_yt(self):
        """POST test case - add YouTube Video

        Tests the function post that a YouTube Video without timestamps gets created
        and saved properly after sending a POST request to content-add
        and that the POST request redirects to the content page.
        """
        path = reverse('frontend:content-add', kwargs={
            'course_id': 1, 'topic_id': 1, 'type': 'YouTubeVideo'
        })
        data = {
            'language': 'de',
            'url': 'https://www.youtube.com/watch?v=9xwazD5SyVg',
            'start_time': '0:00',
            'end_time': '0:00',
            'form-TOTAL_FORMS': '0',
            'form-INITIAL_FORMS': '0'
        }
        self.post_redirects_to_content(path, data)
        self.assertEqual(model.YTVideoContent.objects.count(), 1)
        content = model.YTVideoContent.objects.first()
        self.assertEqual(content.url, "https://www.youtube.com/watch?v=9xwazD5SyVg")

    @skip('Need Youtube API Key')
    def test_add_yt_correct_times(self):
        """POST test case - add YouTube Video

        Tests the function post that a YouTube Video with correct timestamps gets created
        and saved properly after sending a POST request to content-add
        and that the POST request redirects to the content page.

        """
        path = reverse('frontend:content-add', kwargs={
            'course_id': 1, 'topic_id': 1, 'type': 'YouTubeVideo'
        })
        data = {
            'language': 'de',
            'url': 'https://www.youtube.com/watch?v=9xwazD5SyVg',
            'start_time': '0:01',
            'end_time': '0:05',
            'form-TOTAL_FORMS': '0',
            'form-INITIAL_FORMS': '0'
        }
        self.post_redirects_to_content(path, data)
        self.assertEqual(model.YTVideoContent.objects.count(), 1)
        content = model.YTVideoContent.objects.first()
        self.assertEqual(content.url, "https://www.youtube.com/watch?v=9xwazD5SyVg")
        self.assertEqual(content.start_time, "0:01")
        self.assertEqual(content.end_time, "0:05")

    @skip('Need Youtube API Key')
    def test_add_yt_wrong_times(self):
        """POST test case - add YouTube Video

        Tests the function post that a YouTube Video with correct timestamps gets created
        and saved properly after sending
        a POST request to content-add and that the POST request redirects to
        the content page.
        """
        path = reverse('frontend:content-add', kwargs={
            'course_id': 1, 'topic_id': 1, 'type': 'YouTubeVideo'
        })
        data = {
            'language': 'de',
            'url': 'https://www.youtube.com/watch?v=9xwazD5SyVg',
            'start_time': '0:05',
            'end_time': '0:01',
            'form-TOTAL_FORMS': '0',
            'form-INITIAL_FORMS': '0'
        }
        response = self.client.post(path, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(model.YTVideoContent.objects.count(), 0)

    @skip('Need Youtube API Key')
    def test_add_yt_equal_times(self):
        """POST test case - add YouTube Video

        Tests the function post that a YouTube Video with correct timestamps gets created
        saved properly after sending
        a POST request to content-add and that the POST request redirects to
        the content page.
        """
        path = reverse('frontend:content-add', kwargs={
            'course_id': 1, 'topic_id': 1, 'type': 'YouTubeVideo'
        })
        data = {
            'language': 'de',
            'url': 'https://www.youtube.com/watch?v=9xwazD5SyVg',
            'start_time': '0:05',
            'end_time': '0:05',
            'form-TOTAL_FORMS': '0',
            'form-INITIAL_FORMS': '0'
        }
        response = self.client.post(path, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(model.YTVideoContent.objects.count(), 0)

    @skip('Need Youtube API Key')
    def test_add_yt_times_longer_than_video(self):
        """POST test case - add YouTube Video

        Tests the function post that a YouTube Video with correct timestamps gets created
        and saved properly after sending
        a POST request to content-add and that the POST request redirects to
        the content page.
        """
        path = reverse('frontend:content-add', kwargs={
            'course_id': 1, 'topic_id': 1, 'type': 'YouTubeVideo'
        })
        data = {
            'language': 'de',
            'url': 'https://www.youtube.com/watch?v=9xwazD5SyVg',
            'start_time': '0:07',
            'end_time': '0:20',
            'form-TOTAL_FORMS': '0',
            'form-INITIAL_FORMS': '0'
        }
        response = self.client.post(path, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(model.YTVideoContent.objects.count(), 0)

    @skip('Need Youtube API Key')
    def test_add_yt_wrong_timestamps(self):
        """POST test case - add YouTube Video

        Tests the function post that a YouTube Video with correct timestamps gets created
        and saved properly after sending
        a POST request to content-add and that the POST request redirects to
        the content page.
        """
        path = reverse('frontend:content-add', kwargs={
            'course_id': 1, 'topic_id': 1, 'type': 'YouTubeVideo'
        })
        data = {
            'language': 'de',
            'url': 'https://www.youtube.com/watch?v=9xwazD5SyVg',
            'start_time': '0:7',
            'end_time': '0:00',
            'form-TOTAL_FORMS': '0',
            'form-INITIAL_FORMS': '0'
        }
        response = self.client.post(path, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(model.YTVideoContent.objects.count(), 0)

        data['start_time'] = "13:00:10"
        response = self.client.post(path, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(model.YTVideoContent.objects.count(), 0)

        data['start_time'] = "10"
        response = self.client.post(path, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(model.YTVideoContent.objects.count(), 0)

        data['start_time'] = "0h0m0s"
        response = self.client.post(path, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(model.YTVideoContent.objects.count(), 0)

    def test_add_latex(self):
        """POST test case -  add LaTeX

        Tests the function post that a LaTeX Content gets created and saved properly after sending
        a POST request to content-add and that the POST request redirects to the
        content page.
        """
        path = reverse('frontend:content-add', kwargs={
            'course_id': 1, 'topic_id': 1, 'type': 'Latex'
        })
        data = {
            'language': 'de',
            'textfield': '\\textbf{Test}',
            'source': 'src',
            'form-TOTAL_FORMS': '0',
            'form-INITIAL_FORMS': '0'
        }
        self.post_redirects_to_content(path, data)
        self.assertEqual(model.Latex.objects.count(), 2)
        content = model.Latex.objects.get(pk=2)
        self.assertEqual(content.textfield, '\\textbf{Test}')
        self.assertTrue(bool(content.pdf))

    def test_latex_preview_success(self):
        """POST test case - LaTeX preview - success

        Tests that the POST preview request is sent and processed correctly, returning
        an appropriating response indicating that the request was successful.
        """
        path = reverse('frontend:content-add', kwargs={
            'course_id': 1, 'topic_id': 1, 'type': 'Latex'
        })
        old_objects_count = model.Latex.objects.count()
        old_attachments_count = ImageAttachment.objects.count()
        data = {
            'textfield': 'Lorem ipsum',
            'form-TOTAL_FORMS': '0',
            'form-INITIAL_FORMS': '0',
            'form-0-image': utils.generate_image_file(0),
            'latex-preview': True,
        }
        # Last parameter is used to make the request an ajax request
        response = self.client.post(path, data, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.reason_phrase, 'OK')
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertEqual(model.Latex.objects.count(), old_objects_count)
        self.assertEqual(ImageAttachment.objects.count(), old_attachments_count)

    def test_latex_preview_invalid_request(self):
        """POST test case LaTeX preview - failure

         Tests that the POST preview request is sent and rejected because the request was
         invalid, returning an appropriating response with the corresponding
         reason.
         """
        path = reverse('frontend:content-add', kwargs={
            'course_id': 1, 'topic_id': 1, 'type': 'Latex'
        })
        old_objects_count = model.Latex.objects.count()
        old_attachments_count = ImageAttachment.objects.count()
        data = {
            'form-TOTAL_FORMS': '0',
            'form-INITIAL_FORMS': '0',
            'latex-preview': True,
        }
        # Last parameter is used to make the request an ajax request
        response = self.client.post(path, data, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.reason_phrase, 'Invalid data')
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')
        self.assertEqual(model.Latex.objects.count(), old_objects_count)
        self.assertEqual(ImageAttachment.objects.count(), old_attachments_count)

    def test_latex_preview_fail_text(self):
        """POST test case LaTeX preview - failure

        Tests that the POST preview request is sent and rejected because no LaTeX code
        was sent in the request, returning an appropriating response with the corresponding
        reason.
        """
        path = reverse('frontend:content-add', kwargs={
            'course_id': 1, 'topic_id': 1, 'type': 'Latex'
        })
        old_objects_count = model.Latex.objects.count()
        old_attachments_count = ImageAttachment.objects.count()
        data = {
            'textfield': '',
            'form-TOTAL_FORMS': '0',
            'form-INITIAL_FORMS': '0',
            'latex-preview': True,
        }
        # Last parameter is used to make the request an ajax request
        response = self.client.post(path, data, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.reason_phrase, 'Textfield is empty')
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')
        self.assertEqual(model.Latex.objects.count(), old_objects_count)
        self.assertEqual(ImageAttachment.objects.count(), old_attachments_count)

    def test_latex_preview_fail_invalid_attachments(self):
        """POST test case LaTeX preview - failure

        Tests that the POST preview request is sent and rejected
        because of one of the following reasons:
        1. At least one of the attachments is not an image
        2. At least one of the attachments was empty
        An appropriating response with the corresponding reason message will then be sent back.
        """
        path = reverse('frontend:content-add', kwargs={
            'course_id': 1, 'topic_id': 1, 'type': 'Latex'
        })
        old_objects_count = model.Latex.objects.count()
        old_attachments_count = ImageAttachment.objects.count()
        test_file = SimpleUploadedFile("test_file.md", b"A")
        datas = [{
            'textfield': 'Test invalid image extension',
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-0-image': test_file,
            'latex-preview': True,
        }, {
            'textfield': 'Test empty form in formset',
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'latex-preview': True,
        }]
        # Last parameter is used to make the request an ajax request
        for data in datas:
            response = self.client.post(path,
                                        data,
                                        **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.reason_phrase, 'Invalid attachment data')
            self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')
            self.assertEqual(model.Latex.objects.count(), old_objects_count)
            self.assertEqual(ImageAttachment.objects.count(), old_attachments_count)

    def test_add_attachments(self):
        """POST test case - add attachments

        Tests the function post that Image Attachments get created and saved properly after sending
        a POST request to content-add and that the POST request redirects to
        the content page.
        """
        path = reverse('frontend:content-add', kwargs={
            'course_id': 1, 'topic_id': 1, 'type': 'Textfield'
        })
        img0 = utils.generate_image_file(0)
        img1 = utils.generate_image_file(1)
        data = {
            'language': 'de',
            'textfield': 'Lorem ipsum',
            'source': 'src',
            'form-0-source': 'src 0',
            'form-0-image': img0,
            'form-1-source': 'src 1',
            'form-1-image': img1,
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0'
        }
        self.post_redirects_to_content(path, data)
        self.assertEqual(model.TextField.objects.count(), 1)
        text = model.TextField.objects.first()
        self.assertEqual(text.textfield, "Lorem ipsum")
        self.assertEqual(ImageAttachment.objects.count(), 2)
        content = model.Content.objects.get(pk=text.content_id)
        self.assertEqual(content.ImageAttachments.count(), 2)
        for image_attachment in content.ImageAttachments.all():
            self.assertTrue(bool(image_attachment.image))

    def test_add_empty_attachment(self):
        """POST test case - add empty attachment

        Tests the function post that an empty image attachment does not get added.
        """
        path = reverse('frontend:content-add', kwargs={
            'course_id': 1, 'topic_id': 1, 'type': 'Textfield'
        })
        data = {
            'language': 'de',
            'textfield': 'Lorem ipsum',
            'source': 'src',
            'form-0-source': '',
            'form-0-image': '',
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0'
        }
        response = self.client.post(path, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(model.TextField.objects.count(), 0)
        self.assertEqual(ImageAttachment.objects.count(), 0)

    def test_get(self):
        """GET test case

        Tests the function get_context_data that the context for content-add is set properly.
        """
        path = reverse('frontend:content-add', kwargs={
            'course_id': 1, 'topic_id': 1, 'type': 'Textfield'
        })
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        context = response.context_data
        self.assertEqual(type(context['form']), AddContentForm)
        self.assertEqual(context['course'], Course.objects.first())
        self.assertEqual(context['content_type_form'], form.AddTextField)
        self.assertTrue(context['attachment_allowed'])
        self.assertTrue('item_forms' in context)


class DeleteContentViewTestCase(MediaTestCase):
    """Delete content test case

    Defines the test cases for the delete content view.
    """

    def test_delete_textfield_attachments(self):
        """POST test case - delete textfield with attachments

        Tests the function post that a TextField with Image Attachments gets deleted properly
        after sending a POST request to content-delete.
        """
        content = utils.create_content(model.TextField.TYPE)
        utils.generate_attachment(content, 2)
        content.save()
        model.TextField.objects.create(textfield='Lorem Ipsum', content=content)
        self.assertEqual(Content.objects.count(), 2)
        self.assertEqual(model.TextField.objects.count(), 1)
        self.assertEqual(ImageAttachment.objects.count(), 2)
        path = reverse('frontend:content-delete', kwargs={
            'course_id': 1, 'topic_id': 1, 'pk': 2
        })
        self.client.post(path)
        self.assertEqual(Content.objects.count(), 1)
        self.assertEqual(model.TextField.objects.count(), 0)
        self.assertEqual(ImageAttachment.objects.count(), 0)

    def test_latex(self):
        """POST test case - delete latex

        Tests the function post that a LaTeX content gets deleted properly after sending
        a POST request to content-delete.
        """
        self.assertEqual(Content.objects.count(), 1)
        self.assertEqual(model.Latex.objects.count(), 1)
        path = reverse('frontend:content-delete', kwargs={
            'course_id': 1, 'topic_id': 1, 'pk': 1
        })
        self.client.post(path)
        self.assertEqual(Content.objects.count(), 0)
        self.assertEqual(model.Latex.objects.count(), 0)


class EditContentViewTestCase(MediaTestCase):
    """Edit content test case

    Defines the test cases for the edit content view.
    """

    def test_latex(self):
        """POST test case -  edit LaTeX

        Tests the function post that a LaTeX Content gets edited and saved properly after sending
        a POST request to content-edit and that the POST request redirects to the content page.
        """
        data = {
            'change_log': 'stuff changed',
            'description': 'description',
            'language': 'en',
            'textfield': 'Lorem ipsum',
            'source': 'src 2',
            'form-TOTAL_FORMS': '0',
            'form-INITIAL_FORMS': '0'
        }
        path = reverse('frontend:content-edit', kwargs={
            'course_id': 1, 'topic_id': 1, 'pk': 1
        })
        response = self.client.post(path, data)

        self.assertEqual(response.url, reverse('frontend:content', kwargs={
            'course_id': 1, 'topic_id': 1, 'pk': 1
        }))
        self.assertEqual(Content.objects.first().language, 'en')
        self.assertEqual(model.Latex.objects.first().source, 'src 2')
        self.assertEqual(model.Latex.objects.first().textfield, 'Lorem ipsum')

    def test_textfield_attachments(self):
        """POST test case -  edit textfield with attachments

        Tests the function post that a textfield with attachments gets edited and saved properly
        after sending a POST request to content-edit and that the POST request redirects to the
        content page.
        """
        content = utils.create_content(model.TextField.TYPE)
        utils.generate_attachment(content, 2)
        content.save()
        model.TextField.objects.create(textfield='Text', source='src', content=content)

        data = {
            'change_log': 'stuff changed',
            'language': 'de',
            'description': 'description',
            'textfield': 'Lorem ipsum',
            'source': 'src text',
            'form-0-id': '1',
            'form-0-source': 'src 0',
            'form-0-image': utils.generate_image_file(42),
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '2'
        }
        path = reverse('frontend:content-edit', kwargs={
            'course_id': 1, 'topic_id': 1, 'pk': 2
        })
        response = self.client.post(path, data)

        self.assertEqual(response.url, reverse('frontend:content', kwargs={
            'course_id': 1, 'topic_id': 1, 'pk': 2
        }))
        content = Content.objects.get(pk=2)
        self.assertEqual(content.language, 'de')
        textfield = model.TextField.objects.first()
        self.assertEqual(textfield.source, 'src text')
        self.assertEqual(textfield.textfield, 'Lorem ipsum')
        self.assertEqual(content.ImageAttachments.count(), 1)
        self.assertEqual(ImageAttachment.objects.count(), 1)
        image = ImageAttachment.objects.first().image
        self.assertIn('test42', image.name)

    def test_context(self):
        """Get context data test case

        Tests the function get_context_data that the context for content-edit is set properly.
        """
        path = reverse('frontend:content-edit', kwargs={
            'course_id': 1, 'topic_id': 1, 'pk': 1
        })
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        context = response.context_data
        self.assertEqual(context['course_id'], 1)
        self.assertEqual(context['topic_id'], 1)
        self.assertEqual(type(context['content_type_form']), form.AddLatex)
        self.assertTrue(context['attachment_allowed'])
        self.assertTrue('item_forms' in context)

    def test_md(self):
        """POST test case -  edit MD

        Tests the function post that a MD Content gets edited and saved properly after sending
        a POST request to content-edit and that the POST request redirects to the content page.
        """
        content = utils.create_content(model.MDContent.TYPE)
        content.save()
        model.MDContent.objects.create(textfield='Markdown Script', source='src', content=content)

        data = {
            'change_log': 'stuff changed',
            'language': 'de',
            'description': 'description',
            'textfield': 'Lorem ipsum',
            'source': 'src text',
            'form-TOTAL_FORMS': '0',
            'form-INITIAL_FORMS': '0'
        }
        path = reverse('frontend:content-edit', kwargs={
            'course_id': 1, 'topic_id': 1, 'pk': 2
        })
        response = self.client.post(path, data)

        self.assertEqual(response.url, reverse('frontend:content', kwargs={
            'course_id': 1, 'topic_id': 1, 'pk': 2
        }))
        content = Content.objects.get(pk=2)
        self.assertEqual(content.language, 'de')
        md_content = model.MDContent.objects.first()
        self.assertEqual(md_content.source, 'src text')
        self.assertEqual(md_content.textfield, 'Lorem ipsum')
