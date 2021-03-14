"""Purpose of this file

Marks this directory as Python package directories. This package contains
frontend views related operation.
"""

from .content import ContentView
from .content import rate_content

from .course import CourseView, AddCourseView, EditCourseStructureView, CourseDeleteView

from .coursebook import add_to_coursebook
from .courses import CourseListView, CourseListForCategoryView, CourseListForPeriodView

from .comment import EditComment, DeleteComment

from .history import CourseHistoryCompareView, PdfHistoryCompareView, ImageHistoryCompareView
from .history import LatexHistoryCompareView, YTVideoHistoryCompareView

from .page import StartView, DashboardView, TutorialView

from .profile import ProfileView, ProfileEditView

from .search import SearchView
