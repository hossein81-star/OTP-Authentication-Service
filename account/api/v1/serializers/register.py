from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth import get_user_model
from ....authentication.redis import get_otp_from_cache,increment_failed_otp_attempts
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


User = get_user_model()


class GetUserPhoneNUmberSerializer(serializers.Serializer):
    phone_number = PhoneNumberField()


class UserRegisterSerializer(serializers.Serializer):
    phone_number = PhoneNumberField()
    otp = serializers.CharField(max_length=6)

    def validate_phone_number(self, value):
        
        
        if User.objects.filter(phone_number=str(value)).exists():
            raise serializers.ValidationError(
                "This phone number is already registered."
            )
        return value


    def validate(self, attrs):
        phone_number=attrs["phone_number"]
        cached_otp = get_otp_from_cache(phone_number=phone_number)
        recived_otp=attrs.get("otp")

        if cached_otp is False:
            raise serializers.ValidationError(
                {"otp": "OTP has expired. Please request a new OTP."}
            )
        if cached_otp != recived_otp:
            
         attempts = increment_failed_otp_attempts(phone_number=phone_number)
         if attempts >= 5:
            raise serializers.ValidationError(
                "Too many incorrect OTP attempts. Please request a new OTP."
            )
         raise serializers.ValidationError(
                {"otp": "The OTP entered is incorrect."}
            )

        attrs.pop("otp")
        
        return attrs


    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
