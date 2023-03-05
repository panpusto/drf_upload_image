from django.urls import path
from .views import ImageListAPIView, ExpiringLinkAPIView, ExpiringLinkDetailAPIView


urlpatterns = [
    path('images/', ImageListAPIView.as_view(), name='api_image_list'),
    path('expiring_links/', ExpiringLinkAPIView.as_view(), name='api_expiring_link'),
    path('expiring_links/<str:token>/', ExpiringLinkDetailAPIView.as_view(), name='api_expiring_link_detail')
]