from django.contrib.auth.models import AbstractUser
import uuid
from django.db import models


class CustomUser(AbstractUser):
    """Representation of the user."""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable = False
    )
    account_tier=models.ForeignKey(
        'AccountTier',
        on_delete = models.SET_NULL,
        null = True
    )

    def __str__(self):
        return self.username


class AccountTier(models.Model):
    """Representation of the account tier."""
    name = models.CharField(max_length=64)
    thumbnail_size = models.ManyToManyField('images.ThumbnailSize', blank=True)
    is_expiring_link = models.BooleanField(
        default=False,
        verbose_name='Generates expiring link')
    is_original_file = models.BooleanField(
        default=False,
        verbose_name='Original file')

    def __str__(self):
        return self.name

    @property
    def get_thumbnail_sizes(self):
        """Gets thumbnail sizes available for account tier."""
        return self.thumbnail_size.all()

    def admin_thumbnail_sizes(self):
        """Readable thumbnail sizes for admin panel."""
        return ', '.join([str(size) for size in self.thumbnail_size.all()])
    admin_thumbnail_sizes.short_description = 'Thumbnail Sizes'
