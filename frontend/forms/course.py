"""Purpose of this file

This file contains forms associated with the course.
"""

from django import forms

from base.models import Course
from content.widgets import ModifiedClearableFileInput


class AddAndEditCourseForm(forms.ModelForm):
    """Add and edit course form

    This model represents the add form for adding and editing a course.
    """

    # Default value is -1: if this value gets overwritten the form
    # Edits the existing course with the title in the database

    # pylint: disable=too-few-public-methods
    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        :attr Meta.model (Model): The model to which this form corresponds
        :type Meta.model: Model
        :attr Meta.fields: Including fields into the form
        :type Meta.fields: List[str]
        """
        model = Course
        fields = ['title', 'description', 'image', 'owners',
                  'restrict_changes', 'category', 'period']
        widgets = {
            'image': ModifiedClearableFileInput(attrs={'required':'false'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Use better multiple select input for owners
        self.fields["owners"].widget.attrs = {'class': 'chosen-select'}


class FilterAndSortForm(forms.Form):
    """Filter and sort form

    This model represents the add form for entering filter and sorting options.

    :attr FilterAndSortForm.FILTER_CHOICE: The filter choices
    :type FilterAndSortForm.FILTER_CHOICE: List[Tuple[str, str]]
    :attr FilterAndSortForm.SORTING_CHOICE: The sorting choices
    :type FilterAndSortForm.SORTING_CHOICE: List[Tuple[str, str]]
    :attr FilterAndSortForm.filter: The field to enter the filter choices
    :type FilterAndSortForm.filter: CharField
    :attr FilterAndSortForm.sort: The field to enter the sort choices
    :type FilterAndSortForm.sort: CharField
    """

    FILTER_CHOICE = [('None', '------')]  # + Content.STYLE
    SORTING_CHOICE = [('None', '-----'), ('creation_date', 'Date'), ('rating', 'Rating')]
    filter = forms.CharField(label='Filter by',
                             widget=forms.Select(choices=FILTER_CHOICE,
                                                 attrs={'class': 'form-control',
                                                        'style': 'width:auto',
                                                        'onchange': 'this.form.submit();'}))
    sort = forms.CharField(label='Sort by',
                           widget=forms.Select(choices=SORTING_CHOICE,
                                               attrs={'class': 'form-control',
                                                      'style': 'width:auto',
                                                      'onchange': 'this.form.submit();'}))
