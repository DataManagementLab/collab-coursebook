
from django.views.generic import UpdateView

from base.models import Content, Comment, Course, Topic, Favorite, Rating
from frontend.forms import CommentForm, TranslateForm

class ContentRatingView(UpdateView):
    None