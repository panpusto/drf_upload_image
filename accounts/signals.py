from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import AccountTier
from images.models import ThumbnailSize
from .builtin_tiers import BUILTIN_TIERS


@receiver(post_migrate)
def create_builtin_tiers(sender, **kwargs):
    """Creates default tiers: Basic, Premium, Enterprise. """
    if sender.name == 'accounts':
        if AccountTier.objects.filter(name='Basic').exists():
            return

        # basic
        basic_tier = AccountTier.objects.create(
            name='Basic',
            is_expiring_link=BUILTIN_TIERS['Basic']['is_expiring_link'],
            is_original_file=BUILTIN_TIERS['Basic']['is_original_file'],
        )
        basic_thumbnail_size = ThumbnailSize.objects.create(
            width=BUILTIN_TIERS['Basic']['thumbnail_size']['width'],
            height=BUILTIN_TIERS['Basic']['thumbnail_size']['width']
        )
        basic_tier.thumbnail_size.add(basic_thumbnail_size)

        # premium
        premium_tier = AccountTier.objects.create(
            name='Premium',
            is_expiring_link=BUILTIN_TIERS['Premium']['is_expiring_link'],
            is_original_file=BUILTIN_TIERS['Premium']['is_original_file']
        )
        premium_thumbnail_size = ThumbnailSize.objects.create(
            width=BUILTIN_TIERS['Premium']['thumbnail_size']['width'],
            height=BUILTIN_TIERS['Premium']['thumbnail_size']['height']
        )
        premium_tier.thumbnail_size.set([basic_thumbnail_size, premium_thumbnail_size])

        # enterprise
        enterprise_tier = AccountTier.objects.create(
            name='Enterprise',
            is_expiring_link=BUILTIN_TIERS['Enterprise']['is_expiring_link'],
            is_original_file=BUILTIN_TIERS['Enterprise']['is_original_file']
        )
        enterprise_tier.thumbnail_size.set([basic_thumbnail_size, premium_thumbnail_size])
