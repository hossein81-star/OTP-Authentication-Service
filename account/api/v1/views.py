from rest_framework.views import APIView
from .serializers import UserRegisterSerializer
from drf_spectacular.utils import extend_schema,OpenApiResponse
from ...tasks import send_otp
from rest_framework.response import Response
from rest_framework import status
from ...redis import is_cooldown,is_blocked,user_otp_request_count,add_user_to_cache,set_otp_in_cache,get_user_request_count
from django.contrib.auth.hashers import make_password
import random


# Generate a 6-digit OTP code
def create_otp():
    return('' . join([str(i) for i in sorted([random.randint(0, 9) for _ in range(6)])]))


class SendOtpApi(APIView):

    @extend_schema(
        request=UserRegisterSerializer,
        responses={
            200: OpenApiResponse(description="OTP sent successfully"),
            400: OpenApiResponse(description="Invalid request"),
        },
        description="Send OTP to phone number",
        tags=["Auth"]
    )
    def post(self, request):

        # Ensure session exists for tracking OTP cooldown and user state
        if not request.session.session_key:
            request.session.create()

        session_id = request.session.session_key

        # Validate incoming user registration data
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extract validated user input
        phone_number = str(serializer.validated_data["phone_number"])
        email=serializer.validated_data["email"]
        password=serializer.validated_data["confirm_password"]

        # Hash password before storing it temporarily in cache
        password=make_password(password)

        
        # Get OTP request count for rate limiting per phone number
        user_request_count=get_user_request_count(phone_number=phone_number)

        # Check if user is blocked due to too many OTP requests
        user_is_blocked=is_blocked(count=user_request_count)

        # Check if session is in cooldown period (prevent spam requests)
        user_is_cooldown=is_cooldown(session_id=session_id)
        
        
        
        # Allow OTP generation only if user is not blocked
        if not user_is_blocked:
            
            # Proceed only if cooldown period is not active
            if not user_is_cooldown:

                # Increment OTP request count for this phone number
                user_otp_request_count(phone_number)
                
                
                # Generate OTP code
                otp=create_otp()

                # Store OTP in Redis with expiration (cooldown handling included)
                set_otp_in_cache(session_id=session_id,otp=otp)

                # Temporarily store user data in Redis for later verification step
                add_user_to_cache(session_id=session_id,phone_number=phone_number,email=email,password=password)

                # Trigger asynchronous OTP sending via Celery
                send_otp.delay(
                    otp=otp,
                    phone_number=phone_number
                )

                # Return success response
                return Response(
                    {"message": "OTP sent successfully"},
                    status=status.HTTP_200_OK
                )

            # Return cooldown error response (user must wait before retrying)
            return Response(
                {
                    "message": "tri again befor 60s",
                     "retry_after": 60
                },
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        
            
        # Return blocked response if user exceeded allowed attempts
        else:
            return  Response(
                                {
                                    "message": "you are blocked",
                                    "retry_after": 60
                                },
                                status=status.HTTP_429_TOO_MANY_REQUESTS
                            )