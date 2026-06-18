from celery import shared_task
from .redis import set_otp_in_cache

import random





@shared_task(ignore_result=True)
def send_otp(phone_number,otp):
    print(f"phone number: {phone_number} otp is: {otp}")
    






