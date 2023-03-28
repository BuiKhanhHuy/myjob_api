from rest_framework import serializers
from .models import (
    Feedback
)
from authentication import serializers as auth_serializers


class FeedbackSerializer(serializers.ModelSerializer):
    content = serializers.CharField(max_length=255)
    rating = serializers.IntegerField(default=5)
    isActive = serializers.BooleanField(source='is_active', default=False)
    userDict = auth_serializers.UserSerializer(source="user",
                                               fields=['id', 'fullName', 'avatarUrl'],
                                               read_only=True)

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = Feedback
        fields = ('id', 'content', 'rating', 'isActive', 'userDict')
