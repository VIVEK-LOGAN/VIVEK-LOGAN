from rest_framework import serializers
from .models import UploadProductBulk
class RelatedImageSerializer(serializers.ModelSerializer):
  class Meta:
    model = UploadProductBulk
    fields = ('file')