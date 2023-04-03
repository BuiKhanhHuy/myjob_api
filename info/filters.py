from configs import variable_system as var_sys
from django.db.models import Q
import django_filters
from .models import (
    Company,
    Resume
)


class ResumeFilter(django_filters.FilterSet):
    kw = django_filters.CharFilter(method="title_or_full_name")
    cityId = django_filters.NumberFilter(field_name='city')
    careerId = django_filters.NumberFilter(field_name='career')
    experienceId = django_filters.ChoiceFilter(choices=var_sys.EXPERIENCE_CHOICES,
                                               field_name='experience')
    positionId = django_filters.ChoiceFilter(choices=var_sys.POSITION_CHOICES,
                                             field_name='position')
    academicLevelId = django_filters.ChoiceFilter(choices=var_sys.POSITION_CHOICES,
                                                  field_name='academic_level')
    typeOfWorkplaceId = django_filters.ChoiceFilter(choices=var_sys.TYPE_OF_WORKPLACE_CHOICES,
                                                    field_name='type_of_workplace')
    jobTypeId = django_filters.ChoiceFilter(choices=var_sys.JOB_TYPE_CHOICES,
                                            field_name='job_type')

    genderId = django_filters.ChoiceFilter(choices=var_sys.GENDER_CHOICES,
                                           field_name='job_seeker_profile__gender')
    maritalStatusId = django_filters.ChoiceFilter(choices=var_sys.MARITAL_STATUS_CHOICES,
                                                  field_name="job_seeker_profile__marital_status")

    def title_or_full_name(self, queryset, name, value):
        return queryset.filter(Q(title__icontains=value) | Q(job_seeker_profile__user__full_name__icontains=value))

    class Meta:
        model = Resume
        fields = [
            'kw', 'cityId', 'careerId',
            'experienceId', 'positionId',
            'academicLevelId', 'typeOfWorkplaceId',
            'jobTypeId', 'genderId', 'maritalStatusId'
        ]


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
