"""Purpose of this file

This file contains forms associated with the course.
"""

from django import forms

from base.models import Course


class AddAndEditCourseForm(forms.ModelForm):
    """Add and edit course form

    This model represents the add form for adding and editing a course.
    """

    # Default value is -1: if this value gets overwritten the form
    # Edits the existing course with the title in the database

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta options

        This class handles all possible meta options that you can give to this model.

        Attributes:
            Meta.model (Model): The model to which this form corresponds
            Meta.exclude (List[str]): Excluding fields
        """
        model = Course
        exclude = ['creation_date', 'topics']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Use better multiple select input for owners
        self.fields["owners"].widget.attrs = {'class': 'chosen-select'}


class FilterAndSortForm(forms.Form):
    """Filter and sort form

    This model represents the add form for entering filter and sorting options.

    Attributes:
        FilterAndSortForm.FILTER_CHOICE (List[Tuple[str, str]]): The filter choices
        FilterAndSortForm.SORTING_CHOICE (List[Tuple[str, str]]): The sorting choices
        FilterAndSortForm.filter (CharField): The field to enter the filter choices
        FilterAndSortForm.sort (CharField): The field to enter the sort choices
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
