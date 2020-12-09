from django import forms

from base.models import Course


class AddAndEditCourseForm(forms.ModelForm):
    """
    The Form for adding and editing a course
    """
    # default value is -1: if this value gets overwritten the form
    # edits the existing course with the title in the database

    class Meta:  # pylint: disable=too-few-public-methods
        model = Course
        exclude = ['creation_date', 'topics']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Use better multiple select input for owners
        self.fields["owners"].widget.attrs = {'class': 'chosen-select'}


class FilterAndSortForm(forms.Form):
    """
    The form for entering filter and sorting Options
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
