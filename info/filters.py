from django.db.models import Q
import django_filters
from .models import (
    Company
)


class CompanyFilter(django_filters.FilterSet):
    kw = django_filters.CharFilter(method="company_name_or_field_operation")
    cityId = django_filters.NumberFilter(field_name='location__city')
    excludeSlug = django_filters.CharFilter(method="exclude_slug")

    class Meta:
        model = Company
        fields = ['kw', 'cityId', 'excludeSlug']

    def company_name_or_field_operation(self, queryset, name, value):
        return queryset.filter(Q(company_name__icontains=value) | Q(field_operation__icontains=value))

    def exclude_slug(self, queryset, name, value):
        return queryset.exclude(slug=value)
