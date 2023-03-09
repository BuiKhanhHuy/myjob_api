from rest_framework import serializers
from ..models import (
    JobPost
)


class JobPostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields = ('id', 'job_name', 'position', 'job_type',
                  'type_of_workplace', 'experience', 'location', 'careers')


class JobPostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields = ('id',)
