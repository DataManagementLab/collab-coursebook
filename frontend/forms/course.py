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
        # widgets = {'owners': autocomplete.ModelSelect2Multiple(url='select_many_to_many')}