import time
import uuid
import hashlib
from rest_framework import generics as g
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from django.http import (
    Http404,
    HttpResponseNotFound,
    HttpResponse,
    FileResponse
)
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.core import signing
from .models import Image, ExpiringLink
from .serializers import (
    ImageListSerializer,
    ImageCreateSerializer,
    ExpiringLinkListSerializer,
    ExpiringLinkCreateSerializer,
    ExpiringLinkDetailSerializer
)
from .permissions import IsAdminOrEnterprise




class ImageListAPIView(g.ListCreateAPIView):
    """Displays list of users images and allows to upload new images."""
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ImageCreateSerializer
        return ImageListSerializer

    def get_queryset(self):
        return Image.objects.filter(upload_by=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(upload_by=self.request.user)



class ExpiringLinkAPIView(g.ListCreateAPIView):
    """Displays list of expiring links and allow to generate new links."""
    permission_classes = [IsAdminOrEnterprise]
    queryset = ExpiringLink.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ExpiringLinkCreateSerializer
        return ExpiringLinkListSerializer

    def list(self, request, *args, **kwargs):
        links = ExpiringLink.objects.filter(image__upload_by=request.user)
        serializer = self.get_serializer_class()(links, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        expiring_link = self.generate_expiring_link(request)
        return Response({'link': expiring_link}, status=status.HTTP_201_CREATED, headers=headers)

    def generate_expiring_link(self, request):
        """Generates new expiring link."""
        image_id = request.data.get('image')
        time_to_expired = int(request.data.get('time_to_expired'))

        salt = str(uuid.uuid4())

        expiration_time = int(time.time()) + time_to_expired
        hash_input = f'{image_id}{expiration_time}{salt}'
        token = hashlib.sha256(hash_input.encode()).hexdigest()

        url = reverse('api_expiring_link_detail', kwargs={'token': token})
        expiring_url = self.request.build_absolute_uri(url)

        image = Image.objects.get(id=image_id)
        ExpiringLink.objects.update(
            link=expiring_url,
            image=image,
            time_to_expired=expiration_time)

        return expiring_url


class ExpiringLinkDetailAPIView(g.RetrieveAPIView):
    """Displays details of expiring link."""
    queryset = ExpiringLink.objects.all()
    permission_classes = [IsAdminOrEnterprise]
    serializer_class = ExpiringLinkDetailSerializer

    def get_object(self):
        try:
            token = self.kwargs.get('token')
            expiring_link_id = signing.loads(token)
            expiring_link = get_object_or_404(self.queryset, pk=expiring_link_id)

            if expiring_link.is_expired():
                expiring_link.delete()
                return HttpResponseNotFound()

            if expiring_link.image.user != self.request.user:
                raise PermissionDenied("User not authorized to view expiring link")

            return expiring_link

        except (ValueError, ExpiringLink.DoesNotExist, signing.BadSignature):
            return HttpResponseNotFound()

