from django.db import models
from django.contrib.auth.models import User


class feed(models.Model):
	id=models.IntegerField(primary_key=True)
	author=models.CharField(max_length=50)
	title=models.CharField(max_length=100)
	body=models.TextField()


class UsersModel(models.Model):
	id = models.IntegerField(primary_key=True)
	User = models.ForeignKey(User, on_delete=models.CASCADE)
	UserFirstName = models.CharField(max_length=50, blank=True)
	UserLastName = models.CharField(max_length=50, blank=True)
	UserEmail = models.CharField(max_length=50, blank=True)
	UserPhoneNumber = models.CharField(max_length=10, blank=True)
	UserBirthDate = models.DateTimeField(blank=True)
	UserProfileImage = models.ImageField(upload_to='UserProfileImages/')
	Datetime = models.DateTimeField(auto_now_add=True, blank=True)

	def __str__(self):
		return self.UserFirstName

class ProductsModel(models.Model):
	id=models.IntegerField(primary_key=True)
	User = models.ForeignKey(UsersModel, on_delete=models.CASCADE)
	ProductName = models.CharField(max_length=50, blank=True)
	ProductDescription = models.TextField(blank=True)
	ProductType = models.CharField(max_length=100, blank=True)
	ProductImage = models.ImageField(upload_to='ProductImages/')
	ProductFIle = models.FileField(upload_to='ProductFiles/', blank=True)
	ProductDate = models.DateTimeField(auto_now_add=True, blank=True)

	def __str__(self):
		return self.ProductName

	def split_desc(self):
		return self.ProductDescription[:20]+"..."
	def split_title(self):
		return self.ProductName[:10]+"..."

class UploadProductBulk(models.Model):
	file = models.FileField(upload_to='PRODUCTFILE/')



	

