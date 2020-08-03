from pathlib import Path
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from base.models import Course
from export.helper_functions import generate_coursebook_for


def generate_coursebook(request, *args, **kwargs):
    """
    Opens generated coursebook in a new tab
    """
    course_id = kwargs['pk']
    course = Course.objects.get(pk=course_id)
    user = request.user

    generated_file_path = generate_coursebook_for(user, course)
    pdf_file_path = generated_file_path + '.pdf'
    if Path(pdf_file_path).exists():
        with open(pdf_file_path, 'rb') as file_handler:
            response = HttpResponse(file_handler.read(), content_type="application/pdf")
            file_handler.close()
        return response
    messages.error(request, 'There was an error while generating your coursebook.')
    return HttpResponseRedirect(reverse('frontend:course', args=(course_id, )))
