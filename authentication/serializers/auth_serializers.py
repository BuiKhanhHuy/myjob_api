from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from ..models import User
from info.models import JobSeekerProfile


class JobSeekerRegisterSerializer(serializers.ModelSerializer):
    fullName = serializers.CharField(source="full_name", required=True, max_length=100)
    email = serializers.EmailField(required=True, max_length=100,
                                   validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(required=True, max_length=100)
    confirmPassword = serializers.CharField(required=True, max_length=100)

    def validate(self, attrs):
        password = attrs["password"]
        confirm_password = attrs["confirmPassword"]
        if not password == confirm_password:
            raise serializers.ValidationError({"confirmPassword": "Mật khẩu xác nhận không trùng khớp!"})
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirmPassword")
        user = User.objects.create_user(**validated_data)
        JobSeekerProfile.objects.create(user=user)

        return user

    class Meta:
        model = User
        fields = ("fullName", "email", "password", "confirmPassword")
