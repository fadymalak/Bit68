from django.db.models.signals import post_save
from django.dispatch import receiver
from shop.models import User, Cart


@receiver(signal=post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    """if new User create Cart obj for him"""
    if created:
        Cart.objects.create(user=instance)
