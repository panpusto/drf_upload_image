from rest_framework import serializers
from images.models import Image, ExpiringLink


class ImageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = [
            'image',
        ]


class ImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = [
            'image',
            'get_links_to_display'
        ]


class ExpiringLinkListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpiringLink
        fields = [
            'link'
        ]


class ExpiringLinkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpiringLink
        fields = [
            'image',
            'time_to_expired',
        ]


class ExpiringLinkDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpiringLink
        fields = [
            'link'
        ]