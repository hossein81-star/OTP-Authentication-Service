from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth import get_user_model


User = get_user_model()

class UserRegisterSerializer(serializers.Serializer):
  phone_number=PhoneNumberField()
  email=serializers.EmailField()
  password=serializers.CharField(max_length=255,write_only=True)
  confirm_password=serializers.CharField(max_length=255,write_only=True)
  
  


  def validate(self,attr):
    password=attr.get("password")
    confirm_password=attr.get("confirm_password")
    
    if password != confirm_password:
      raise serializers.ValidationError('Password does not match')
    try:
      validate_password(confirm_password)
    except ValidationError as e:
      raise serializers.ValidationError({"password": list(e.messages)})
    attr.pop("password")
    return attr
 

    
        