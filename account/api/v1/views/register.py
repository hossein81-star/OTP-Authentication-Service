from rest_framework.views import APIView
from ..serializers.register import UserRegisterSerializer
from drf_spectacular.utils import extend_schema,OpenApiResponse
from ....tasks import send_otp
from rest_framework.response import Response
from rest_framework import status
from ....authentication.redis import is_blocked,get_otp_attempts,delete_user_cached_data

from django.contrib.auth import get_user_model

from django.shortcuts import get_object_or_404
from ....authentication.jwt import create_tokens_for_user
User=get_user_model()


class UserRegisterApi(APIView):
    @extend_schema(
            request=UserRegisterSerializer,
            responses={
                200: OpenApiResponse(description="User Created."),
                400: OpenApiResponse(description="Invalid request"),
            },
            description="User Created.",
    )
    def post(self,request):
        serializer=UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number=serializer.validated_data["phone_number"]
        attemps_otp_field_count=int(get_otp_attempts(phone_number=phone_number))
        user_is_blocked=is_blocked(count=attemps_otp_field_count)
        if not user_is_blocked:
            serializer.save()
            
            
            user=get_object_or_404(User,phone_number=phone_number)
            tokens=create_tokens_for_user(user)
        
            user.phone_verified=True
            user.save()
            delete_user_cached_data(phone_number=phone_number)

            return Response({
                "user": {
                    "id": user.id,
                    "phone_number": str(user.phone_number),
                    "token":tokens
                },
                
            }, status=status.HTTP_201_CREATED)
        
        return  Response(
                    {
                        "message": "you are blocked",
                        "retry_after": 60
                    },
                    status=status.HTTP_429_TOO_MANY_REQUESTS
                )
        
        
      
