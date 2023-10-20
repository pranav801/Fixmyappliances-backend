import random
import string

def generate_random_password(password_length=8):
    characters = string.ascii_letters + string.digits + '@&#$'
    password = ''.join(random.choice(characters) for _ in range(password_length))
    
    return password