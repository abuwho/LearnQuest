from . import models
import random

def generate_code():
    return 1234

def store_code():
    print("Storing in redis")

def send_reset_email(user: models.User) -> None:
    print("Sending email to user")
    

def validate_code(code:int) -> models.User:
    return None

