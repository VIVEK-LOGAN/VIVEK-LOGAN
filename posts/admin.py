from django.contrib import admin
from .models import *


admin.site.register(UsersModel)
admin.site.register(ProductsModel)
admin.site.register(UploadProductBulk)