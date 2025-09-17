# signals.py
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import ProductImg, Category
import os


@receiver(post_delete, sender=ProductImg)
def delete_image_file(sender, instance, **kwargs):
    """
    ProductImage modeli o'chirilganda unga tegishli faylni media papkasidan o'chiradi.
    """
    if instance.img and os.path.isfile(instance.img.path):
        os.remove(instance.img.path)



@receiver(post_delete, sender=Category)
def delete_ctg_image_file(sender, instance, **kwargs):
    """
    ProductImage modeli o'chirilganda unga tegishli faylni media papkasidan o'chiradi.
    """
    if instance.img and os.path.isfile(instance.img.path):
        os.remove(instance.img.path)




