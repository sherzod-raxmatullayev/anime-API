
import django_filters
from .models import Animes


class AnimeFilter(django_filters.FilterSet):
    # release_date oralig'i
    release_date_after = django_filters.DateFilter(field_name="release_date", lookup_expr="gte")
    release_date_before = django_filters.DateFilter(field_name="release_date", lookup_expr="lte")

    # created_at oralig'i (date-time bo'lgani uchun DateTimeFilter)
    created_after = django_filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")
    created_before = django_filters.DateTimeFilter(field_name="created_at", lookup_expr="lte")

    # episodes soni oralig'i
    episodes_min = django_filters.NumberFilter(field_name="episodes", lookup_expr="gte")
    episodes_max = django_filters.NumberFilter(field_name="episodes", lookup_expr="lte")

    class Meta:
        model = Animes
        fields = []  # hammasini custom fieldlar bilan boshqaryapmiz


