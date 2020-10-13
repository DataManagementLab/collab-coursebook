from time import timezone as tz
import datetime
from dal import autocomplete
from base.models import content
from base.utils import get_user


# This class is the Autocomplete used in the Topic Form to determine the structure
class TopicAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = content.Topic.objects.all()
        if self.q:
            qs = qs.filter(title__startswith=self.q)
            print("qs", qs)
            print("q", self.q)
        return qs

    # Creates a new Topic with the given text as title
    def create_object(self, text):
        """Create an object given a text."""
        print("text", text)
        return content.Topic.objects.get_or_create(title=text,
                                                   category=content.Category.objects.get_or_create(title="Default")[
                                                       0])  # todo make change of category possible
