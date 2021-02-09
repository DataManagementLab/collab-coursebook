"""Purpose of this file

Marks this directory as Python package directories. This package contains
frontend views related operation.
"""

from .page import StartView, DashboardView
from .profile import ProfileView, ProfileEditView
from .courses import CourseListView, CourseListForCategoryView, CourseListForPeriodView
from .course import CourseView, AddCourseView, CourseDeleteView
from .content import ContentView
from .comment import EditComment, DeleteComment
from .content import rate_content
from .history import CourseHistoryCompareView, LatexHistoryCompareView, PdfHistoryCompareView, ImageHistoryCompareView, YTVideoHistoryCompareView, ImageHistoryCompareView
