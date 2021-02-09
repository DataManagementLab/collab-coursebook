"""Purpose of this file

This file describes the frontend views related to content types.
"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView

import reversion
from reversion.models import Version
from reversion_compare.forms import SelectDiffForm
from reversion_compare.views import HistoryCompareDetailView

from base.models import Content, Comment, Course, Topic, Favorite
from base.utils import get_user

from content.forms import CONTENT_TYPE_FORMS, AddContentFormAttachedImage, SingleImageFormSet
from content.models import CONTENT_TYPES, IMAGE_ATTACHMENT_TYPES
from content.models import ImageContent, Latex, PDFContent, YTVideoContent
from content.models import SingleImageAttachment, ImageAttachment, TextField

from export.views import generate_pdf_response

from frontend.forms import CommentForm, TranslateForm
from frontend.forms.addcontent import AddContentForm, EditContentForm


def clean_attachment(attachment_object, image_formset):
    """Clean attachment

    Cleans the attachment from the database if the attachments
    were removed from the form.

    :param attachment_object: The attachment object
    :type attachment_object: ImageAttachment
    :param image_formset: The image form set
    :type image_formset: BaseModelFormSet
    """
    clean = attachment_object.images.count() - image_formset.total_form_count()
    if clean > 0:
        remove_source = attachment_object.images.order_by('id').reverse()[:clean]
        for remove_object in remove_source:
            SingleImageAttachment.objects.filter(pk=remove_object.pk).delete()
            remove_object.delete()


# pylint: disable=invalid-name
def rate_content(request, course_id, topic_id, content_id, pk):
    """Rate content

    Let the user rate content.

    :param topic_id: The id of the topic
    :type topic_id: int
    :param request: The given request
    :type request: HttpRequest
    :param course_id: course id
    :type course_id: int
    :param content_id: id of the content which gets rated
    :type content_id: int
    :param pk: the user rating (should be in [ 1, 2, 3, 4, 5])
    :type pk: Any


    :return: the redirect to content page
    :rtype: HttpResponse
    """
    content = get_object_or_404(Content, pk=content_id)
    profile = get_user(request)
    content.rate_content(user=profile, rating=pk)

    return HttpResponseRedirect(
        reverse_lazy('frontend:content', args=(course_id, topic_id, content_id,))
        + '#rating')


def update_comment(request):
    """Update reversion comment

    Gets the comment from the form and updates the comment for the reversion.

    :param request: The given request
    :type request: HttpRequest
    """
    # Reversion comment
    change_log = request.POST.get('change_log')

    # Changes log is not empty set it as comment in reversion,
    # else the default comment message will be used
    if change_log:
        reversion.set_comment(change_log)


def validate_latex(user, content, latex_content, topic_id):
    """Validate LaTeX

    Validates LateX and compiles the LaTeX code and stores its pdf into the database.

    :param user: The current user
    :type user: User
    :param content: The content of the pdf
    :type content: Content
    :param latex_content: The data of the content type
    :type latex_content: Latex
    :param topic_id: The primary key of the topic
    :type topic_id: int
    """
    topic = Topic.objects.get(pk=topic_id)
    pdf = generate_pdf_response(user, topic, content)
    latex_content.pdf.save(f"{topic}" + ".pdf", ContentFile(pdf))
    latex_content.save()


def validate_attachment(view, attachment_form, image_formset, content):
    """Validate attachment

    Validates the image attachments and stores them into the database.

    :param view: The view that wants to validate the data
    :type view: View
    :param attachment_form: The attachment form
    :type attachment_form: ModelForm
    :param image_formset: The image form set
    :type image_formset: BaseModelFormSet
    :param content: The content
    :type content: Content

    :return: the redirection to the invalid page if the image form set or
    the attachment form is not valid
    :rtype: None | HttpResponseRedirect
    """
    if attachment_form.is_valid():
        # Evaluates the attachment form
        content_attachment = attachment_form.save(commit=False)
        content_attachment.save()
        content.attachment = content_attachment
        images = []
        # Evaluates all forms of the formset and append to image set
        if image_formset.is_valid():
            for form in image_formset:
                used_form = form.save(commit=False)
                used_form.save()
                images.append(used_form)
        else:
            return view.form_invalid(image_formset)

        # Stores the attached images in DB
        content.attachment.images.set(images)
        return None

    return view.form_invalid(attachment_form)


# pylint: disable=too-many-ancestors
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
    template_name = 'frontend/content/addcontent.html'
    form_class = AddContentForm
    success_url = reverse_lazy('frontend:dashboard')
    context_object_name = 'content'

    def get_success_message(self, cleaned_data):
        """Success message

        Returns the success message when the profile was updated

        :param cleaned_data: The cleaned data
        :type cleaned_data: dict

        :return: the success message when the profile was updated
        :rtype: __proxy__
        """
        return _(f"Content '{cleaned_data['type']}' successfully added")

    def handle_error(self):
        """
        create error message and return to course page
        """
        course_id = self.kwargs['course_id']
        messages.error(self.request, _('An error occurred while processing the request'))
        return HttpResponseRedirect(reverse('frontend:course', args=(course_id,)))

    def get_context_data(self, **kwargs):
        """Context data

        Returns the context data of the addition of content. If something went wrong,
        redirect to the invalid page.

        :param kwargs: The keyword arguments
        :type kwargs: dict

        :return: the context data of the addition of the content or if something went wrong,
        redirect to the invalid page
        :rtype: Dict[str, Any] | HttpResponseRedirect
         """
        context = super().get_context_data(**kwargs)

        # Retrieves the form for content type
        if "type" in self.kwargs:
            content_type = self.kwargs['type']
            if content_type in CONTENT_TYPE_FORMS:
                context['content_type_form'] = CONTENT_TYPE_FORMS.get(content_type)
            else:
                return self.handle_error()
        else:
            return self.handle_error()

        # Checks if attachments are allowed for given content type
        context['attachment_allowed'] = content_type in IMAGE_ATTACHMENT_TYPES

        # Retrieves attachment_form
        context['attachment_form'] = AddContentFormAttachedImage

        # Retrieves parameters
        course = Course.objects.get(pk=self.kwargs['course_id'])
        context['course'] = course

        # setup formset
        formset = SingleImageFormSet(queryset=SingleImageAttachment.objects.none())
        context['item_forms'] = formset

        return context

    def post(self, request, *args, **kwargs):
        """Post

        Submits the form and its uploaded files to store it into the database.

        :param request: The given request
        :type request: HttpRequest
        :param args: The arguments
        :type args: Any
        :param kwargs: The keyword arguments
        :type kwargs: dict

        :return: the redirection to the content page after the submitting or
        to the invalid page if something wrong occurs
        :rtype: HttpResponseRedirect
        """
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

            # If the content type is Latex, compile the Latex Code and store in DB
            if content_type == 'Latex':
                validate_latex(get_user(request), content, content_type_data, kwargs['topic_id'])

            # Checks if attachments are allowed for the given content type
            if content_type in IMAGE_ATTACHMENT_TYPES:
                # Reads input from all forms
                attachment_form = AddContentFormAttachedImage(request.POST, request.FILES)
                image_formset = SingleImageFormSet(request.POST, request.FILES)

                # Validates attachments
                redirect = validate_attachment(self, attachment_form, image_formset, content)
                if redirect is not None:
                    return redirect

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

        # add_content_form invalid
        if not add_content_form.is_valid():
            return self.form_invalid(add_content_form)
        # content_type_form invalid
        return self.form_invalid(content_type_form)


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
    template_name = 'frontend/content/editcontent.html'
    form_class = EditContentForm

    def get_content_url(self):
        """Content url

        Gets the url of the content page.

        :return: url of the content page
        :rtype: Optional[str]
        """
        course_id = self.kwargs['course_id']
        topic_id = self.kwargs['topic_id']
        content_id = self.get_object().pk
        return reverse('frontend:content', args=(course_id, topic_id, content_id,))

    def get_success_url(self):
        """Success URL

        Returns the url for successful editing.

        :return: the url of the edited content
        :rtype: str
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
        :type kwargs: dict

        :return: the redirection page of the dispatch
        :rtype: HttpResponse
        """
        user = get_user(request)
        if self.get_object().readonly:
            # only admins and the content owner can edit the content
            if self.get_object().author == user or request.user.is_superuser:
                return super().dispatch(request, *args, **kwargs)
            messages.error(request, _('You are not allowed to edit this content'))
            return HttpResponseRedirect(self.get_content_url())
        # everyone can edit the content
        return super().dispatch(request, *args, **kwargs)

    def handle_error(self):
        """Handle error

        Create error message and return to course page.

        :return: the http response redirect of the error handling
        :rtype: HttpResponseRedirect
        """
        course_id = self.kwargs['course_id']
        messages.error(self.request, _('An error occurred while processing the request'))
        return HttpResponseRedirect(reverse('frontend:course', args=(course_id,)))

    def get_context_data(self, **kwargs):
        """Context data

        Returns the context data of the editing.

        :param kwargs: The keyword arguments
        :type kwargs: dict

        :return: the context data of the editing
        :rtype: Dict[str, Any]
        """
        context = super().get_context_data(**kwargs)
        context['course_id'] = self.kwargs['course_id']
        context['topic_id'] = self.kwargs['topic_id']

        # Adds the form only to context data if not already in it
        # (when passed by post method containing error messages)
        if 'content_type_form' not in context:
            content_type = self.get_object().type
            if content_type in CONTENT_TYPE_FORMS:
                content_file = CONTENT_TYPES[content_type].objects.get(pk=self.get_object().pk)
                context['content_type_form'] = \
                    CONTENT_TYPE_FORMS.get(content_type)(instance=content_file)
            else:
                return self.handle_error()

        # Checks if attachments are allowed for given content type
        context['attachment_allowed'] = content_type in IMAGE_ATTACHMENT_TYPES

        if content_type in IMAGE_ATTACHMENT_TYPES:

            # Retrieves attachment_form
            attachment_object = ImageAttachment.objects.get(pk=self.get_object().attachment.pk)
            context['attachment_form'] = AddContentFormAttachedImage(instance=attachment_object)

            # Identifies the pk's of attached images
            pk_set = []
            for picture in self.get_object().attachment.images.all():
                pk_set.append(picture.pk)

            # Setups the formset with attached images
            formset = SingleImageFormSet(
                queryset=SingleImageAttachment.objects.filter(pk__in=pk_set))
            context['item_forms'] = formset

        return context

    def post(self, request, *args, **kwargs):
        """Post

        Submits the form and its uploaded files to store it into the database.

        :param request: The given request
        :type request: HttpRequest
        :param args: The arguments
        :type args: Any
        :param kwargs: The keyword arguments
        :type kwargs: dict

        :return: the redirection to the content page after the submitting or
        to the invalid page if something wrong occurs
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

            # Reversion comment
            update_comment(request)

            # Check form validity and update both forms/associated models
            if form.is_valid() and content_type_form.is_valid():
                content = form.save()
                content_type = content.type
                content_type_data = content_type_form.save()

                # If the content type is Latex, compile the Latex Code and store in DB
                if content_type == 'Latex':
                    validate_latex(get_user(request),
                                   content,
                                   content_type_data,
                                   kwargs['topic_id'])

                # Checks if attachments are allowed for the given content type
                if content_type in IMAGE_ATTACHMENT_TYPES:

                    # Retrieves current state of attachment form and formset
                    attachment_object = ImageAttachment.objects.get(
                        pk=self.get_object().attachment.pk)
                    attachment_form = AddContentFormAttachedImage(
                        instance=attachment_object,
                        data=request.POST,
                        files=request.FILES)
                    image_formset = SingleImageFormSet(
                        data=request.POST,
                        files=request.FILES)

                    # Removes images from database
                    clean_attachment(attachment_object, image_formset)

                    # Validates attachments
                    redirect = validate_attachment(self, attachment_form, image_formset, content)
                    if redirect is not None:
                        return redirect

                # Generates preview image in 'uploads/contents/'
                preview = CONTENT_TYPES.get(content_type) \
                    .objects.get(pk=content.pk).generate_preview()
                content.preview.name = preview
                content.save()

                messages.add_message(self.request, messages.SUCCESS, _("Content updated"))
                return HttpResponseRedirect(self.get_success_url())

            # Don't save and render error messages for both forms
            return self.render_to_response(
                self.get_context_data(form=form, content_type_form=content_type_form))

        # Redirect to error page (should not happen for valid content types)
        return self.handle_error()


# pylint: disable=too-many-ancestors
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

    # pylint: disable=unused-argument
    def post(self, request, *args, **kwargs):
        """Post

        Creates comment in database.

        :param request: The given request
        :type request: HttpResponse
        :param args: The arguments
        :type: Any
        :param kwargs: The keyword arguments
        :type kwargs: dict

        :return: the redirection to the content page
        :rtype: HttpResponse
        """
        comment_form = CommentForm(request.POST)
        translate_form = TranslateForm(request.POST)
        self.object = self.get_object()  # line required

        # pylint: disable=no-member
        if comment_form.is_valid():
            text = comment_form.cleaned_data['text']
            Comment.objects.create(content=self.get_object(), creation_date=timezone.now(),
                                   author=request.user.profile, text=text)
        elif translate_form.is_valid():
            language = translate_form.cleaned_data['translation']
            context = self.get_context_data(**kwargs)
            # get original content
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

        Gets the context data.

        :param kwargs: The keyword arguments
        :type kwargs: dict

        :return: the context data
        :rtype: dict
        """
        context = super().get_context_data(**kwargs)
        context['search_result'] = self.request.GET.get('q')
        content = self.get_object()
        context['user'] = self.request.user
        context['count'] = content.get_rate_count()
        context['rate'] = round(content.get_rate(), 2)

        # course id for back to course button
        course_id = self.kwargs['course_id']
        # pylint: disable=no-member
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
                context['markdown'] = html
        """

        context['comment_form'] = CommentForm()
        # pylint: disable=no-member
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
        context['attachment'] = content.attachment

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
    model = SingleImageAttachment
    template_name = "content/view/AttachedImage.html"

    context_object_name = 'SingleImageAttachment'

    def get_context_data(self, **kwargs):
        """Context data

        Gets the context data.

        :param kwargs: The keyword arguments
        :type kwargs: dict

        :return: the context data
        :rtype: dict
        """
        context = super().get_context_data(**kwargs)

        # retrieve parameters
        course = Course.objects.get(pk=self.kwargs['course_id'])
        context['course'] = course

        topic = Topic.objects.get(pk=self.kwargs['topic_id'])
        context['topic'] = topic

        content = Content.objects.get(pk=self.kwargs['content_id'])
        context['content'] = content

        attachment = ImageAttachment.objects.get(pk=self.kwargs['imageattachment_id'])
        context['attachment'] = attachment

        context['isCurrentUserOwner'] = self.request.user.profile in course.owners.all()
        context['translate_form'] = TranslateForm()

        return context


# pylint: disable=too-many-ancestors
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
        :rtype: optional[str]
        """
        course_id = self.kwargs['course_id']
        topic_id = self.kwargs['topic_id']
        content_id = self.get_object().pk
        return reverse('frontend:content', args=(course_id, topic_id, content_id,))

    def get_success_url(self):
        """Success URL

        Returns the url to return to after successful delete

        :return: the url of the edited content
        :rtype: str
        """
        course_id = self.kwargs['course_id']
        return reverse_lazy('frontend:course', args=(course_id,))

    # Check if the user is allowed to view the delete page
    def dispatch(self, request, *args, **kwargs):
        """Dispatch

        Overwrites dispatch: Check if a user is allowed to visit the page.

        :param request: The given request
        :type request: HttpRequest
        :param args: The arguments
        :type args: Any
        :param kwargs: The keyword arguments
        :type kwargs: dict

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

        Deletes the content when the user clicks the delete button

        :param request: The given request
        :attr request: HttpRequest
        :param args: The arguments
        :type args: Any
        :param kwargs: The keyword arguments
        :type kwargs: dict

        :return: the redirect to success url (course)
        :rtype: HttpResponse
        """

        # Send success message
        messages.success(request, "Content successfully deleted", extra_tags="alert-success")

        if self.get_object().type in IMAGE_ATTACHMENT_TYPES:

            # Retrieve the attachment
            attachment_object = ImageAttachment.objects.get(pk=self.get_object().attachment.pk)

            # Remove the images in the attachment from DB
            for remove_object in attachment_object.images.all():
                SingleImageAttachment.objects.filter(pk=remove_object.pk).delete()
                remove_object.delete()

            # Retrieve the success url, then delete the corresponding attachment
            success_url = super().delete(self, request, *args, **kwargs)
            ImageAttachment.objects.filter(pk=attachment_object.pk).delete()
            attachment_object.delete()
            return success_url

        return super().delete(self, request, *args, **kwargs)


# pylint: disable=too-many-ancestors
class ContentReadingModeView(LoginRequiredMixin, DetailView):
    """Content reading mode view

    Displays the content to the user.

    :attr ContentReadingModeView.model: The model of the view
    :type ContentReadingModeView.model: Model
    :attr ContentReadingModeView.template_name: The path to the html template
    :type ContentReadingModeView.template_name: str
    """
    model = Content
    template_name = "frontend/content/readingmode.html"

    def get_context_data(self, **kwargs):
        """Context data

        Gets the context data for the response.

        :param kwargs: The keyword arguments
        :type kwargs: dict

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
        return context
