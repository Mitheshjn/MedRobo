from django.db import models

# Create your models here.
class details(models.Model):
	
	name = models.CharField(max_length=20,default='',null=False)
	disease = models.CharField(max_length=20,default='',null=False)
	door = models.CharField(max_length=2,default='',null=False)
	bed = models.CharField(max_length=2,default='',null=False)
	med1 = models.CharField(max_length=3,default='off',blank=True)
	med2 = models.CharField(max_length=3,default='off',blank=True)
	med3 = models.CharField(max_length=3,default='off',blank=True)
	med4 = models.CharField(max_length=3,default='off',blank=True)
	#med5 = models.CharField(max_length=3,default='off',blank=True)
	#med6 = models.CharField(max_length=3,default='off',blank=True)
