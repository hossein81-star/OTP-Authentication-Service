from django.urls import path
from .views import SendOtpApi,UserRegisterApi



urlpatterns = [
    path("send_otp/",SendOtpApi.as_view(),name="send-otp"),
    path("user_register/",UserRegisterApi.as_view(),name="user-register"),
]