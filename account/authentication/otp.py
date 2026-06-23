import random

def create_otp():
    return('' . join([str(i) for i in sorted([random.randint(0, 9) for _ in range(6)])]))