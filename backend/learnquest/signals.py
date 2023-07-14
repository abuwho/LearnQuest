from django.db.models.signals import post_save
from django.dispatch import receiver
from authentication.models import User
from learnquest.models import Profile, Wallet, Cart

@receiver(post_save, sender=User)
def my_model_post_save(sender, instance, created, **kwargs):
    """
    Create a profile, wallet and cart for the user when the user is created.

    Args:
        sender (User): The User model class.
        instance (User): The User model instance.
        created (bool): A boolean value indicating whether the user was created or not.
        **kwargs: Additional keyword arguments.

    """
    if created:
        profile = Profile(user = instance)
        wallet = Wallet(user = instance)
        cart = Cart(user= instance)
        profile.save()
        wallet.save()
        cart.save()