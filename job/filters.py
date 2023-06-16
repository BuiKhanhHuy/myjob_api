from django.core.exceptions import ValidationError
from requests.compat import basestring

from configs import variable_system as var_sys
from helpers import utils
from django.db.models import Q
import django_filters
from rest_framework.filters import OrderingFilter
from .models import (
    JobPost,
    JobPostActivity
)


class JobPostFilter(django_filters.FilterSet):
    kw = django_filters.CharFilter(method="job_name_or_career_name")
    careerId = django_filters.NumberFilter(field_name='career')
    cityId = django_filters.NumberFilter(field_name='location__city')
    positionId = django_filters.ChoiceFilter(choices=var_sys.POSITION_CHOICES, field_name='position')
    experienceId = django_filters.ChoiceFilter(choices=var_sys.EXPERIENCE_CHOICES, field_name='experience')
    typeOfWorkplaceId = django_filters.ChoiceFilter(choices=var_sys.TYPE_OF_WORKPLACE_CHOICES,
                                                    field_name='type_of_workplace')
    jobTypeId = django_filters.ChoiceFilter(choices=var_sys.JOB_TYPE_CHOICES, field_name='job_type')
    genderId = django_filters.ChoiceFilter(choices=var_sys.GENDER_CHOICES, field_name='gender_required')
    isUrgent = django_filters.BooleanFilter(field_name='is_urgent')
    statusId = django_filters.ChoiceFilter(choices=var_sys.JOB_POST_STATUS, field_name="status")
    excludeSlug = django_filters.CharFilter(method="exclude_slug")
    companyId = django_filters.NumberFilter(field_name="company")

    class Meta:
        model = JobPost
        fields = ['kw', 'careerId', 'cityId', 'positionId',
                  'experienceId', 'typeOfWorkplaceId', 'jobTypeId',
                  'genderId', 'isUrgent', 'statusId', 'excludeSlug', 'companyId']

    def job_name_or_career_name(self, queryset, name, value):
        return queryset.filter(Q(job_name__icontains=value) | Q(career__name__icontains=value))

    def exclude_slug(self, queryset, name, value):
        return queryset.exclude(slug=value)


class AliasedOrderingFilter(OrderingFilter):
    """ this allows us to "alias" fields on our model to ensure consistency at the API level
        We do so by allowing the ordering_fields attribute to accept a list of tuples.
        You can mix and match, i.e.:
        ordering_fields = (('alias1', 'field1'), 'field2', ('alias2', 'field2')) """

    def remove_invalid_fields(self, queryset, fields, view, request):
        valid_fields = getattr(view, 'ordering_fields', self.ordering_fields)
        if valid_fields is None or valid_fields == '__all__':
            return super(AliasedOrderingFilter, self).remove_invalid_fields(queryset, fields, view)

        aliased_fields = {}
        for field in valid_fields:
            if isinstance(field, basestring):
                aliased_fields[field] = field
            else:
                aliased_fields[field[0]] = field[1]

        ordering = []
        for raw_field in fields:
            invert = raw_field[0] == '-'
            field = raw_field.lstrip('-')
            if field in aliased_fields:
                if invert:
                    ordering.append('-{}'.format(aliased_fields[field]))
                else:
                    ordering.append(aliased_fields[field])
        return ordering


class EmployerJobPostActivityFilter(django_filters.FilterSet):
    cityId = django_filters.NumberFilter(field_name='resume__city')
    careerId = django_filters.NumberFilter(field_name='resume__career')
    experienceId = django_filters.ChoiceFilter(choices=var_sys.EXPERIENCE_CHOICES,
                                               field_name='resume__experience')
    positionId = django_filters.ChoiceFilter(choices=var_sys.POSITION_CHOICES,
                                             field_name='resume__position')
    academicLevelId = django_filters.ChoiceFilter(choices=var_sys.POSITION_CHOICES,
                                                  field_name='resume__academic_level')
    typeOfWorkplaceId = django_filters.ChoiceFilter(choices=var_sys.TYPE_OF_WORKPLACE_CHOICES,
                                                    field_name='resume__type_of_workplace')
    jobTypeId = django_filters.ChoiceFilter(choices=var_sys.JOB_TYPE_CHOICES,
                                            field_name='resume__job_type')

    genderId = django_filters.ChoiceFilter(choices=var_sys.GENDER_CHOICES,
                                           field_name='resume__job_seeker_profile__gender')
    maritalStatusId = django_filters.ChoiceFilter(choices=var_sys.MARITAL_STATUS_CHOICES,
                                                  field_name="resume__job_seeker_profile__marital_status")

    jobPostId = django_filters.NumberFilter(field_name='job_post')
    status = django_filters.ChoiceFilter(choices=var_sys.APPLICATION_STATUS,
                                         field_name='status')

    class Meta:
        model = JobPostActivity
        fields = [
            'cityId', 'careerId',
            'experienceId', 'positionId',
            'academicLevelId', 'typeOfWorkplaceId',
            'jobTypeId', 'genderId', 'maritalStatusId',
            'jobPostId', 'status'
        ]
