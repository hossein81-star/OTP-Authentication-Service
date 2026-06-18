from django.urls import path
from .views import SendOtpApi



urlpatterns = [
    path("send_otp/",SendOtpApi.as_view(),name="send-otp"),
    

    
]