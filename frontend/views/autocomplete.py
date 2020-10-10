from time import timezone

from dal import autocomplete
from base.models import content

# This class is the Autocomplete used in the Topic Form to determine the structure
class TopicAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return content.Topic.objects.none()
        qs = content.Topic.objects.all()

        if self.q:
            qs = qs.filter(title__startswith=self.q)

        return qs

    # Creates a new Topic with the given text as title
    # creation_date is the current time and author is the logged in user
    def create_object(self, text):
        """Create an object given a text."""
        return content.Topic.objects.get_or_create(title=text, creation_date=timezone.now(), author=content.get_user(self.request))[0]

