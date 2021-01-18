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

    Attributes:
        DeleteComment.model (Model): The model of the view
        DeleteComment.template_name (str): The path to the html template
        DeleteComment.context_object_name (str): The context object name
    """
    model = Comment
    template_name = 'frontend/comment/delete_confirm.html'
    context_object_name = 'comment'

    # check if the user is allowed to view the delete page
    def dispatch(self, request, *args, **kwargs):
        """Dispatch

        Checks whether a user has permission to view the delete page.

        Parameters:
            request (HttpRequest): The given request
            args: The arguments
            kwargs (dict): The additional arguments

        return: If user has no permission he will be redirected to the no permission page
        otherwise the dispatch from DeleteView is called and the result is returned
        rtype: HttpResponse
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

        Returns the url for successful delete.

        return: The url of the content to which the deleted argument
        belonged with tag to the comment section
        rtype: str
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

        Gets the context data and adds course id to it

        Parameters:
            kwargs (dict): The arguments

        return: The context data to which the course_id was added
        rtype: dict
        """
        context = super().get_context_data(**kwargs)
        context['course_id'] = self.kwargs['course_id']
        topic = Topic.objects.get(pk=self.kwargs['topic_id'])
        context['topic'] = topic

        return context


class EditComment(LoginRequiredMixin, UpdateView):  # pylint: disable=too-many-ancestors
    """Edit comment

    This model represents the editing of a comment in the database.

    Attributes:
        EditComment.model (Model): The model of the view
        EditComment.template_name (str): The path to the html template
        EditComment.context_object_name (str): The context object name
        EditComment.form_class (ModelForm): THe form of the view
    """
    model = Comment
    template_name = 'frontend/comment/edit.html'
    context_object_name = 'comment'
    form_class = CommentForm

    def form_valid(self, form):
        """Form validation

        Checks whether the form is valid. And saves the entered comment.

        Parameters:
            form (CommentForm): The form that should be checked

        return: The user is redirected to the content page at the comment section
        rtype: HttpResponse
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

        Checks if the user is the author and therefore has permission to change the comment.

        Parameters:
            request (HttpRequest): THe given request
            args: The arguments
            kwargs (dict): The keyword arguments

        return: If the user is the author the dispatch from UpdateView is called, otherwise the
        no permission page will be displayed
        rtype: HttpResponse
        """
        comment = self.get_object()
        if comment.author != self.request.user.profile:
            messages.error(request, _("You don't have permission to do this."),
                           extra_tags="alert-danger")
            course_id = self.kwargs['course_id']
            topic_id = self.kwargs['topic_id']
            return HttpResponseRedirect(reverse('frontend:content', args=(course_id, topic_id,
                                                                          comment.content.id,)))
        return super(EditComment, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Context data

        Gets context data and adds the course_id

        Parameters:
             kwargs (dict): The keyword arguments

        return: The context data with added course_id
        :rtype: dict
        """
        context = super().get_context_data(**kwargs)
        context['course_id'] = self.kwargs['course_id']
        topic = Topic.objects.get(pk=self.kwargs['topic_id'])
        context['topic'] = topic

        return context
