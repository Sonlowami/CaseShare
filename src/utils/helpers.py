import random

def generate_OTP():
    code = ''.join(random.choices('0123456789', k=8))
    return code
