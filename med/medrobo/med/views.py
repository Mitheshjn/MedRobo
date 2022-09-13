from django.shortcuts import render,HttpResponse,redirect
import numpy as np
from .models import details

# Create your views here.

count = 1
def home(request):
	global count
	count=count
	return render(request, 'home.html',{'count':count})

def results(request):
	return render(request, 'result.html')

def add(request):
	global count 	
	if request.method == "POST":
		if count<=9:
			count=create(request,count)
			print(count)
		elif count>9:
			count=delete()
	return render(request, 'add.html',{'count':count})

def create(request,count):
	if request.method == "POST":
		name = request.POST['name1']
		disease = request.POST['disease1']
		door = request.POST['door1']
		bed = request.POST['bed1']
		med1 = request.POST.get('m1-1')
		med2 = request.POST.get('m2-1')
		med3 = request.POST.get('m3-1')
		med4 = request.POST.get('m4-1')
		#med5 = request.POST.get('m5-1')
		#med6 = request.POST.get('m6-1')
		
	obj=details()
	obj.id=count
	obj.name=name
	obj.disease=disease
	obj.door=door
	obj.bed=bed
	obj.med1=med1
	obj.med2=med2
	obj.med3=med3
	obj.med4=med4
	#obj.med5=med5
	#obj.med6=med6
	obj.save()
	count=count+1
	return count

def delete():
	obj=details.objects.get(id =1)
	obj.delete()
	obj=details.objects.get(id =2)
	obj.delete()
	obj=details.objects.get(id =3)
	obj.delete()
	obj=details.objects.get(id =4)
	obj.delete()
	obj=details.objects.get(id =5)
	obj.delete()
	obj=details.objects.get(id =6)
	obj.delete()
	obj=details.objects.get(id =7)
	obj.delete()
	obj=details.objects.get(id =8)
	obj.delete()
	obj=details.objects.get(id =9)
	obj.delete()

	count=1
	return count

def delete_data(request):
	global count
	obj=details.objects.all()
	for o in obj:
		if o.id != None:
			o.delete()

	count=1
	return redirect('show.html',count)

def show(request):
	data = details.objects.all()
	det={
	"detail_data":data
	}
	return render(request, 'show.html',det)

