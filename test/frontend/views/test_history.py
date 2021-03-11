"""Purpose of this file

This file contains the test cases for /frontend/views/history.py.
"""

from test import utils
from test.test_cases import MediaTestCase, BaseCourseViewTestCase

import reversion

from reversion import set_comment, is_registered
from reversion.models import Version


from django.urls import reverse

from base.models import Content, Course

import content.models as model


class BaseHistoryCompareViewTestCase(MediaTestCase):
    """BaseHistoryCompareView test case

    Defines the test cases for view BaseHistoryCompareView.
    """

    def test_initial_state(self):
        """Test case - initial states

        Tests if the relevant models are registered.
        """
        self.assertTrue(is_registered(Course))
        self.assertTrue(is_registered(Content))
        self.assertTrue(is_registered(model.TextField))
        self.assertTrue(is_registered(model.Latex))
        self.assertTrue(is_registered(model.ImageContent))
        self.assertTrue(is_registered(model.PDFContent))
        self.assertTrue(is_registered(model.YTVideoContent))


class ContentHistoryCompareViewTestCase(MediaTestCase):
    """ history compare test cases

    Defines test cases for the view ContentHistoryCompareView.
    """

    def setUp(self):
        """Setup

        Sets up the test database.
        """
        super().setUp()
        # set up a textfield item to test
        with reversion.create_revision():
            content1 = utils.create_content(model.TextField.TYPE)
            utils.generate_attachment(content1, 2)
            text1 = model.TextField.objects.create(content=content1,
                                                   textfield='Hello!',
                                                   source='test')
            set_comment('initial version')

        # create a new version and make 1 change to text1
        with reversion.create_revision():
            text1.textfield = 'test test'
            text1.save()
            set_comment('change text')

        queryset = Version.objects.get_for_object(text1)
        self.revision_ids1 = queryset.values_list("revision_id", flat=True)
        self.version_ids1 = queryset.values_list("pk", flat=True)

        # set up a latex item to test
        with reversion.create_revision():
            content2 = utils.create_content(model.Latex.TYPE)
            latex1 = model.Latex.objects.create(content=content2,
                                                textfield='/textbf{Hello!}',
                                                source='test')
            set_comment('initial version')

        # create a new version and make 1 change to latex1
        with reversion.create_revision():
            latex1.textfield = '/textbf{你好！}'
            latex1.save()
            set_comment('change code')

        queryset2 = Version.objects.get_for_object(latex1)
        self.revision_ids2 = queryset2.values_list("revision_id", flat=True)
        self.version_ids2 = queryset2.values_list("pk", flat=True)

        self.textfield_path = reverse('frontend:textfield-history', kwargs={
            'course_id': 1, 'topic_id': 1, 'pk': text1.pk
        })
        self.latex_path = reverse('frontend:latex-history', kwargs={
            'course_id': 1, 'topic_id': 1, 'pk': latex1.pk
        })

    def test_textfield_version_create(self):
        """Create version test case - Textfield

        Tests if the versions are correctly generated for text1.
        """
        # after set up the number of versions of text1 should be 2
        text1 = model.TextField.objects.get(pk=2)
        self.assertEqual(Version.objects.get_for_object(text1).count(), 2)
        # the revision ids for text1 should be 1 and 2
        self.assertEqual(list(self.revision_ids1), [2, 1])

    def test_textfield_revert_changes(self):
        """Revert version test case - Textfield changes

        Tests content revert with one change within TextField model.
        """
        # performing the revert with post
        data = {'ver_pk': '2'}
        self.client.post(self.textfield_path, data)

        # check the state of text1 after the revert
        text1 = model.TextField.objects.get(pk=2)
        text1.refresh_from_db()

        queryset = Version.objects.get_for_object(text1)
        self.version_ids1 = queryset.values_list("pk", flat=True)
        # the number of versions should be 3 now
        self.assertEqual(self.version_ids1.count(), 3)
        # the textfield should be identical to version 1
        self.assertEqual(text1.textfield, 'Hello!')
        # topic id should not be changed
        self.assertEqual(text1.content.topic_id, 1)

    def assert_revert_to_2nd_version(self):
        """assert contains html

        Assert that the textfield gets reverted to the 2nd version successfully
        """
        # performing the revert to the 2nd version with post
        data = {'ver_pk': '6'}
        self.client.post(self.textfield_path, data)

        # check the state of text1 after the revert
        text1 = model.TextField.objects.get(pk=2)
        text1.refresh_from_db()

        queryset = Version.objects.get_for_object(text1)
        self.version_ids1 = queryset.values_list("pk", flat=True)
        # the number of versions should be 4 now
        self.assertEqual(self.version_ids1.count(), 4)
        # the textfield should be identical to version 2
        self.assertEqual(text1.textfield, 'test test')
        # the source should be identical to version 2 too
        self.assertEqual(text1.source, 'test')
        # topic id should not be changed
        self.assertEqual(text1.content.topic_id, 1)

    def test_textfield_revert_no_changes(self):
        """Revert version test case - Textfield no changes

        Tests content revert with no change within TextField model.
        """
        # save a new version but don't make any change
        with reversion.create_revision():
            text1 = model.TextField.objects.get(pk=2)
            text1.save()
            set_comment('nothing changed')
        self.assert_revert_to_2nd_version()

    def test_textfield_revert_many_fields(self):
        """Revert version test case - Textfield many fields changed

        Tests content revert with more than one change within TextField model.
        """
        # save a new version but don't make any change
        with reversion.create_revision():
            text1 = model.TextField.objects.get(pk=2)
            text1.textfield = 'jo jo'
            text1.source = 'new source'
            text1.save()
            set_comment('text and source changed')
        self.assert_revert_to_2nd_version()

    def test_textfield_compare_change_one(self):
        """Compare test case - Textfield one change

        Tests content history compare with one change within TextField model
        """
        # performing the compare of the first two versions
        data2 = {"version_id2": self.version_ids1[0], "version_id1": self.version_ids1[1]}
        response = self.client.get(self.textfield_path, data2)
        # check if the differences will be correctly collected
        self.assert_contains_html(
            response,
            "<del>- Hello!</del>",
            "<ins>+ test test</ins>",
            "<blockquote>change text</blockquote>",  # change log
        )

    def test_textfield_compare_no_change(self):
        """Compare test case - Textfield no change

        Tests content history compare with no change within TextField model.
        """
        # save a new version but don't make any change
        with reversion.create_revision():
            text1 = model.TextField.objects.get(pk=2)
            text1.save()
            set_comment('nothing changed')
        # performing the revert to the 2nd version with post
        data2 = {"version_id2": self.version_ids1[0], "version_id1": self.version_ids1[1]}
        response = self.client.get(self.textfield_path, data2)
        self.assert_contains_html(response,
                                  "There are no differences.")

    def test_textfield_compare_many_change(self):
        """Compare test case - Textfield many changes

        Tests content history compare with more than 1 changes from Content and TextField model.
        """
        # test with more changes including content-field
        text1 = model.TextField.objects.get(pk=2)
        with reversion.create_revision():
            # version 3 for text1
            text1.content.description = 'new desc'
            text1.source = 'local'
            text1.save()
            set_comment('test with more changes including content-field')

        queryset = Version.objects.get_for_object(text1)
        version_ids1 = queryset.values_list("pk", flat=True)
        revision_ids1 = queryset.values_list("revision_id", flat=True)
        # the number of versions and revisions should be 3 now
        self.assertEqual(version_ids1.count(), 3)
        self.assertEqual(list(revision_ids1), [5, 2, 1])

        # performing compare
        data3 = {"version_id2": version_ids1[0], "version_id1": version_ids1[2]}
        response = self.client.get(self.textfield_path, data3)
        # check if the selected versions corresponding the compared versions
        self.assert_contains_html(
            response,
            f'<input onclick="validateCompareOption(this, true)" type="radio" name="version_id1" value="{version_ids1[0]:d}" '
            f'style="visibility:hidden" />',
            f'<input onclick="validateCompareOption(this, false)" type="radio" name="version_id2" value="{version_ids1[0]:d}" '
            f'checked="checked" />',
            f'<input onclick="validateCompareOption(this, true)" type="radio" name="version_id1" value="{version_ids1[2]:d}" '
            f'checked="checked" />',
            f'<input onclick="validateCompareOption(this, false)" type="radio" name="version_id2" value="{version_ids1[2]:d}" />',
        )
        # check if the differences will be correctly collected
        self.assert_contains_html(
            response,
            "<del>this is a description</del>",  # change for content.description
            "<ins>new desc</ins>",
            "<del>- test</del>",  # change for source
            "<ins>+ local</ins>",
            "<blockquote>test with more changes including content-field</blockquote>",  # change log
        )

    def test_latex_version_create(self):
        """Create version test case - LaTeX

        Tests if the versions are correctly generated for latex1.
        """
        latex1 = model.Latex.objects.get(pk=3)
        # after set up the number of versions of latex1 should be 2
        self.assertEqual(Version.objects.get_for_object(latex1).count(), 2)
        # the revision ids for latex1 should be 1 and 2
        self.assertEqual(list(self.revision_ids2), [4, 3])

    def test_latex_revert_changes(self):
        """Revert version test case - LaTeX changes

        Tests latex revert with changes within the Latex model.
        """
        # performing the revert with post
        data = {'ver_pk': '10'}  # the version number must be correct
        self.client.post(self.latex_path, data)

        # check the state of latex1 after the revert
        latex1 = model.Latex.objects.get(pk=3)
        latex1.refresh_from_db()

        queryset2 = Version.objects.get_for_object(latex1)
        self.version_ids2 = queryset2.values_list("pk", flat=True)
        # the number of versions should be 3 now
        self.assertEqual(self.version_ids2.count(), 3)
        # the text field should be identical to the original
        self.assertEqual(latex1.textfield, '/textbf{Hello!}')
        # the revert should not change the author id
        self.assertEqual(latex1.content.author_id, 1)
        # after revert the pdf file of latex should still exist
        self.assertIsNotNone(latex1.pdf)

    # TODO next iteration #pylint: disable=fixme,pointless-string-statement
    """def test_compare_with_attachment(self):
        """"""Compare test case - Content history compare with attachment

        Tests content history compare with attachment.
        """"""
        text1 = model.TextField.objects.get(pk=2)
        with reversion.create_revision():
            text1.content.attachment.images.get(pk=1).source = 'new source text'
            text1.save()
            set_comment('attachment edited')

        queryset = Version.objects.get_for_object(text1)
        self.version_ids1 = queryset.values_list("pk", flat=True)
        # performing the compare between the last two versions
        data3 = {"version_id2": self.version_ids1[0], "version_id1": self.version_ids1[1]}
        response = self.client.get(self.textfield_path, data3)
        # TODO the changes of attachment source is not showing at current status #pylint: disable=fixme
        self.assert_contains_html(
            response,
            # "<ins>+ new source text</ins>",  # change for source
            "<blockquote>attachment edited</blockquote>",  # change log
        )
        queryset3 = Version.objects.get_for_object(text1.content.attachment)
        # the versions of the attachment should also exist in database
        self.assertNotEqual(queryset3.values_list("pk", flat=True).count(), 0)"""


class CourseHistoryCompareViewTestCase(BaseCourseViewTestCase):
    """ CourseHistoryCompareView Test Cases

    Defines Test Cases for the view CourseHistoryCompareView.
    """

    def setUp(self):
        """Setup

        Sets up the test database.
        """
        super().setUp()

        # create a new version and make 1 change to course1
        with reversion.create_revision():
            self.course1.description = 'test test'
            self.course1.save()
            set_comment('change desc')

        self.queryset = Version.objects.get_for_object(self.course1)
        self.revision_ids1 = self.queryset.values_list("revision_id", flat=True)
        self.version_ids1 = self.queryset.values_list("pk", flat=True)

        self.cat_id = self.cat.pk

    def test_version_create_course(self):
        """Create course test case - Version

        Tests if the versions of the course are correctly generated.
        """

        # after set up the number of versions of course1 should be 2
        self.assertEqual(Version.objects.get_for_object(self.course1).count(), 2)
        # the revision ids for text1 should be 1 and 2
        self.assertEqual(list(self.revision_ids1), [2, 1])
        self.assertEqual(self.course1.description, 'test test')

    def test_revert_course_change_one(self):
        """Revert course test case - One change

        Tests course revert when there is exactly 1 change.
        """
        # performing the revert with post
        path = reverse('frontend:course-history', kwargs={
            'pk': self.course1.pk
        })
        data = {'ver_pk': '1'}
        self.client.post(path, data)

        # check the state of course1 after the revert
        self.course1.refresh_from_db()

        self.queryset = Version.objects.get_for_object(self.course1)
        self.version_ids1 = self.queryset.values_list("pk", flat=True)
        # the number of versions should be 3 now
        self.assertEqual(self.version_ids1.count(), 3)
        # the textfield should be identical to the original
        self.assertEqual(self.course1.description, 'desc')
        # the category should not be changed after revert
        self.assertEqual(self.course1.category_id, self.cat_id)

    def assert_revert_to_2nd_version(self):
        """assert contains html

        Assert that the course gets reverted to the 2nd version successfully
        """
        # performing the revert with post
        path = reverse('frontend:course-history', kwargs={
            'pk': self.course1.pk
        })
        data = {'ver_pk': '2'}
        self.client.post(path, data)

        # check the state of course1 after the revert
        self.course1.refresh_from_db()

        self.queryset = Version.objects.get_for_object(self.course1)
        self.version_ids1 = self.queryset.values_list("pk", flat=True)
        # the number of versions should be 4 now
        self.assertEqual(self.version_ids1.count(), 4)
        # the desc should be identical to version 2
        self.assertEqual(self.course1.description, 'test test')
        # the title should be identical to version 1
        self.assertEqual(self.course1.title, 'Course Test')
        # the category should not be changed after revert
        self.assertEqual(self.course1.category_id, self.cat_id)

    def test_revert_course_no_change(self):
        """Revert test cases - No changes

        Tests course revert when there is no change.
        """
        # save a new version but don't make any change
        with reversion.create_revision():
            self.course1.save()
            set_comment('nothing changed')
        self.assert_revert_to_2nd_version()

    def test_revert_course_many_changes(self):
        """Revert test cases - Many changes

        Tests course revert when more than 1 change.
        """
        with reversion.create_revision():
            self.course1.description = 'new descc xixi'
            self.course1.title = 'xixi'
            self.course1.save()
            set_comment('title and desc changed')

        self.assert_revert_to_2nd_version()

    def test_compare_course_change_one(self):
        """Compare test cases - One change

        Tests course course history compare when there is exactly 1 change.
        """
        # performing compare
        path = reverse('frontend:course-history', kwargs={
            'pk': self.course1.pk
        })
        data = {"version_id2": self.version_ids1[0], "version_id1": self.version_ids1[1]}
        response = self.client.get(path, data)

        # check if the differences will be correctly collected
        self.assert_contains_html(
            response,
            "<del>- desc</del>",  # change for description
            "<ins>+ test test</ins>",
            "<blockquote>change desc</blockquote>",  # change log
        )

    def test_compare_course_no_change(self):
        """Compare test cases - No changes

        Tests course course history compare when there is no changes.
        """
        with reversion.create_revision():
            self.course1.save()
            set_comment('nothing changed')
        # performing compare
        path = reverse('frontend:course-history', kwargs={
            'pk': self.course1.pk
        })
        data = {"version_id2": self.version_ids1[0], "version_id1": self.version_ids1[1]}
        response = self.client.get(path, data)

        self.assert_contains_html(response,
                                  "There are no differences.")

    def test_compare_course_many_changes(self):
        """Compare test cases - Many changes

        Tests course course history compare when there is more than 1 changes.
        """
        with reversion.create_revision():
            self.course1.description = 'new descc xixi'
            self.course1.title = 'xixi'
            self.course1.save()
            set_comment('title and desc changed')
        # performing compare
        path = reverse('frontend:course-history', kwargs={
            'pk': self.course1.pk
        })
        data = {"version_id2": self.version_ids1[0], "version_id1": self.version_ids1[1]}
        response = self.client.get(path, data)
        # check if the differences will be correctly collected
        self.assert_contains_html(
            response,
            "<del>- test test</del>",  # change for description
            "<ins>+ new descc xixi</ins>",
            "<del>- Course Test</del>",  # change for title
            "<ins>+ xixi</ins>",
            "<blockquote>title and desc changed</blockquote>",  # change log
        )
