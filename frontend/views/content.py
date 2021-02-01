"""Purpose of this file

"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView

from base.models import Content, Comment, Course, Topic, Favorite
from base.utils import get_user
from content.forms import CONTENT_TYPE_FORMS, AddContentFormAttachedImage, SingleImageFormSet
from content.models import CONTENT_TYPES, IMAGE_ATTACHMENT_TYPES
from content.models import SingleImageAttachment, ImageAttachment
from export.views import generate_pdf_response
from frontend.forms import CommentForm, TranslateForm
from frontend.forms.addcontent import AddContentForm


class AddContentView(SuccessMessageMixin, LoginRequiredMixin, CreateView):  # pylint: disable=too-many-ancestors
    """
    Adds a new content to the database
    """
    model = Content
    template_name = 'frontend/content/addcontent.html'
    form_class = AddContentForm
    success_url = reverse_lazy('frontend:dashboard')
    context_object_name = 'content'

    def get_success_message(self, cleaned_data):
        return _(f"Content '{cleaned_data['type']}' successfully added")

    def handle_error(self):
        """
        create error message and return to course page
        """
        course_id = self.kwargs['course_id']
        messages.error(self.request, _('An error occurred while processing the request'))
        return HttpResponseRedirect(reverse('frontend:course', args=(course_id,)))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # retrieve form for content type
        if "type" in self.kwargs:
            content_type = self.kwargs['type']
            if content_type in CONTENT_TYPE_FORMS:
                context['content_type_form'] = CONTENT_TYPE_FORMS.get(content_type)
            else:
                return self.handle_error()
        else:
            return self.handle_error()

        # check if attachments are allowed for given content type
        context['attachment_allowed'] = content_type in IMAGE_ATTACHMENT_TYPES

        # retrieve attachment_form
        context['attachment_form'] = AddContentFormAttachedImage

        # retrieve parameters
        course = Course.objects.get(pk=self.kwargs['course_id'])
        context['course'] = course

        # setup formset
        formset = SingleImageFormSet(queryset=SingleImageAttachment.objects.none())
        context['item_forms'] = formset

        return context

    def post(self, request, *args, **kwargs):
        # retrieve content type form
        if "type" in self.kwargs:
            content_type = self.kwargs['type']
            if content_type in CONTENT_TYPE_FORMS:
                content_type_form = CONTENT_TYPE_FORMS.get(content_type)(request.POST,
                                                                         request.FILES)
            else:
                return self.handle_error()
        else:
            return self.handle_error()

        # read input from all included forms
        add_content_form = AddContentForm(request.POST)
        attachment_form = AddContentFormAttachedImage(request.POST, request.FILES)
        image_formset = SingleImageFormSet(request.POST, request.FILES)

        # check if content forms are valid
        if add_content_form.is_valid() and content_type_form.is_valid():

            # save author etc.
            content = add_content_form.save(commit=False)
            content.author = get_user(self.request)
            topic_id = self.kwargs['topic_id']
            content.topic = Topic.objects.get(pk=topic_id)
            content.type = content_type
            content.save()

            # evaluate generic form
            content_type_data = content_type_form.save(commit=False)
            content_type_data.content = content
            content_type_data.save()

            # If the content type is Latex, compile the Latex Code and store in DB
            if content_type == 'Latex':
                topic = Topic.objects.get(pk=kwargs['topic_id'])
                pdf = generate_pdf_response(get_user(self.request), topic, content)
                content_type_data.pdf.save(f"{topic}" + ".pdf", ContentFile(pdf))
                content_type_data.save()

            # Check if attachments are allowed for the given content type
            if content_type in IMAGE_ATTACHMENT_TYPES:
                if attachment_form.is_valid():

                    # evaluate the attachment form
                    content_attachment = attachment_form.save(commit=False)
                    content_attachment.save()
                    content.attachment = content_attachment
                    images = []

                    # evaluate all forms of the formset and append to image set
                    if image_formset.is_valid():
                        for form in image_formset:
                            used_form = form.save(commit=False)
                            used_form.save()
                            images.append(used_form)
                    else:
                        return self.form_invalid(image_formset)

                    # store the attached images in DB
                    content.attachment.images.set(images)
                else:
                    return self.form_invalid(attachment_form)

            # generate preview image in 'uploads/contents/'
            preview = CONTENT_TYPES.get(content_type).objects.get(pk=content.pk).generate_preview()
            content.preview.name = preview
            content.save()

            # Redirect to content
            course_id = self.kwargs['course_id']
            topic_id = self.kwargs['topic_id']
            return HttpResponseRedirect(reverse_lazy('frontend:content',
                                                     args=(course_id, topic_id, content.id,)))

        # add_content_form invalid
        if not add_content_form.is_valid():
            return self.form_invalid(add_content_form)
        # content_type_form invalid
        return self.form_invalid(content_type_form)


class EditContentView(LoginRequiredMixin, UpdateView):
    model = Content
    template_name = 'frontend/content/editcontent.html'
    form_class = AddContentForm

    def get_content_url(self):
        """
        get the url of the content page
        :return: url of the content page
        """
        course_id = self.kwargs['course_id']
        topic_id = self.kwargs['topic_id']
        content_id = self.get_object().pk
        return reverse('frontend:content', args=(course_id, topic_id, content_id,))

    def get_success_url(self):
        return self.get_content_url()

    def dispatch(self, request, *args, **kwargs):
        user = get_user(request)
        if self.get_object().readonly:
            # only admins and the content owner can edit the content
            if self.get_object().author == user or request.user.is_superuser:
                return super().dispatch(request, *args, **kwargs)
            else:
                messages.error(request, _('You are not allowed to edit this content'))
                return HttpResponseRedirect(self.get_content_url())
        else:
            # everyone can edit the content
            return super().dispatch(request, *args, **kwargs)

    def handle_error(self):
        """
        create error message and return to course page
        """
        course_id = self.kwargs['course_id']
        messages.error(self.request, _('An error occurred while processing the request'))
        return HttpResponseRedirect(reverse('frontend:course', args=(course_id,)))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course_id'] = self.kwargs['course_id']
        context['topic_id'] = self.kwargs['topic_id']

        # Add form only to context data if not already in it
        # (when passed by post method containing error messages)
        if 'content_type_form' not in context:
            content_type = self.get_object().type
            if content_type in CONTENT_TYPE_FORMS:
                content_file = CONTENT_TYPES[content_type].objects.get(pk=self.get_object().pk)
                context['content_type_form'] = \
                    CONTENT_TYPE_FORMS.get(content_type)(instance=content_file)
            else:
                return self.handle_error()

        # check if attachments are allowed for given content type
        context['attachment_allowed'] = content_type in IMAGE_ATTACHMENT_TYPES

        if content_type in IMAGE_ATTACHMENT_TYPES:

            # retrieve attachment_form
            attachment_object = ImageAttachment.objects.get(pk=self.get_object().attachment.pk)
            context['attachment_form'] = AddContentFormAttachedImage(instance=attachment_object)

            # identify pk's of attached pictures
            pkSet = []
            for picture in self.get_object().attachment.images.all():
                pkSet.append(picture.pk)

            # setup formset with attached pictures
            formset = SingleImageFormSet(queryset=SingleImageAttachment.objects.filter(pk__in=pkSet))
            context['item_forms'] = formset

        return context

    def post(self, request, *args, **kwargs):
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

            # Check form validity and update both forms/associated models
            if form.is_valid() and content_type_form.is_valid():
                form.save()
                content = form.save()
                content_type = content.type
                content_object = content_type_form.save()

                # If the content type is Latex, compile the Latex Code and store in DB
                if content_type == 'Latex':
                    topic = Topic.objects.get(pk=kwargs['topic_id'])
                    pdf = generate_pdf_response(get_user(self.request), topic, content)
                    content_object.pdf.save(f"{topic}" + ".pdf", ContentFile(pdf))
                    content_object.save()

                # Check if attachments are allowed for the given content type
                if content_type in IMAGE_ATTACHMENT_TYPES:

                    # Retrieve current state of attachment form and formset
                    attachment_object = ImageAttachment.objects.get(pk=self.get_object().attachment.pk)
                    attachment_form = AddContentFormAttachedImage(instance=attachment_object,
                                                                  data=request.POST,
                                                                  files=request.FILES)
                    image_formset = SingleImageFormSet(data=request.POST,
                                                       files=request.FILES)

                    # Remove images from database
                    clear_counter = attachment_object.images.count() - image_formset.total_form_count()
                    if clear_counter > 0:
                        remove_source = attachment_object.images.order_by('id').reverse()[:clear_counter]
                        for remove_object in remove_source:
                            SingleImageAttachment.objects.filter(pk=remove_object.pk).delete()
                            remove_object.delete()



                    if attachment_form.is_valid():

                        # evaluate the attachment form
                        content_attachment = attachment_form.save(commit=False)
                        content_attachment.save()
                        content.attachment = content_attachment
                        images = []

                        # evaluate all forms of the formset and append to image set
                        if image_formset.is_valid():
                            for form in image_formset:
                                used_form = form.save(commit=False)
                                used_form.save()
                                images.append(used_form)
                        else:
                            return self.form_invalid(image_formset)

                        # store the attached images in DB
                        content.attachment.images.set(images)
                    else:
                        return self.form_invalid(attachment_form)

                preview = CONTENT_TYPES.get(content_type).objects.get(pk=content.pk).generate_preview()
                content.preview.name = preview
                content.save()
                messages.add_message(self.request, messages.SUCCESS, _("Content updated"))
                return HttpResponseRedirect(self.get_success_url())

            # Don't save and render error messages for both forms
            return self.render_to_response(
                self.get_context_data(form=form, content_type_form=content_type_form))

        # Redirect to error page (should not happen for valid content types)
        return self.handle_error()


class ContentView(DetailView):  # pylint: disable=too-many-ancestors
    """
    Displays the content to the user
    """
    model = Content
    template_name = "frontend/content/detail.html"

    context_object_name = 'content'

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
        content = self.get_object()
        context['user'] = self.request.user
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

        context['favorite'] = Favorite.objects.filter(course=course, user=get_user(self.request),
                                                      content=content).count() > 0
        context['attachment'] = content.attachment

        return context


class AttachedImageView(DetailView):
    """
    Displays the attached image to the user
    """
    model = SingleImageAttachment
    template_name = "content/view/AttachedImage.html"

    context_object_name = 'SingleImageAttachment'

    def get_context_data(self, **kwargs):
        """
        get context data
        :param dict kwargs: keyword arguments
        :return: context
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


class DeleteContentView(LoginRequiredMixin, DeleteView):  # pylint: disable=too-many-ancestors
    """
    Deletes the content and redirects to course
    """
    model = Content
    template_name = "frontend/content/detail.html"

    def get_content_url(self):
        """
        get the url of the content page
        :return: url of the content page
        """
        course_id = self.kwargs['course_id']
        topic_id = self.kwargs['topic_id']
        content_id = self.get_object().pk
        return reverse('frontend:content', args=(course_id, topic_id, content_id,))

    def get_success_url(self):
        """
        Returns the url to return to after successful delete
        :return: the success url
        :rtype: str
        """
        course_id = self.kwargs['course_id']
        return reverse_lazy('frontend:course', args=(course_id,))

    # Check if the user is allowed to view the delete page
    def dispatch(self, request, *args, **kwargs):
        """Dispatch

        Overwrites dispatch: Check if a user is allowed to visit the page.

        Parameters:

            request (HttpRequest): The request
            args: The arguments
            kwargs (dict): The keyword arguments

        return: the response to redirect to overview of the course if the user is not owner
        rtype: HttpResponse
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

        Parameters:
            request (HttpRequest): The request
            args: The arguments
            kwargs (dict): The keyword arguments

        return: the redirect to success url (course)
        rtype: HttpResponse
        """

        messages.success(request, "Content successfully deleted", extra_tags="alert-success")
        return super().delete(self, request, *args, **kwargs)


class ContentReadingModeView(LoginRequiredMixin, DetailView):  # pylint: disable=too-many-ancestors
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
            contents = [f.content for f in Favorite.objects
                .filter(course=course,
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


def rate_content(request, course_id, topic_id, content_id, pk):
    """
    Let the user rate content
    :param int topic_id: id of the topic
    :param HttpRequest request: request
    :param int course_id: course id
    :param int content_id: id of the content which gets rated
    :param int pk: the user rating (should be in [ 1, 2, 3, 4, 5])
    :return: redirect to content page
    :rtype: HttpResponse
    """
    content = get_object_or_404(Content, pk=content_id)
    profile = get_user(request)
    content.rate_content(user=profile, rating=pk)

    return HttpResponseRedirect(
        reverse_lazy('frontend:content', args=(course_id, topic_id, content_id,))
        + '#rating')
