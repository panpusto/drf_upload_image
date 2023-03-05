import os
from io import BytesIO
from PIL import Image as PILImage
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Image




def convert_to_thumbnails(pk):
    """Converts uploaded image to thumbnails according to user's account tier."""
    instance = Image.objects.get(id=pk)

    user_tier = instance.upload_by.account_tier
    tier_thumbnails = user_tier.get_thumbnail_sizes
    org_file_path = os.path.abspath(instance.image.url)
    filename, extension = os.path.basename(org_file_path).split('.')

    for size in tier_thumbnails:
        width, height = int(size.width), int(size.height)

        img_file = BytesIO(instance.image.read())
        image = PILImage.open(img_file)

        thumb = image.resize((width, height))
        thumbnail_io = BytesIO()

        thumb.save(
            thumbnail_io,
            format='JPEG' if extension.lower() == 'jpg' else 'PNG',
            quality=100)
        thumbnail_name = f'{filename}_thumb{width}x{height}.{extension}'
        thumb_file = SimpleUploadedFile(
            thumbnail_name,
            thumbnail_io.getvalue(),
            content_type="image/jpg" if extension.lower() == 'jpg' else 'image/png')
        instance.image.save(thumbnail_name, thumb_file, save=False)
