from configs import variable_system as var_sys
from django.db.models import Q
import django_filters
from .models import (
    JobPost
)


class JobPostFilter(django_filters.FilterSet):
    kw = django_filters.CharFilter(method="job_name_or_career_name")
    careerId = django_filters.NumberFilter(field_name='career')
    cityId = django_filters.NumberFilter(field_name='location__city')
    positionId = django_filters.ChoiceFilter(choices=var_sys.POSITION_CHOICES, field_name='position')
    experienceId = django_filters.ChoiceFilter(choices=var_sys.EXPERIENCE_CHOICES, field_name='experience')
    typOfWorkplaceId = django_filters.ChoiceFilter(choices=var_sys.TYPE_OF_WORKPLACE_CHOICES,
                                                   field_name='type_of_workplace')
    typeJobId = django_filters.ChoiceFilter(choices=var_sys.JOB_TYPE_CHOICES, field_name='type_job')
    genderId = django_filters.ChoiceFilter(choices=var_sys.GENDER_CHOICES, field_name='gender')
    isUrgent = django_filters.BooleanFilter(field_name='is_urgent')
    excludeSlug = django_filters.CharFilter(method="exclude_slug")

    class Meta:
        model = JobPost
        fields = ['kw', 'careerId', 'cityId', 'positionId',
                  'experienceId', 'typOfWorkplaceId', 'typeJobId',
                  'genderId', 'isUrgent', 'excludeSlug']

    def job_name_or_career_name(self, queryset, name, value):
        return queryset.filter(Q(job_name__icontains=value) | Q(career__name__icontains=value))

    def exclude_slug(self, queryset, name, value):
        return queryset.exclude(slug=value)
