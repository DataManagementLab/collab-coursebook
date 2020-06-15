from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, CreateView

from base.models import Content, Comment, Course, Topic, Favorite
from base.utils import get_user
from frontend.forms import CommentForm, TranslateForm
from frontend.forms.addcontent import AddContentForm, AddContentFormYoutubeVideo, AddContentFormImage


class AddContentView(SuccessMessageMixin, LoginRequiredMixin, CreateView):  # pylint: disable=too-many-ancestors
    """
    Adds a new content to the database
    """
    model = Course
    template_name = 'frontend/content/addcontent.html'
    form_class = AddContentForm
    success_url = reverse_lazy('frontend:dashboard')

    def get_success_message(self, cleaned_data):
        return _(f"Content '{cleaned_data['type']}' successfully added")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if "type" in self.kwargs:
            content_type = self.kwargs['type']
            if content_type == 'youtubevideo':
                context['typeform'] = AddContentFormYoutubeVideo
            elif content_type == 'image':
                context['typeform'] = AddContentFormImage
            else:
                pass
        return context

    def post(self, request, *args, **kwargs):
        # TODO: process form input
        pass
    
    # def form_valid(self, form):
    #     """
    #     Checks whether the form is valid. And saves the entered content.
    #     :param AddContentForm form: The form that should be checked
    #     :return: the user is redirected to the content page
    #     :rtype: HttpResponseRedirect
    #     """
    #     content = form.save(commit=False)
    #     content.author = get_user(self.request)
    #     topic_id = self.kwargs['topic_id']
    #     content.topic = Topic.objects.get(pk=topic_id)
    #     content.save()
    #     course_id = self.kwargs['course_id']
    #     topic_id = self.kwargs['topic_id']
    #     return HttpResponseRedirect(reverse_lazy('frontend:content', args=(course_id, topic_id, content.id,)))


class ContentView(DetailView):  # pylint: disable=too-many-ancestors
    """
    Displays the content to the user
    """
    model = Content
    template_name = "frontend/content/detail.html"
    #form_class = Comment

    def post(self, request, *args, **kwargs):  # pylint: disable=unused-argument
        """
        create comment in database
        :param HttpResponse request: request
        :param args: args
        :param dict kwargs: keyword arguments
        :return: redirect to content page
        :rtype: HttpResponse
        """
        comment_form = CommentForm(request.POST)
        translate_form = TranslateForm(request.POST)
        self.object = self.get_object()  # line required

        if comment_form.is_valid():
            text = comment_form.cleaned_data['text']
            Comment.objects.create(content=self.get_object(), creation_date=timezone.now(),  # pylint: disable=no-member
                                   author=request.user.profile, text=text)
        elif translate_form.is_valid():
            language = translate_form.cleaned_data['translation']
            context = self.get_context_data(**kwargs)
            # get original content
            content = self.object
            """
            with content.file.open() as file:
                html = markdown(file.read().decode('utf-8'), safe_mode=True,
                                extras=["tables"])

            original_content = html

            # translate using google translate
            if language != "None":
                translation = Translator().translate(original_content, dest=language).text
                # use beautifulsoup to create pretty html, remove whitespaces eg.
                soup = BeautifulSoup(translation, features="html.parser")
                translated_html = ''.join(soup.prettify())
                # remove whitespaces from urls: Google translate adds whitespaces to urls
                translated_html = re.sub(r'\s*([/])\s*', r'\1', translated_html)
                context['markdown'] = translated_html
                initialized_form = TranslateForm()
                initialized_form.fields['translation'].initial = str(language)
                context['translate_form'] = initialized_form
            else:
                context['markdown'] = original_content
            """
            return self.render_to_response(context)

        course_id = self.kwargs['course_id']
        topic_id = self.kwargs['topic_id']
        return HttpResponseRedirect(
            reverse_lazy('frontend:content', args=(course_id, topic_id, self.get_object().id,))
            + '#comments')

    def get_context_data(self, **kwargs):
        """
        get context data
        :param dict kwargs: keyword arguments
        :return: context
        :rtype: dict
        """
        context = super().get_context_data(**kwargs)
        context['search_result'] = self.request.GET.get('q')
        content = super().get_object()
        context['count'] = content.get_rate_count()
        context['rate'] = round(content.get_rate(), 2)

        # course id for back to course button
        course_id = self.kwargs['course_id']
        course = Course.objects.get(pk=course_id)  # pylint: disable=no-member
        context['course'] = course

        topic = Topic.objects.get(pk=self.kwargs['topic_id'])
        context['topic'] = topic
        context['isCurrentUserOwner'] = self.request.user.profile in course.owners.all()

        """
        if '.md' in content.file.name:
            with content.file.open() as file:
                # needs to be capable of displaying ä ö ü
                html = markdown(file.read().decode('utf-8'), safe_mode=True,
                                extras=["tables"])
                chars = {'ö': '&ouml', 'ä': '&auml', 'ü': '&uuml', 'Ü': '&Uuml', 'Ä': '&Auml',
                         'Ö': '&Ouml', 'ß': '&szlig'}
                for char in chars:
                    html = html.replace(char, chars[char])
                context['markdown'] = html
        """

        context['comment_form'] = CommentForm()
        context['comments'] = Comment.objects.filter(content=self.get_object()  # pylint: disable=no-member
                                                     ).order_by('-creation_date')
        context['translate_form'] = TranslateForm()

        if self.request.GET.get('coursebook'):
            context['ending'] = '?coursebook=True'
        elif self.request.GET.get('s'):
            context['ending'] = '?s=' + self.request.GET.get('s') + "&f=" \
                                + self.request.GET.get('f')

        if self.request.user.is_authenticated:
            context['user_rate'] = content.get_user_rate(self.request.user.profile)
            """
            if Favourite.objects.filter(course=course, user=get_user(self.request),
                                        content_list=content).count() > 0:
                context['favourite'] = True
            """
        return context


class ContentReadingModeView(DetailView):  # pylint: disable=too-many-ancestors
    """
    Displays the content to the user
    """
    model = Content
    template_name = "frontend/content/readingmode.html"

    def get_context_data(self, **kwargs):
        """
        gets the context data for the response
        :param dict kwargs: keyword arguments
        :return: the context
        :rtype: dict
        """
        context = super().get_context_data(**kwargs)
        context['course_id'] = self.kwargs['course_id']
        context['topic_id'] = topic_id = self.kwargs['topic_id']
        content = self.get_object()

        topic = Topic.objects.get(pk=topic_id)
        if self.request.GET.get('coursebook'):
            course = get_object_or_404(Course, {"pk": self.kwargs['course_id']})
            contents = [f.content for f in Favorite.objects.filter(course=course, user=self.request.user.profile)] #models.get_coursebook_flat(get_user(self.request), course)
        else:
            contents = topic.get_contents(self.request.GET.get('s'), self.request.GET.get('f'))

        list_of_content_ids = [content.id for content in contents]

        index_of_content = list_of_content_ids.index(content.id)
        if index_of_content > 0:
            context['previous_id'] = list_of_content_ids[index_of_content - 1]
        else:
            context['previous_id'] = list_of_content_ids[-1]

        if index_of_content == len(list_of_content_ids) - 1:
            context['next_id'] = list_of_content_ids[0]
        else:
            context['next_id'] = list_of_content_ids[index_of_content + 1]
        if self.request.GET.get('coursebook'):
            context['ending'] = '?coursebook=True'
        elif self.request.GET.get('s'):
            context['ending'] = '?s=' + self.request.GET.get('s') + "&f=" + \
                                self.request.GET.get('f')
        return context
