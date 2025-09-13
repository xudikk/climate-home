# signals.py
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import ProductImg
import os


@receiver(post_delete, sender=ProductImg)
def delete_image_file(sender, instance, **kwargs):
    """
    ProductImage modeli o'chirilganda unga tegishli faylni media papkasidan o'chiradi.
    """
    if instance.img and os.path.isfile(instance.img.path):
        os.remove(instance.img.path)
