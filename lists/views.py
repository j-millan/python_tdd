from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import List, Item

def home(request):
	return render(request, 'lists/home.html')

def list_view(request):
	items = Item.objects.all()
	return render(request, 'lists/list.html', {'items': items})

def new_list(request):
	list_ = List.objects.create() 
	Item.objects.create(text=request.POST.get('item_text'), list=list_)
	return redirect('/lists/the-only-list-in-the-world/')