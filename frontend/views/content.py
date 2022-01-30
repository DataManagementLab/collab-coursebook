"""Purpose of this file

This file describes the frontend views related to content types.
"""
import re

import markdown
import math

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView

from base.models import Content, Comment, Course, Topic, Favorite
from base.utils import get_user

from content.attachment.forms import ImageAttachmentFormSet, LatexPreviewImageAttachmentFormSet
from content.attachment.models import ImageAttachment, IMAGE_ATTACHMENT_TYPES
from content.forms import CONTENT_TYPE_FORMS, EditMD
from content.models import CONTENT_TYPES

from frontend.forms.comment import CommentForm
from frontend.forms.content import AddContentForm, EditContentForm, TranslateForm
from frontend.templatetags.cc_frontend_tags import js_escape
from frontend.views.history import Reversion
from frontend.views.validator import Validator

from content.static.yt_api import *
from export.views import latex_preview

def clean_attachment(content, image_formset):
    """Clean attachment

    Cleans the attachment from the database if the attachments
    were removed from the form.

    :param content: The content object
    :type content: Content
    :param image_formset: The image form set
    :type image_formset: BaseModelFormSet
    """
    clean = content.ImageAttachments.count() - image_formset.total_form_count()
    if clean > 0:
        remove_source = content.ImageAttachments.order_by('id').reverse()[:clean]
        for remove_object in remove_source:
            remove_object.delete()


# Tooltip for LaTeX
# str: Path of the LaTeX example code
LATEX_EXAMPLE_PATH = 'content/templates/form/examples/Latex_textfield.txt'
# __proxy__: Message if the file was not found
LATEX_EXAMPLE = _('There exists no example yet.')

# Retrieve example code
try:
    with open(LATEX_EXAMPLE_PATH, 'r') as file:
        LATEX_EXAMPLE = js_escape(file.read())
except FileNotFoundError:
    pass


def rate_content(request, course_id, topic_id, content_id, pk):  # pylint: disable=invalid-name
    """Rate content

    Lets the user rate content.

    :param topic_id: The id of the topic
    :type topic_id: int
    :param request: The given request
    :type request: HttpRequest
    :param course_id: The course id
    :type course_id: int
    :param content_id: The id of the content which gets rated
    :type content_id: int
    :param pk: The user rating (should be in [ 1, 2, 3, 4, 5])
    :type pk: Any


    :return: the redirection to the content page
    :rtype: HttpResponse
    """
    content = get_object_or_404(Content, pk=content_id)
    profile = get_user(request)
    content.rate_content(user=profile, rating=pk)

    return HttpResponseRedirect(
        reverse_lazy('frontend:content', args=(course_id, topic_id, content_id,))
        + '#rating')


def md_to_html(text, content):
    if content.ImageAttachments.count() > 0:
        attachments = content.ImageAttachments.all()
        for idx, attachment in enumerate(attachments):
            text = re.sub(rf"!\[(.*?)]\(Image-{idx}\)",
                          rf"![\1]({attachment.image.url})",
                          text)
    return markdown.markdown(text)


class AddContentView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    """Add content view

    Adds a new content to the database.

    :attr AddContentView.model: The model to which this view corresponds
    :type AddContentView.model: Model
    :attr AddContentView.template_name: The path to the html template
    :type AddContentView.template_name: str
    :attr AddContentView.success_url: Redirection of a successful url
    :type AddContentView.success_url: __proxy__
    :attr AddContentView.context_object_name: The context object name
    :type AddContentView.context_object_name: str
    """
    model = Content
    template_name = 'frontend/content/add.html'
    form_class = AddContentForm
    success_url = reverse_lazy('frontend:dashboard')
    context_object_name = 'content'
    object = None

    def get_success_message(self, cleaned_data):
        """Success message

        Returns the success message when the content was created.

        :param cleaned_data: The cleaned data
        :type cleaned_data: dict[str, Any]

        :return: the success message when the profile was updated
        :rtype: __proxy__
        """
        message = _("Content %(title)s successfully added") % {'title': cleaned_data['type']}
        return message

    def handle_error(self):
        """Error handling

        Creates an error message and return to course page.

        :return: to the course page
        :rtype: HttpResponseRedirect
        """
        course_id = self.kwargs['course_id']
        messages.error(self.request, _('An error occurred while processing the request'))
        return HttpResponseRedirect(reverse('frontend:course', args=(course_id,)))

    def get_context_data(self, **kwargs):
        """Context data

        Gets the context data of the view which can be accessed in
        the html templates.

        :param kwargs: The additional arguments
        :type kwargs: dict[str, Any]

        :return: the context data
        :rtype: dict[str, Any]
        """
        context = super().get_context_data(**kwargs)
        # Retrieves the form for content type
        content_type = self.kwargs['type']
        if 'content_type_form' not in context:
            context['content_type_form'] = CONTENT_TYPE_FORMS.get(content_type)

        # Checks if attachments are allowed for given content type
        context['attachment_allowed'] = content_type in IMAGE_ATTACHMENT_TYPES

        # Checks if content type is of type Markdown
        context['is_markdown_content'] = content_type == 'MD'

        # Checks if content type is of type YouTubeVideo
        context['is_yt_content'] = content_type == 'YouTubeVideo'

        # Checks if content type is of type Latex
        context['is_latex_content'] = content_type == 'Latex'

        if content_type == 'Latex':
            context['latex_tooltip'] = LATEX_EXAMPLE

        # Retrieves parameters
        course = Course.objects.get(pk=self.kwargs['course_id'])
        context['course'] = course

        # Topic
        context['topic'] = Topic.objects.get(pk=self.kwargs['topic_id'])

        # Setup formset
        if 'item_forms' not in context:
            formset = ImageAttachmentFormSet(queryset=ImageAttachment.objects.none())
            context['item_forms'] = formset

        return context

    def post(self, request, *args, **kwargs):
        """Post

        Defines the action after a post request.

        :param request: The given request
        :type request: HttpRequest
        :param args: The arguments
        :type args: Any
        :param kwargs: The keyword arguments
        :type kwargs: dict[str, Any]

        :return: the response after a post request
        :rtype: HttpResponseRedirect
        """
        if 'latex-preview' in request.POST and request.is_ajax():
            return latex_preview(request, get_user(request),
                                 Topic.objects.get(pk=self.kwargs['topic_id']),
                                 LatexPreviewImageAttachmentFormSet(request.POST, request.FILES))

        # Retrieves content type form
        if 'type' in self.kwargs:
            content_type = self.kwargs['type']
            if content_type in CONTENT_TYPE_FORMS:
                content_type_form = CONTENT_TYPE_FORMS.get(content_type)(request.POST,
                                                                         request.FILES)
            else:
                return self.handle_error()
        else:
            return self.handle_error()

        # Reads input from included forms
        add_content_form = AddContentForm(request.POST)
        image_formset = ImageAttachmentFormSet(request.POST, request.FILES)

        # Checks if content forms are valid
        if add_content_form.is_valid() and content_type_form.is_valid():

            # Saves author etc.
            content = add_content_form.save(commit=False)
            content.author = get_user(self.request)
            topic_id = self.kwargs['topic_id']
            content.topic = Topic.objects.get(pk=topic_id)
            content.type = content_type
            content.save()
            # Evaluates generic form
            content_type_data = content_type_form.save(commit=False)

            content_type_data.content = content
            content_type_data.save()

            # Checks if attachments are allowed for the given content type
            if content_type in IMAGE_ATTACHMENT_TYPES:
                # Validates attachments
                redirect = Validator.validate_attachment(content,
                                                         image_formset)
                if redirect is not None:
                    return redirect

            # If the content type is LaTeX, compile the LaTeX Code and store in DB
            if content_type == 'Latex':
                Validator.validate_latex(get_user(request),
                                         content,
                                         content_type_data)

            # If the content type is MD store in DB, is_file checks if there is a md file
            # so validator knows if it needs to create a md file or text
            if content_type == 'MD':
                is_file = content_type_form.cleaned_data['options'] == 'file'
                Validator.validate_md(get_user(request),
                                      content,
                                      content_type_data,
                                      is_file)

            # Generates preview image in 'uploads/contents/'
            preview = CONTENT_TYPES.get(content_type).objects.get(pk=content.pk).generate_preview()
            content.preview.name = preview
            content.save()

            # Redirects to content
            course_id = self.kwargs['course_id']
            topic_id = self.kwargs['topic_id']
            return HttpResponseRedirect(reverse_lazy(
                'frontend:content',
                args=(course_id,
                      topic_id,
                      content.id)))

        return self.render_to_response(
            self.get_context_data(form=add_content_form, content_type_form=content_type_form,
                                  item_forms=image_formset))


class EditContentView(LoginRequiredMixin, UpdateView):
    """Edit content view

    This model represents the edit of a content view.

    :attr EditContentView.model: The model of the view
    :type EditContentView.model: Model
    :attr EditContentView.template_name: The path to the html template
    :type EditContentView.template_name: str
    :attr EditContentView.form_class: The form class of the view
    :type EditContentView.form_class: Form
    """
    model = Content
    template_name = 'frontend/content/edit.html'
    form_class = EditContentForm

    def get_content_url(self):
        """Content url

        Gets the url of the content page.

        :return: url of the content page
        :rtype: None or str
        """
        course_id = self.kwargs['course_id']
        topic_id = self.kwargs['topic_id']
        content_id = self.get_object().pk
        return reverse('frontend:content', args=(course_id, topic_id, content_id,))

    def get_success_url(self):
        """Success URL

        Returns the url for successful editing.

        :return: the url of the edited content
        :rtype: None or str
        """
        return self.get_content_url()

    def dispatch(self, request, *args, **kwargs):
        """Dispatch

        Dispatches the edit content view.

        :param request: The given request
        :type request: HttpRequest
        :param args: The arguments
        :type args: Any
        :param kwargs: The keyword arguments
        :type kwargs: dict[str, Any]

        :return: the redirection page of the dispatch
        :rtype: HttpResponse
        """
        user = get_user(request)
        if self.get_object().readonly:
            # Only admins and the content owner can edit the content
            if self.get_object().author == user or request.user.is_superuser:
                return super().dispatch(request, *args, **kwargs)
            messages.error(request, _('You are not allowed to edit this content'))
            return HttpResponseRedirect(self.get_content_url())
        # Everyone can edit the content
        return super().dispatch(request, *args, **kwargs)

    def handle_error(self):
        """Error handling

        Creates error message and return to course page.

        :return: to the course page.
        :rtype: HttpResponseRedirect
        """
        course_id = self.kwargs['course_id']
        messages.error(self.request, _('An error occurred while processing the request'))
        return HttpResponseRedirect(reverse('frontend:course', args=(course_id,)))

    def get_context_data(self, **kwargs):
        """Context data

        Gets the context data of the view which can be accessed in
        the html templates.

        :param kwargs: The additional arguments
        :type kwargs: dict[str, Any]

        :return: the context data
        :rtype: dict[str, Any]
        """
        content = self.get_object()
        context = super().get_context_data(**kwargs)
        context['course_id'] = self.kwargs['course_id']
        context['topic_id'] = self.kwargs['topic_id']
        content_type = self.get_object().type

        # Topic
        context['topic'] = Topic.objects.get(pk=self.kwargs['topic_id'])

        # Adds the form only to context data if not already in it
        # (when passed by post method containing error messages)
        if 'content_type_form' not in context:
            if content_type in CONTENT_TYPE_FORMS:
                content_file = CONTENT_TYPES[content_type].objects.get(pk=self.get_object().pk)
                # if content is MD and there exists an md file in DB for it,
                # get EditMD so the user can't edit the md file.
                if content.type == "MD":
                    if content.mdcontent.md:
                        context['content_type_form'] = \
                            EditMD(instance=content_file)
                else:
                    context['content_type_form'] = \
                        CONTENT_TYPE_FORMS.get(content_type)(instance=content_file)

        # Checks if attachments are allowed for given content type
        context['attachment_allowed'] = content_type in IMAGE_ATTACHMENT_TYPES

        # Checks if content type is of type Latex
        context['is_latex_content'] = content_type == 'Latex'
        # Checks if content type if of type MDContent
        context['is_markdown_content'] = content_type == 'MD'
        # Checks if content type is of type YouTube
        context['is_yt_content'] = content_type == 'YouTubeVideo'
        if content_type == 'Latex':
            context['latex_tooltip'] = LATEX_EXAMPLE

        if content_type in IMAGE_ATTACHMENT_TYPES and 'item_forms' not in context:

            # Identifies the pk's of attached images
            pk_set = []
            for image in self.get_object().ImageAttachments.all():
                pk_set.append(image.pk)

            # Setups the formset with attached images
            formset = ImageAttachmentFormSet(
                queryset=ImageAttachment.objects.filter(pk__in=pk_set))
            context['item_forms'] = formset

        return context

    def post(self, request, *args, **kwargs):
        """Post

        Defines the action after a post request.

        :param request: The given request
        :type request: HttpRequest
        :param args: The arguments
        :type args: Any
        :param kwargs: The keyword arguments
        :type kwargs: dict[str, Any]

        :return: the response after a post request
        :rtype: HttpResponseRedirect
        """
        self.object = self.get_object()
        form = self.get_form()

        if self.object.type in CONTENT_TYPE_FORMS:

            # Bind/init form with existing data
            content_object = CONTENT_TYPES[self.object.type].objects.get(pk=self.get_object().pk)

            # Careful: Order is important for file fields (instance first, afterwards form data,
            # if using kwargs dict as single argument instead, instance information
            # will not be parsed in time)
            content_type_form = CONTENT_TYPE_FORMS.get(self.object.type)(instance=content_object,
                                                                         data=self.request.POST,
                                                                         files=self.request.FILES)
            if self.object.type == "MD":
                content_type_form = EditMD(instance=content_object,
                                           data=self.request.POST,
                                           files=self.request.FILES)

            # Reversion comment
            Reversion.update_comment(request)
            image_formset = ImageAttachmentFormSet(
                data=request.POST,
                files=request.FILES)

            # Check form validity and update both forms/associated models
            if form.is_valid() and content_type_form.is_valid():
                content = form.save()
                content_type = content.type
                content_type_data = content_type_form.save()

                # Checks if attachments are allowed for the given content type
                if content_type in IMAGE_ATTACHMENT_TYPES:

                    # Removes images from database
                    clean_attachment(content, image_formset)

                    # Validates attachments
                    redirect = Validator.validate_attachment(content,
                                                             image_formset)
                    if redirect is not None:
                        return redirect

                # If the content type is LaTeX, compile the LaTeX Code and store in DB
                if content_type == 'Latex':
                    Validator.validate_latex(get_user(request),
                                             content,
                                             content_type_data)

                # If the content type is MD, compile an HTML version of it and store in DB
                if content_type == 'MD':
                    Validator.validate_md(get_user(request),
                                          content,
                                          content_type_data,
                                          False)

                # Generates preview image in 'uploads/contents/'
                preview = CONTENT_TYPES.get(content_type) \
                    .objects.get(pk=content.pk).generate_preview()
                content.preview.name = preview
                content.save()

                messages.add_message(self.request, messages.SUCCESS, _("Content updated"))
                return HttpResponseRedirect(self.get_success_url())

            # Don't save and render error messages for both forms
            return self.render_to_response(
                self.get_context_data(form=form,
                                      content_type_form=content_type_form,
                                      item_forms=image_formset))

        # Redirect to error page (should not happen for valid content types)
        return self.handle_error()


class ContentView(DetailView):
    """Content view

    Displays the content to the user

    :attr ContentView.model: The model of the view
    :type ContentView.model: Model
    :attr ContentView.template_name: The path to the html template
    :type ContentView.template_name: str
    :attr ContentView.context_object_name: The name of the context variable
    :type ContentView.context_object_name: str
    """
    model = Content
    template_name = "frontend/content/detail.html"

    context_object_name = 'content'

    def post(self, request, *args, **kwargs):  # pylint: disable=unused-argument
        """Post

        Defines the action after a post request.

        :param request: The given request
        :type request: HttpRequest
        :param args: The arguments
        :type args: Any
        :param kwargs: The keyword arguments
        :type kwargs: dict[str, Any]

        :return: the response after a post request
        :rtype: HttpResponseRedirect
        """
        comment_form = CommentForm(request.POST)
        translate_form = TranslateForm(request.POST)
        self.object = self.get_object()

        if comment_form.is_valid():
            text = comment_form.cleaned_data['text']
            Comment.objects.create(content=self.get_object(), creation_date=timezone.now(),
                                   author=request.user.profile, text=text)
        elif translate_form.is_valid():
            language = translate_form.cleaned_data['translation']
            context = self.get_context_data(**kwargs)
            # Gets original content
            content = self.object
            r"""
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
        """Context data

        Gets the context data of the view which can be accessed in
        the html templates.

        :param kwargs: The additional arguments
        :type kwargs: dict[str, Any]

        :return: the context data
        :rtype: dict[str, Any]
        """
        context = super().get_context_data(**kwargs)
        context['search_result'] = self.request.GET.get('q')
        content = self.get_object()
        context['user'] = self.request.user
        context['count'] = content.get_rate_count()
        context['rate'] = round(content.get_rate(), 2)

        # Course id for back to course button
        course_id = self.kwargs['course_id']

        course = Course.objects.get(pk=course_id)
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
                context['markdown'] = html"""

        if content.type == "MD":
            md_text = content.mdcontent.textfield
            context['html'] = md_to_html(md_text, content)

        if content.type == 'YouTubeVideo':
            seconds_total = content.ytvideocontent.startTime
            context['start_hours'], context['start_minutes'], context['start_seconds'] = seconds_to_time(seconds_total)

            seconds_total = content.ytvideocontent.endTime
            if (seconds_total == 0):
                context['end_hours'], context['end_minutes'], context['end_seconds'] = seconds_to_time(
                    get_video_length(content.ytvideocontent.id))
            else:
                context['end_hours'], context['end_minutes'], context['end_seconds'] = seconds_to_time(seconds_total)

            context['length'] = get_video_length(content.ytvideocontent.id)

        context['comment_form'] = CommentForm()

        context['comments'] = Comment.objects.filter(content=self.get_object()
                                                     ).order_by('-creation_date')
        context['translate_form'] = TranslateForm()

        if self.request.GET.get('coursebook'):
            context['ending'] = '?coursebook=True'
        elif self.request.GET.get('s'):
            context['ending'] = '?s=' + self.request.GET.get('s') + "&f=" \
                                + self.request.GET.get('f')

        if self.request.user.is_authenticated:
            context['user_rate'] = content.get_user_rate(self.request.user.profile)

        context['favorite'] = Favorite.objects.filter(course=course, user=get_user(self.request),
                                                      content=content).count() > 0

        return context


class AttachedImageView(DetailView):
    """Attached image view

    Displays the attached image to the user.

    :attr AttachedImageView.model: The model of the view
    :type AttachedImageView.model: Model
    :attr AttachedImageView.template_name: The path to the html template
    :type AttachedImageView.template_name: str
    :attr AttachedImageView.context_object_name: The name of the context variable
    :type AttachedImageView.context_object_name: str
    """
    model = ImageAttachment
    template_name = "content/view/AttachedImage.html"

    context_object_name = 'ImageAttachment'

    def get_context_data(self, **kwargs):
        """Context data

        Gets the context data of the view which can be accessed in
        the html templates.

        :param kwargs: The additional arguments
        :type kwargs: dict[str, Any]

        :return: the context data
        :rtype: dict[str, Any]
        """
        context = super().get_context_data(**kwargs)

        # retrieve parameters
        course = Course.objects.get(pk=self.kwargs['course_id'])
        context['course'] = course

        topic = Topic.objects.get(pk=self.kwargs['topic_id'])
        context['topic'] = topic

        content = Content.objects.get(pk=self.kwargs['content_id'])
        context['content'] = content

        context['isCurrentUserOwner'] = self.request.user.profile in course.owners.all()
        context['translate_form'] = TranslateForm()

        return context


class DeleteContentView(LoginRequiredMixin, DeleteView):
    """Delete content view

    Deletes the content and redirects to course.

    :attr DeleteContentView.model: The model of the view
    :type DeleteContentView.model: Model
    :attr DeleteContentView.template_name: The path to the html template
    :type DeleteContentView.template_name: str
    """
    model = Content
    template_name = "frontend/content/detail.html"

    def get_content_url(self):
        """Content url

        Gets the url of the content page.

        :return: the url of the content page
        :rtype: None or str
        """
        course_id = self.kwargs['course_id']
        topic_id = self.kwargs['topic_id']
        content_id = self.get_object().pk
        return reverse('frontend:content', args=(course_id, topic_id, content_id,))

    def get_success_url(self):
        """Success URL

        Returns the url to return to after successful delete

        :return: the url of the edited content
        :rtype: __proxy__
        """
        course_id = self.kwargs['course_id']
        return reverse_lazy('frontend:course', args=(course_id,))

    def dispatch(self, request, *args, **kwargs):
        """Dispatch

        Checks if the user is allowed to view the delete page.

        :param request: The given request
        :type request: HttpRequest
        :param args: The arguments
        :type args: Any
        :param kwargs: The keyword arguments
        :type kwargs: dict[str, Any]

        :return: the response to redirect to overview of the course if the user is not owner
        :rtype: HttpResponse
        """
        user = get_user(request)
        # only admins and the content owner can delete the content
        if self.get_object().author == user or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        messages.error(request, _('You are not allowed to delete this content'))
        return HttpResponseRedirect(self.get_content_url())

    def delete(self, request, *args, **kwargs):
        """Delete

        Deletes the content when the user clicks the delete button.

        :param request: The given request
        :attr request: HttpRequest
        :param args: The arguments
        :type args: Any
        :param kwargs: The keyword arguments
        :type kwargs: dict[str, Any]

        :return: the redirect to success url (course)
        :rtype: HttpResponse
        """

        # Sends the success message
        messages.success(request, "Content successfully deleted", extra_tags="alert-success")

        return super().delete(self, request, *args, **kwargs)


class ContentReadingModeView(LoginRequiredMixin, DetailView):
    """Content reading mode view

    Displays the content to the user.

    :attr ContentReadingModeView.model: The model of the view
    :type ContentReadingModeView.model: Model
    :attr ContentReadingModeView.template_name: The path to the html template
    :type ContentReadingModeView.template_name: str
    """
    model = Content
    template_name = "frontend/content/reading_mode.html"

    def get_context_data(self, **kwargs):
        """Context data

        Gets the context data of the view which can be accessed in
        the html templates.

        :param kwargs: The additional arguments
        :type kwargs: dict[str, Any]

        :return: the context data
        :rtype: dict[str, Any]
        """
        context = super().get_context_data(**kwargs)
        context['course_id'] = self.kwargs['course_id']
        context['topic_id'] = topic_id = self.kwargs['topic_id']
        content = self.get_object()

        topic = Topic.objects.get(pk=topic_id)
        if self.request.GET.get('coursebook'):
            course = get_object_or_404(Course, {"pk": self.kwargs['course_id']})
            contents = [
                f.content for f in Favorite.objects.filter(
                    course=course,
                    user=self.request.user.profile)]  # models
            # .get_coursebook_flat(get_user(self.request), course)
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

        if content.type == "MD":
            md_text = content.mdcontent.textfield
            context['html'] = md_to_html(md_text, content)

        return context
