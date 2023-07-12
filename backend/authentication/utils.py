from . import models
import random

def generate_code():
    """
    Generate a verification code.

    Returns:
        int: The generated verification code.

    """
    return 1234

def store_code():
    """
    Store the verification code.

    This function can be implemented to store the verification code in a database, cache, or any other storage mechanism.

    """
    print("Storing in redis")

def send_reset_email(user: models.User) -> None:
    """
    Send a password reset email to the user.

    Args:
        user (User): The user model instance.

    """
    print("Sending email to user")
    

def validate_code(code:int) -> models.User:
    """
    Validate the verification code.

    Args:
        code (int): The verification code to validate.

    Returns:
        User: The user model instance if the code is valid, else None.

    """
    return None

