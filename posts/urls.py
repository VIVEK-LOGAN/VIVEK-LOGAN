from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .ajax_views import UploadProductBulkAJAXView

ajax_router = DefaultRouter()
ajax_router.register(r'', UploadProductBulkAJAXView)

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'base_layout', views.base_layout, name='base_layout'),
    path(r'getdata', views.getdata, name='getdata'),
    path(r'createpost', views.createpost, name='createpost'),
    path(r'login', views.LoginView, name='login'),
    path(r'register', views.RegisterView, name='register'),
    path(r'logout', views.LogoutView, name='logout'),
    path(r'myproduct', views.MyProductView, name='myproduct'),
    path(r'updateproduct/<id>', views.updateproduct, name='updateproduct'),
    path(r'deleteproduct/<did>', views.deleteproduct, name='deleteproduct'),
    path(r'async', views.Async, name='async'),
    path(r'upload', views.Upload, name='upload'),
    path(r'^uploadfile', include(ajax_router.urls)),

]
