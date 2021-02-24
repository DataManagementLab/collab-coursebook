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


class HistoryCompareViewTestCase(MediaTestCase):
    """ history compare test cases

    Defines test cases for ContentHistoryCompareView and CourseHistoryCompareView

    """

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

    def test_revert_and_compare_textfield(self):
        """ test cases for revert and comparing textfield content


        """

        with reversion.create_revision():
            content1 = utils.create_content(model.TextField.TYPE)
            text1 = model.TextField.objects.create(content=content1,
                                                   textfield='Hello!',
                                                   source='test')
            set_comment('initial version')

        # print("version 1:", text1)

        # create a new version and make 1 change to text1
        with reversion.create_revision():
            text1.textfield = 'test test'
            text1.save()
            set_comment('change text')

        queryset = Version.objects.get_for_object(text1)
        revision_ids1 = queryset.values_list("revision_id", flat=True)

        # after this change the number of versions of text1 should be 2
        self.assertEqual(Version.objects.get_for_object(text1).count(), 2)
        # the revision ids for text1 should be 1 and 2
        self.assertEqual(list(revision_ids1), [2, 1])

        # performing the revert with post
        path = reverse('frontend:textfield-history', kwargs={
            'course_id': 1, 'topic_id': 1, 'pk': text1.pk
        })
        data = {'rev_pk': '1'}
        self.client.post(path, data)

        # check the state of text1 after the revert
        text1.refresh_from_db()

        queryset = Version.objects.get_for_object(text1)
        version_ids1 = queryset.values_list("pk", flat=True)
        # the number of versions should be 3 now
        self.assertEqual(version_ids1.count(), 3)
        # the textfield should be identical to the original
        self.assertEqual(text1.textfield, 'Hello!')

        # performing the compare of the first two versions
        data2 = {"version_id2": version_ids1[1], "version_id1": version_ids1[2]}
        response = self.client.get(path, data2)
        # check if the differences will be correctly collected
        self.assertContainsHtml(
            response,
            "<del>- Hello!</del>",
            "<ins>+ test test</ins>",
            "<blockquote>change text</blockquote>",  # change log
        )

        # test with more changes including content-field
        with reversion.create_revision():
            # version 4 for text1
            text1.content.description = 'new desc'
            text1.source = 'local'
            text1.save()
            set_comment('test with more changes including content-field')

        queryset = Version.objects.get_for_object(text1)
        version_ids2 = queryset.values_list("pk", flat=True)
        revision_ids2 = queryset.values_list("revision_id", flat=True)
        # the number of versions and revisions should be 4 now
        self.assertEqual(version_ids2.count(), 4)
        self.assertEqual(list(revision_ids2), [4, 3, 2, 1])
        # performing compare
        data3 = {"version_id2": version_ids2[0], "version_id1": version_ids2[1]}
        response = self.client.get(path, data3)
        # check if the selected versions corresponding the compared versions
        self.assertContainsHtml(
            response,
            f'<input type="radio" name="version_id1" value="{version_ids2[0]:d}" style="visibility:hidden" />',
            f'<input type="radio" name="version_id2" value="{version_ids2[0]:d}" checked="checked" />',
            f'<input type="radio" name="version_id1" value="{version_ids2[1]:d}" checked="checked" />',
            f'<input type="radio" name="version_id2" value="{version_ids2[1]:d}" />',
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

    def test_revert_and_compare_course(self):
        with reversion.create_revision():
            course1 = utils.create_content(Course)
            set_comment('initial version')

