from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, Currency, Friendship
from django.conf import settings
import boto3
from botocore.client import Config
import re

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'

class UserRegistrationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    mobile_no = serializers.CharField(required=False, allow_blank=True)
    default_currency = serializers.SlugRelatedField(queryset=Currency.objects.all(), slug_field='code', required=False)
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'mobile_no', 'default_currency', 'password', 'password_confirmation']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirmation']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        # if not re.match(r'^[0-9]{10,15}$', attrs.get('mobile_no', '')):
        #     raise serializers.ValidationError({"mobile_no": "Invalid mobile number format."})
        
        return attrs
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password_confirmation')

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user_data = UserRegistrationSerializer(self.user).data
        message = "Login successful."
        data.update({'user': user_data, 'message': message})
        return data
    
class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_confirmation = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirmation']:
            raise serializers.ValidationError({"new_password": "New password fields didn't match."})
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct.")
        return value
    
    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance
    
class UserProfileSerializer(serializers.ModelSerializer):
    default_currency = CurrencySerializer(read_only=True)
    profile_photo = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'mobile_no', 'default_currency', 'profile_photo']

    def get_presigned_url(self, key):
        if not key:
            return None
        
        s3 = boto3.client(
            's3',
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            config=Config(signature_version=settings.AWS_S3_SIGNATURE_VERSION),
        )

        return s3.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                'Key': key,
            },
            ExpiresIn=60 * 60 * 5
        )
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.profile_photo:
            representation['profile_photo'] = self.get_presigned_url(instance.profile_photo.name)
        return representation
        
class UserLookupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']

class FriendshipSerializer(serializers.ModelSerializer):
    from_user = UserRegistrationSerializer(read_only=True)
    to_user = UserRegistrationSerializer(read_only=True)

    class Meta:
        model = Friendship
        fields = '__all__'