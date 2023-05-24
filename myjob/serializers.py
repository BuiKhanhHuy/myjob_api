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

    def create(self, validated_data):
        request = self.context['request']
        feedback = Feedback.objects.create(**validated_data, user=request.user)
        return feedback

    class Meta:
        model = Feedback
        fields = ('id', 'content', 'rating', 'isActive', 'userDict')


class BannerSerializer(serializers.ModelSerializer):
    imageUrl = serializers.URLField(source="image_url", read_only=True)
    imageMobileUrl = serializers.URLField(source="image_mobile_url", read_only=True)
    buttonText = serializers.CharField(source='button_text', read_only=True)
    description = serializers.CharField(read_only=True)
    buttonLink = serializers.URLField(source="button_link", read_only=True)
    isShowButton = serializers.BooleanField(source='is_show_button', read_only=True)
    isActive = serializers.BooleanField(source='is_active', read_only=True)
    descriptionLocation = serializers.IntegerField(source='description_location', read_only=True)

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
        fields = ('id', 'imageUrl', 'imageMobileUrl',
                  'buttonText', 'description',
                  'buttonLink', 'isShowButton',
                  'isActive', 'descriptionLocation')
