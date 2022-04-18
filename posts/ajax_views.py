from rest_framework import viewsets
from .models import UploadProductBulk
from .serializers import RelatedImageSerializer
class UploadProductBulkAJAXView(viewsets.ModelViewSet):
  serializer_class = RelatedImageSerializer
  queryset = UploadProductBulk.objects.all()