from django.shortcuts import render
from django.http import HttpResponse

def home(request):
	return HttpResponse('<html><title>To-do list</title></html>')