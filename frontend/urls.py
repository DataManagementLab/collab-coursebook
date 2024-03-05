"""Purpose of this file

This file defines the URL mapping.
"""

from django.urls import path, re_path, include, register_converter
from django.views.i18n import JavaScriptCatalog
from django.utils.translation import gettext_lazy as _

from content.models import CONTENT_TYPES

from export.views import generate_coursebook_response

from frontend import views


app_name = "frontend"

class BooleanConverter:
     """Boolean converter
     A URL converter for boolean values.

     This converter is used to convert boolean values between Python objects and URL strings.
     It supports the values "True" and "False" (case-insensitive) in URL strings.

     :param regex: The regular expression pattern used to match boolean values in URL strings.
     :type regex: str
     """

     regex = "([Tt]rue)|([Ff]alse)"

     def to_python(self, value):
          """To python
          Converts a boolean value from a URL string to a Python object.

          :param value: The boolean value as a string.
          :type value: str

          :return: The boolean value as a Python object.
          :rtype: bool
          """
          return value.lower() in ["true","True"]

     def to_url(self, value):
          """To URL
          Converts a boolean value from a Python object to a URL string.

          :param value: The boolean value as a Python object.
          :type value: bool

          :return: The boolean value as a URL string.
          :rtype: str

          """
          return str(value)
    
register_converter(BooleanConverter, "boolean")

urlpatterns = [
    path('',
         include([
        re_path(r'^(?P<sort>date-new|date-old|title-a|title-z)/$',
                views.StartView.as_view(),
                name='public-courses-sort'),
        path('',
             views.StartView.as_view(),
             name='public-courses'),
        ])),
    path('dashboard/',
         views.DashboardView.as_view(),
         name="dashboard"),
    path('search/',
         views.search.SearchView.as_view(),
         name='search'),
    path('tutorial/',
         views.TutorialView.as_view(),
         name='tutorial'),
    path('privacy/',
         views.PrivacyNoteView.as_view(),
         name='privacy'),
    path('privacy-accept/',
         views.AcceptPrivacyNoteView.as_view(),
         name='privacy_accept'),
    path('profile/<int:pk>/', include([
        path('',
             views.ProfileView.as_view(),
             name='profile'),
        path('edit',
             views.ProfileEditView.as_view(),
             name='profile-edit'),
    ])),

    path('courses/', include([
        re_path(r'^(?P<sort>date-new|date-old|title-a|title-z)/$',
                views.CourseListView.as_view(),
                name='courses-sort'),
        path('',
             views.CourseListView.as_view(),
             name='courses'),
        path('<int:pk>/', include([
            path('duplicate/',
                 views.course.DuplicateCourseView.as_view(),
                 name='course-duplicate'),
            path('',
                 views.CourseView.as_view(),
                 name='course'),
            path('public',
                 views.PublicCourseView.as_view(),
                 name='public'),
            path('edit/',
                 views.course.EditCourseView.as_view(),
                 name='course-edit'),
            path('edit/structure',
                 views.course.EditCourseStructureView.as_view(),
                 name='course-edit-structure'),
            path('history/',
                 views.history.CourseHistoryCompareView.as_view(),
                 name='course-history'),
            path('delete/',
                 views.CourseDeleteView.as_view(),
                 name='course-delete'),
            path('coursebook/',
                 generate_coursebook_response,
                 {'exp_all': False, 'file_name': _('Coursebook')},
                 name='coursebook-generate'),
            path('export/',
                 generate_coursebook_response,
                 {'exp_all': True},
                 name='export-course'),
        ])),
        path('<int:course_id>/topic/<int:topic_id>/content/', include([

            re_path(r'add/(?P<type>' + '|'.join(list(CONTENT_TYPES.keys())) + ')/$',
                    views.content.AddContentView.as_view(), name='content-add'),
            path('<int:content_id>/', include([
                path('attachment/<int:pk>',
                     views.content.AttachedImageView.as_view(),
                     name='attachment'),
                path('rate/<int:pk>/',
                     views.rate_content,
                     name='rating'),
               path('approve/<boolean:approval>/',
                     views.approve_content,
                     name='approve'),
                path('comment/<int:pk>/delete/',
                     views.DeleteComment.as_view(),
                     name='comment-delete'),
                path('comment/<int:pk>/edit/',
                     views.EditComment.as_view(),
                     name='comment-edit'),
                path('coursebook/addfromcontent/',
                     views.coursebook.add_to_coursebook,
                     name='coursebook-add'),
                path('coursebook/removefromcontent/',
                     views.coursebook.remove_from_coursebook,
                     name='coursebook-remove'),
                path('coursebook/addfromcourse/',
                     views.coursebook.add_to_coursebook_from_courseview,
                     name='coursebook-add-courseview'),
                path('coursebook/removefromcourse/',
                     views.coursebook.remove_from_coursebook_from_courseview,
                     name='coursebook-remove-courseview'),

            ])),
            path('<pk>/',
                 views.ContentView.as_view(),
                 name='content'),
            path('<pk>/edit/',
                 views.content.EditContentView.as_view(),
                 name='content-edit'),
            path('<pk>/delete/',
                 views.content.DeleteContentView.as_view(),
                 name='content-delete'),
            path('<pk>/read/',
                 views.content.ContentReadingModeView.as_view(),
                 name='content-reading-mode'),
            path('<pk>/public-read/',
                 views.content.PublicContentReadingModeView.as_view(),
                 name='public-content-reading-mode'),
            path('<pk>/textfield-history/',
                 views.history.TextfieldHistoryCompareView.as_view(),
                 name='textfield-history'),
            path('<pk>/ytvideo-history/',
                 views.history.YTVideoHistoryCompareView.as_view(),
                 name='ytvideo-history'),
            path('<pk>/image-history/',
                 views.history.ImageHistoryCompareView.as_view(),
                 name='image-history'),
            path('<pk>/pdf-history/',
                 views.history.PdfHistoryCompareView.as_view(),
                 name='pdf-history'),
            path('<pk>/latex-history/',
                 views.history.LatexHistoryCompareView.as_view(),
                 name='latex-history'),
            path('<pk>/markdown-history/',
                 views.history.MDHistoryCompareView.as_view(),
                 name='md-history'),
            path('<pk>/panoptovideo-history/',
                 views.history.PanoptoVideoHistoryCompareView.as_view(),
                 name='panoptovideo-history'),
            path('<pk>/anki-history/',
                 views.history.AnkiHistoryCompareView.as_view(),
                 name='anki-history'),
            path('<pk>/exercise-history/',
                 views.history.ExerciseHistoryCompareView.as_view(),
                 name='exercise-history'),
            path('<pk>/generalurl-history/',
                 views.history.GeneralURLHistoryCompareView.as_view(),
                 name='generalurl-history'),     

        ])),
        path('add/',
             views.AddCourseView.as_view(),
             name='add-course'),
    ])),

    path('category/<int:pk>/', include([
        re_path(r'^(?P<sort>date-new|date-old|title-a|title-z)/$',
                views.CourseListForCategoryView.as_view(),
                name='category-courses-sort'),
        path('',
             views.CourseListForCategoryView.as_view(),
             name='category-courses'),
    ])),

    path('period/<int:pk>/', include([
        re_path(r'^(?P<sort>date-new|date-old|title-a|title-z)/$',
                views.CourseListForPeriodView.as_view(),
                name='period-courses-sort'),
        path('',
             views.CourseListForPeriodView.as_view(),
             name='period-courses'),
    ])),

    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
]
