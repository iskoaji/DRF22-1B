from rest_framework import serializers
from apps.users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "phone", "first_name", "last_name"]

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=20, write_only = True)
    confirm_password = serializers.CharField(max_length=20, write_only=True)
    class Meta:
        model = User
        fields = ["id", "phone", "first_name", "last_name", "password", "confirm_password"]

        def validate(self, attrs):
            if attrs['password'] != attrs['confirm_password']:
                raise serializers.ValidationError({"confirm_password":"Пароли не совпадают"})
            if len(attrs['password']) <8:
                raise serializers.ValidationError({"password": "не менее 8 символов"})
            
        def create(self, validate_data):
            validate_data.pop("confirm_password")
            user = User.objects.create(
                phone = validate_data['phone'],
                first_name = validate_data['first_name'],
                last_name = validate_data['last_name'],
            )
            user.set_password(validate_data['password'])
            user.save()
            return user
