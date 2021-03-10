"""Purpose of this file

This file describes the frontend views related to comments.
"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DeleteView, UpdateView
from django.utils.translation import gettext_lazy as _

from base.models import Comment, Topic

from frontend.forms import CommentForm


class DeleteComment(LoginRequiredMixin, DeleteView):  # pylint: disable=too-many-ancestors
    """Delete comment

    This model represents the deletion of a comment and redirects to course list.

    :attr DeleteComment.model: The model of the view
    :type DeleteComment.model: Model
    :attr DeleteComment.template_name: The path to the html template
    :type DeleteComment.template_name: str
    :attr DeleteComment.context_object_name: The context object name
    :type DeleteComment.context_object_name: str
    """
    model = Comment
    template_name = 'frontend/comment/delete_confirm.html'
    context_object_name = 'comment'

    def dispatch(self, request, *args, **kwargs):
        """Dispatch

        Checks whether a user has permission to view the delete page.

        :param request: The given request
        :type request: HttpRequest
        :param args: The arguments
        :type args: Any
        :param kwargs: The additional arguments
        :type kwargs: dict[str, Any]

        :return: if user has no permission he will be redirected to the no permission page
        otherwise the dispatch from DeleteView is called and the result is returned
        :rtype: HttpResponse
        """
        if self.get_object().author != request.user.profile and not request.user.is_superuser:
            # Back url for no permission page
            messages.error(request, _("You don't have permission to do this."),
                           extra_tags="alert-danger")
            course_id = self.kwargs['course_id']
            topic_id = self.kwargs['topic_id']
            return HttpResponseRedirect(
                reverse('frontend:content',
                        args=(course_id,
                              topic_id,
                              self.get_object().content.id,)))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        """Success URL

        Returns the url for successful deletion of the comment to which the deleted
        argument belonged with tag to the comment section

        :return: the url of the content
        :rtype: str
        """
        course_id = self.kwargs['course_id']
        topic_id = self.kwargs['topic_id']
        messages.success(self.request,
                         _("Successfully deleted comment."),
                         extra_tags="alert-success")
        return reverse('frontend:content',
                       args=(course_id, topic_id,
                             self.get_object().content.id,))

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
        topic = Topic.objects.get(pk=self.kwargs['topic_id'])
        context['topic'] = topic

        return context


class EditComment(LoginRequiredMixin, UpdateView):  # pylint: disable=too-many-ancestors
    """Edit comment

    This model represents the editing of a comment in the database.

    :attr EditComment.model: The model of the view
    :type EditComment.model: Model
    :attr EditComment.template_name: The path to the html template
    :type EditComment.template_name: str
    :attr EditComment.context_object_name: The context object name
    :type EditComment.context_object_name: str
    :attr EditComment.form_class: The form of the view
    :type EditComment.form_class: ModelForm
    """
    model = Comment
    template_name = 'frontend/comment/edit.html'
    context_object_name = 'comment'
    form_class = CommentForm

    def form_valid(self, form):
        """Form validation

        Checks whether the form is valid. If it was valid, save the entered comment.

        :param form: The form that should be checked
        :type form: CommentForm

        :return: the user is redirected to the content page at the comment section
        :rtype: HttpResponse
        """
        comment = form.save(commit=False)
        comment.text = form.cleaned_data['text']
        # comment.last_edited_on_date = timezone.now()
        comment.save()
        course_id = self.kwargs['course_id']
        topic_id = self.kwargs['topic_id']
        messages.success(self.request,
                         _("Successfully edited Comment."),
                         extra_tags="alert-success")
        return HttpResponseRedirect(reverse('frontend:content',
                                            args=(course_id, topic_id,
                                                  comment.content.id,)))

    # Checks if user is the author of the comment
    def dispatch(self, request, *args, **kwargs):
        """Dispatch

        Checks if the user is the author of the comment and therefore has permission to change
        the comment.

        :param request: The given request
        :type request: HttpRequest
        :param args: The arguments
        :type args: Any
        :param kwargs: The keyword arguments
        :type kwargs: dict[str, Any]

        :return: if the user is the author the dispatch from UpdateView is called, otherwise the
        no permission page will be displayed
        :rtype: HttpResponse
        """
        comment = self.get_object()
        if comment.author != self.request.user.profile:
            messages.error(request, _("You don't have permission to do this."),
                           extra_tags="alert-danger")
            course_id = self.kwargs['course_id']
            topic_id = self.kwargs['topic_id']
            return HttpResponseRedirect(reverse('frontend:content', args=(course_id, topic_id,
                                                                          comment.content.id,)))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Context data

        Gets the context data of the view which can be accessed in
        the html templates.

        :param kwargs: The keyword arguments
        :type kwargs: dict[str, Any]

        :return: the context data
        :rtype: dict[str, Any]
        """
        context = super().get_context_data(**kwargs)
        context['course_id'] = self.kwargs['course_id']
        topic = Topic.objects.get(pk=self.kwargs['topic_id'])
        context['topic'] = topic

        return context
