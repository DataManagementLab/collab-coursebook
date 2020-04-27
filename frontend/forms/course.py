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
