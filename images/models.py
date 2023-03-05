import uuid
import time
import os
from django.db import models
from pathlib import Path
from .validators import validate_time_to_expired


def path_to_upload_img(instance, filename):
    return f"{instance.upload_by.id}/images/{instance.id}/{filename}"


class Image(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    image = models.ImageField(
        upload_to=path_to_upload_img)
    upload_by = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.CASCADE
    )
    upload_date = models.DateField(
        auto_now_add=True)

    def __str__(self):
        return f'{self.upload_date} {self.get_image_name()}'

    def get_image_name(self):
        """
        Gets name of the uploaded file.
        :return: name of file as str
        """
        return Path(f'{self.image}').stem

    @property
    def get_image_url(self):
        return self.image.url

    def get_links_to_display(self):
        user_account_tier = self.upload_by.account_tier

        files_dir = os.path.dirname(self.image.path)
        images =  os.listdir(files_dir)

        thumbnails_to_return = []
        for image in images:
            path_to_images = os.path.join(files_dir[5:], image)
            urls = 'http://127.0.0.1:8000' + path_to_images
            thumbnails_to_return.append(urls)

        if user_account_tier.is_original_file:
            thumbnails_to_return.append(self.image.url)

        return thumbnails_to_return


class ThumbnailSize(models.Model):
    width = models.IntegerField()
    height = models.IntegerField()

    def __str__(self):
        return f'{self.width}x{self.height}'

    def __repr__(self):
        return self.width, self.height


class ExpiringLink(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    image = models.OneToOneField('Image', on_delete=models.CASCADE, unique=True)
    link = models.CharField(max_length=255)
    time_to_expired = models.IntegerField(validators=[validate_time_to_expired])

    def __str__(self):
        return f'{self.image} - {self.link}'

    def is_expired(self):
        current_time = time.time()
        return current_time > self.time_to_expired
