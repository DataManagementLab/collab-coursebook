from django import forms
from django.forms import formset_factory

from base.models.content import Content


from dal import autocomplete

class AddTopicForm(forms.Form):
    """
    Form to add a topic. Used in the formset
    """
    topic_name = forms.ModelChoiceField(required=False, queryset=Content.Topic.objects.all(),  # pylint: disable=no-member
                                        widget=autocomplete.ModelSelect2('select_topic'), label='')


TopicFormset = formset_factory(AddTopicForm, extra=1)