try:
    from collections import Counter
except ImportError:
    from backport_collections import Counter
import datetime
from django.db.models import Count

from aldryn_people.models import Person
from parler.managers import TranslatableManager


class RelatedManager(TranslatableManager):

    def get_query_set(self):
        qs = super(RelatedManager, self).get_query_set()
        return qs.select_related('featured_image')

    def get_months(self, namespace):
        """
        Get months with posts count for given namespace string.

        This means how much posts there are in each month. Results are ordered
        by date.
        """

        # This is done in a naive way as Django is having tough time while
        # aggregating on date fields
        entries = self.filter(namespace__namespace=namespace)
        dates = entries.values_list('publishing_date', flat=True)
        dates = [(x.year, x.month) for x in dates]
        date_counter = Counter(dates)
        dates = set(dates)
        dates = sorted(dates, reverse=True)
        months = [
            # Use day=3 to make sure timezone won't affect this hacks'
            # month value. There are UTC+14 and UTC-12 timezones.
            {'date': datetime.date(year=year, month=month, day=3),
             'count': date_counter[(year, month)]}
            for year, month in dates]
        return months

    def get_authors(self, namespace):
        """Get authors with posts count for given namespace string."""

        # This methods relies on the facts that:
        # - each Article has author assigned on save()
        # - Article.namespace.namespace is effectively unique for Article models
        return Person.objects.filter(
            article__namespace__namespace=namespace).annotate(
                num_entries=Count('article'))
