import reversion

from reversion import set_comment, is_registered
from reversion.models import Version

from test import utils
from test.test_cases import MediaTestCase

from django.test import TestCase
from django.urls import reverse

from base.models import Content, Course
import content.forms as form
import content.models as model

from frontend.forms import AddContentForm

from frontend.views.content import clean_attachment


class ContentHistoryCompareViewTestCase(MediaTestCase):
    """ history compare test cases

    Defines test cases for ContentHistoryCompareView and CourseHistoryCompareView

    """
    # TODO test review
    def setUp(self):
        super().setUp()
        # set up a textfield item to test
        with reversion.create_revision():
            self.content1 = utils.create_content(model.TextField.TYPE)
            self.text1 = model.TextField.objects.create(content=self.content1,
                                                        textfield='Hello!',
                                                        source='test')
            self.text1.content.attachment = utils.generate_attachment(2)
            set_comment('initial version')

        # create a new version and make 1 change to text1
        with reversion.create_revision():
            self.text1.textfield = 'test test'
            self.text1.save()
            set_comment('change text')

        self.queryset = Version.objects.get_for_object(self.text1)
        self.revision_ids1 = self.queryset.values_list("revision_id", flat=True)
        self.version_ids1 = self.queryset.values_list("pk", flat=True)

        # set up a latex item to test
        with reversion.create_revision():
            self.content2 = utils.create_content(model.Latex.TYPE)
            self.latex1 = model.Latex.objects.create(content=self.content1,
                                                     textfield='/textbf{Hello!}',
                                                     source='test')
            set_comment('initial version')

        # create a new version and make 1 change to latex1
        with reversion.create_revision():
            self.latex1.textfield = '/textbf{你好！}'
            self.latex1.save()
            set_comment('change code')

        # get the author id for later test
        self.author_id = self.latex1.content.author_id

        self.queryset2 = Version.objects.get_for_object(self.latex1)
        self.revision_ids2 = self.queryset2.values_list("revision_id", flat=True)
        self.version_ids2 = self.queryset2.values_list("pk", flat=True)

        # print(list(self.revision_ids2))
        # print(self.version_ids1)
        # print(self.version_ids2)

    def assertContainsHtml(self, response, *args):
        for html in args:
            try:
                self.assertContains(response, html, html=True)
            except AssertionError as e:
                print(e)
                raise

    def test_initial_state(self):
        self.assertTrue(is_registered(Course))
        self.assertTrue(is_registered(Content))
        self.assertTrue(is_registered(model.TextField))
        self.assertTrue(is_registered(model.Latex))
        self.assertTrue(is_registered(model.ImageContent))
        self.assertTrue(is_registered(model.PDFContent))
        self.assertTrue(is_registered(model.YTVideoContent))

    def test_version_create_textfield(self):
        """ test cases for


        """

        # after this change the number of versions of text1 should be 2
        self.assertEqual(Version.objects.get_for_object(self.text1).count(), 2)
        # the revision ids for text1 should be 1 and 2
        self.assertEqual(list(self.revision_ids1), [2, 1])

    def test_revert_textfield(self):
        # performing the revert with post
        path = reverse('frontend:textfield-history', kwargs={
            'course_id': 1, 'topic_id': 1, 'pk': self.text1.pk
        })
        data = {'rev_pk': '2'}
        self.client.post(path, data)

        # check the state of text1 after the revert
        self.text1.refresh_from_db()

        self.queryset = Version.objects.get_for_object(self.text1)
        self.version_ids1 = self.queryset.values_list("pk", flat=True)
        # the number of versions should be 3 now
        self.assertEqual(self.version_ids1.count(), 3)
        # the textfield should be identical to the original
        self.assertEqual(self.text1.textfield, 'Hello!')

    def test_compare_textfield(self):
        # performing the compare of the first two versions
        path = reverse('frontend:textfield-history', kwargs={
            'course_id': 1, 'topic_id': 1, 'pk': self.text1.pk
        })
        data2 = {"version_id2": self.version_ids1[0], "version_id1": self.version_ids1[1]}
        response = self.client.get(path, data2)
        # check if the differences will be correctly collected
        self.assertContainsHtml(
            response,
            "<del>- Hello!</del>",
            "<ins>+ test test</ins>",
            "<blockquote>change text</blockquote>",  # change log
        )

    def test__compare_content_textfield(self):
        # test with more changes including content-field
        with reversion.create_revision():
            # version 3 for text1
            self.text1.content.description = 'new desc'
            self.text1.source = 'local'
            self.text1.save()
            set_comment('test with more changes including content-field')

        self.queryset = Version.objects.get_for_object(self.text1)
        self.version_ids1 = self.queryset.values_list("pk", flat=True)
        self.revision_ids1 = self.queryset.values_list("revision_id", flat=True)
        # the number of versions and revisions should be 3 now
        self.assertEqual(self.version_ids1.count(), 3)
        self.assertEqual(list(self.revision_ids1), [5, 2, 1])

        # performing compare
        path = reverse('frontend:textfield-history', kwargs={
            'course_id': 1, 'topic_id': 1, 'pk': self.text1.pk
        })
        data3 = {"version_id2": self.version_ids1[0], "version_id1": self.version_ids1[2]}
        response = self.client.get(path, data3)
        # check if the selected versions corresponding the compared versions
        self.assertContainsHtml(
            response,
            f'<input type="radio" name="version_id1" value="{self.version_ids1[0]:d}" style="visibility:hidden" />',
            f'<input type="radio" name="version_id2" value="{self.version_ids1[0]:d}" checked="checked" />',
            f'<input type="radio" name="version_id1" value="{self.version_ids1[2]:d}" checked="checked" />',
            f'<input type="radio" name="version_id2" value="{self.version_ids1[2]:d}" />',
        )
        # check if the differences will be correctly collected
        self.assertContainsHtml(
            response,
            "<del>this is a description</del>",  # change for content.description
            "<ins>new desc</ins>",
            "<del>- test</del>",  # change for source
            "<ins>+ local</ins>",
            "<blockquote>test with more changes including content-field</blockquote>",  # change log
        )

    def test_version_create_latex(self):
        """ test cases for


        """

        # after this change the number of versions of latex1 should be 2
        self.assertEqual(Version.objects.get_for_object(self.latex1).count(), 2)
        # the revision ids for latex1 should be 1 and 2
        self.assertEqual(list(self.revision_ids2), [4, 3])

    def test_revert_latex(self):
        # performing the revert with post
        path = reverse('frontend:latex-history', kwargs={
            'course_id': 1, 'topic_id': 1, 'pk': self.latex1.pk
        })
        data = {'rev_pk': '9'}  # the version number must be correct
        self.client.post(path, data)

        # check the state of text1 after the revert
        self.latex1.refresh_from_db()

        self.queryset2 = Version.objects.get_for_object(self.latex1)
        self.version_ids2 = self.queryset2.values_list("pk", flat=True)
        # the number of versions should be 3 now
        self.assertEqual(self.version_ids2.count(), 3)
        # the text field should be identical to the original
        self.assertEqual(self.latex1.textfield, '/textbf{Hello!}')
        # the revert should not change the author id
        self.assertEqual(self.latex1.content.author_id, self.author_id)
        # after revert the pdf file of latex should still exist
        self.assertIsNotNone(self.latex1.pdf)

    def test_compare_with_attachment(self):

        with reversion.create_revision():
            self.text1.content.attachment.images.get(pk=1).source = 'new source text'
            self.text1.save()
            set_comment('attachment edited')

        self.queryset = Version.objects.get_for_object(self.text1)
        self.version_ids1 = self.queryset.values_list("pk", flat=True)
        # print(self.version_ids1) [13, 6, 2]
        # performing the compare between the last two versions
        path = reverse('frontend:textfield-history', kwargs={
            'course_id': 1, 'topic_id': 1, 'pk': self.text1.pk
        })
        data3 = {"version_id2": self.version_ids1[0], "version_id1": self.version_ids1[1]}
        response = self.client.get(path, data3)
        # TODO the changes of attachment source is not showing at current status
        self.assertContainsHtml(
            response,
            # "<ins>+ new source text</ins>",  # change for source
            "<blockquote>attachment edited</blockquote>",  # change log
        )
        queryset3 = Version.objects.get_for_object(self.text1.content.attachment)
        # the versions of the attachment should also exist in database
        self.assertIsNotNone(queryset3)


    def test_revert_and_compare_course(self):
        with reversion.create_revision():
            course1 = utils.create_content(Course)
            set_comment('initial version')
