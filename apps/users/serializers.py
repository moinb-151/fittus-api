from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, Currency, Friendship
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