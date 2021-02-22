"""Purpose of this file

This file contains forms associated with the course.
"""

from django import forms
from django.utils.translation import gettext_lazy as _

from base.models import Course, Topic

from content.widgets import ModifiedClearableFileInput


class AddCourseForm(forms.ModelForm):
    """Add course form

    This model represents the add form for adding a course.
    """

    # Default value is -1: if this value gets overwritten the form
    # Edits the existing course with the title in the database

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta options

        This class handles all possible meta options that you can give to this model.

        :attr Meta.model: The model to which this form corresponds
        :type Meta.model: Model
        :attr Meta.fields: Including fields into the form
        :type Meta.fields: list[str]
        """
        model = Course
        fields = ['title', 'description', 'image', 'owners',
                  'restrict_changes', 'category', 'period']
        widgets = {
            'image': ModifiedClearableFileInput(attrs={'required': 'false'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Use better multiple select input for owners
        self.fields["owners"].widget.attrs = {'class': 'chosen-select'}


class EditCourseForm(forms.ModelForm):
    """Edit course form

    This model represents the edit form for editing a course.

    :attr EditCourseForm.change_log: The change log field which contains
    a detailed message what was edited
    :type EditCourseForm.change_log: CharField
    :attr EditCourseForm.fields: Including fields into the form
    :type EditCourseForm.fields: List[str]
    """

    change_log = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={'style': 'height: 35px'}),
        label=_('Change Log')
    )
    field_order = ['title', 'description', 'image',
                   'owners', 'restrict_changes', 'category', 'period', 'change_log']

    # Default value is -1: if this value gets overwritten the form
    # Edits the existing course with the title in the database

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        :attr Meta.model: The model to which this form corresponds
        :type Meta.model: Model
        :attr Meta.field_order: The order of the fields
        :type Meta.field_order: List(str)
        :attr Meta.widgets: Customization of the model form
        :type Meta.widgets: dict[str, Widget]
        """

        model = Course
        fields = ['title', 'description', 'image', 'owners',
                  'restrict_changes', 'category', 'period']
        widgets = {
            'image': ModifiedClearableFileInput(attrs={'required': 'false'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Use better multiple select input for owners
        self.fields["owners"].widget.attrs = {'class': 'chosen-select'}


class FilterAndSortForm(forms.Form):
    """Filter and sort form

    This model represents the add form for entering filter and sorting options.

    :attr FilterAndSortForm.FILTER_CHOICE: The filter choices
    :type FilterAndSortForm.FILTER_CHOICE: list[tuple[str, str]]
    :attr FilterAndSortForm.SORTING_CHOICE: The sorting choices
    :type FilterAndSortForm.SORTING_CHOICE: list[tuple[str, str]]
    :attr FilterAndSortForm.filter: The field to enter the filter choices
    :type FilterAndSortForm.filter: CharField
    :attr FilterAndSortForm.sort: The field to enter the sort choices
    :type FilterAndSortForm.sort: CharField
    """

    FILTER_CHOICE = [('None', '------'), ('Text', _("Text")), ('Image', _("Image")),
                     ('Latex', _("LaTeX-Textfield")), ('YouTube-Video', _("YouTube-Video")),
                     ('PDF', 'PDF')]  # + Content.STYLE
    SORTING_CHOICE = [('None', '-----'), ('Date', _("Date")), ('Rating', _("Rating"))]
    filter = forms.CharField(label=_("Filter by"),
                             widget=forms.Select(choices=FILTER_CHOICE,
                                                 attrs={'class': 'form-control',
                                                        'style': 'width:auto',
                                                        'onchange': 'this.form.submit();'}))
    sort = forms.CharField(label=_("Sort by"),
                           widget=forms.Select(choices=SORTING_CHOICE,
                                               attrs={'class': 'form-control',
                                                      'style': 'width:auto',
                                                      'onchange': 'this.form.submit();'}))


class TopicChooseForm(forms.Form):
    """Topic choose form

    Represents a combo box containing all topics group by category title and ordered by their title.

    :attr TopicChooseForm.topic_name: The combo box
    :type TopicChooseForm.topic_name: ModelChoiceField
    """
    topic_name = forms.ModelChoiceField(required=False,
                                        queryset=Topic.objects.order_by('category__title', 'title'),
                                        label=_('Topics'))


class CreateTopicForm(forms.ModelForm):
    """Create topic form

    Represents a form to create new topics.
    """

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        :attr Meta.model: The model to which this form corresponds
        :type Meta.model: Model
        :attr Meta.fields: Including fields into the form
        :type Meta.fields: List(str)
        """
        model = Topic
        fields = ['title', 'category']
