import json
from django.conf import settings

redis_client=settings.REDIS_CLIENT

def __otp_key(phone_number):
    return f"phone number otp:{phone_number}"



def is_blocked(count):
    if count < 5:
       return False
    return True    
   

def is_cooldown(phone_number):
   if redis_client.exists(f"otp_cooldown:{phone_number}"):
         return True
   return False

def set_otp_in_cache(phone_number, otp):
    key=__otp_key(phone_number=phone_number)

    redis_client.set(
        f"otp_cooldown:{phone_number}",
        "1",
        ex=600
    )

    redis_client.set(
        key,
        otp,
        ex=600
    )

    


def user_otp_request_count(phone_number):
    key = f"otp:otp_request_count:{phone_number}"
    count = redis_client.incr(key)
    if count == 1:
        redis_client.expire(key, 3600)


def get_user_request_count(phone_number):
    key = f"otp:otp_request_count:{phone_number}"
    if redis_client.exists(key):
        count=redis_client.get(key)
        return int(count)
    return 0  
    
    


        
   
    
def get_otp_from_cache(phone_number):
    key=__otp_key(phone_number=phone_number)
    if redis_client.exists(key):
        otp=redis_client.get(key)
        return otp
    return False
    



def increment_failed_otp_attempts(phone_number):
    key = f"otp:failed_attempts:{phone_number}"

    attempts = redis_client.incr(key)

    if attempts == 1:
        redis_client.expire(key, 3600)

    return attempts
      
    
def get_otp_attempts(phone_number):
    key = f"otp:failed_attempts:{phone_number}"
    if redis_client.exists(key):
        count=redis_client.get(key)
        return int(count)
    return 0 