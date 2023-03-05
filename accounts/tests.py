from django.test import TestCase
from .models import AccountTier
from django.contrib.auth import get_user_model
from images.models import ThumbnailSize


class AccountsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_basic = get_user_model().objects.create(
            username='basic',
            password='testpass123',
        )
        account_tier = AccountTier.objects.get(name='Basic')
        cls.user_basic.account_tier = account_tier

        cls.user_premium = get_user_model().objects.create(
            username='premium',
            password='testpass123',
        )
        account_tier = AccountTier.objects.get(name='Premium')
        cls.user_premium.account_tier = account_tier

        cls.user_enterprise = get_user_model().objects.create(
            username='enterprise',
            password='testpass123',
        )
        account_tier = AccountTier.objects.get(name='Enterprise')
        cls.user_enterprise.account_tier = account_tier

        cls.thumbnail_size_200 = ThumbnailSize.objects.create(
            width=200,
            height=200
        )

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            username='admin', email='admin@email.com', password='testpass123'
        )
        self.assertEqual(user.username, 'admin')
        self.assertEqual(user.email, 'admin@email.com')
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_user(self):
        user = get_user_model().objects.create(
            username='testuser', email='testuser@email.com', password='testpass123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@email.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_user_account_tier(self):
        self.assertEqual(self.user_basic.account_tier.name, "Basic")
        self.assertEqual(self.user_premium.account_tier.name, "Premium")
        self.assertEqual(self.user_enterprise.account_tier.name, "Enterprise")

    def test_is_original_file(self):
        self.assertFalse(self.user_basic.account_tier.is_original_file)
        self.assertTrue(self.user_premium.account_tier.is_original_file)
        self.assertTrue(self.user_enterprise.account_tier.is_original_file)

    def test_is_expiring_links(self):
        self.assertFalse(self.user_basic.account_tier.is_expiring_link)
        self.assertFalse(self.user_premium.account_tier.is_expiring_link)
        self.assertTrue(self.user_enterprise.account_tier.is_expiring_link)

    def test_create_account_tier(self):
        tier = AccountTier.objects.create(
            name='Premium Plus',
            is_expiring_link=False,
            is_original_file=True
        )
        tier.thumbnail_size.set([self.thumbnail_size_200])
        tier.save()
        self.assertEqual(tier.name, 'Premium Plus')
        self.assertEqual(
            tier.thumbnail_size.first().height,
            self.thumbnail_size_200.height)
        self.assertFalse(tier.is_expiring_link)
        self.assertTrue(tier.is_original_file)