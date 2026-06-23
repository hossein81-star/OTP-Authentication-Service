from django.urls import path
from .views.register import UserRegisterApi
from .views.login import UserLoginOtpApi
from .views.logout import UserLogoutAPI
from .views.send_otp import SendOtpApi

urlpatterns = [
    path("send_otp/",SendOtpApi.as_view(),name="send-otp"),
    path("user_register/",UserRegisterApi.as_view(),name="user-register"),
    path("user_login_with_otp/",UserLoginOtpApi.as_view(),name="user-login-with-otp"),
    path("user_logout",UserLogoutAPI.as_view(), name='user_logout'),

]