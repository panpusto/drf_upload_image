from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Image
from .functions import convert_to_thumbnails

@receiver(post_save, sender=Image)
def generate_thumbnails(sender, instance: Image, **kwargs):
    """Generates thumbnails after saving uploaded image to database."""
    convert_to_thumbnails(instance.id)
