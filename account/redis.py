import json
from django.conf import settings

redis_client=settings.REDIS_CLIENT

def __user_key(session_id):
    return f"user:{session_id}"

def is_blocked(count):
    if count < 5:
       return False
    return True    
   

def is_cooldown(session_id):
   if redis_client.exists(f"otp_cooldown:{session_id}"):
         return True
   return False

def set_otp_in_cache(session_id, otp):
    print(f"setting otp for {session_id}")

    redis_client.set(
        f"otp_cooldown:{session_id}",
        "1",
        ex=120
    )

    redis_client.set(
        f"otp:{session_id}",
        otp,
        ex=120
    )

    


def user_otp_request_count(phone_number):
    key = f"otp_request_count:{phone_number}"
    count = redis_client.incr(key)
    if count == 1:
        redis_client.expire(key, 3600)


def get_user_request_count(phone_number):
    key = f"otp_request_count:{phone_number}"
    if redis_client.exists(key):
        count=redis_client.get(key)
        return int(count)
    return 0  
    
    

def add_user_to_cache(session_id,phone_number,email,password):
    session_id=__user_key(session_id=session_id)

    if not redis_client.exists(session_id):
        data={
            "phone_number":phone_number,
            "email":email,
            "password":password
        }
        redis_client.setex(session_id,600,json.dumps(data))
        
   
    
   
  
    
