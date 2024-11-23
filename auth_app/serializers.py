from rest_framework import serializers
from .models import CustomUser, Module



from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

class UserLoginSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=15, required=True)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        user_id = data.get('user_id')
        password = data.get('password')
        
        if user_id and password:
            user = authenticate(user_id=user_id, password=password)  # This will authenticate the user
            if not user:
                raise serializers.ValidationError("Invalid credentials. Please try again.")
            if not user.is_active:
                raise serializers.ValidationError("This account is inactive.")
        else:
            raise serializers.ValidationError("Both user_id and password are required.")
        
        user.is_active=True
        user.save()
        data['user'] = user
        return data


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['id','user', 'name', 'price', 'description']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'user_id', 'username','password', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_active': {'read_only': True}
        }
        def create(self, validated_data):
            user = CustomUser.objects.create_user(
                user_id=validated_data['user_id'],
                password=validated_data['password'],
                **validated_data
            )
            return user

class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'user_id', 'is_admin', 'is_active']