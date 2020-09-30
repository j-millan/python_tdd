from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from lists.models import List, Item

def home(request):
	return render(request, 'lists/home.html')

def list_view(request, pk):
	list_ = get_object_or_404(List, pk=pk)
	return render(request, 'lists/list.html', {'list': list_})

def new_list(request):
	list_ = List.objects.create() 
	Item.objects.create(text=request.POST.get('item_text'), list=list_)
	return redirect('list_view', pk=list_.pk)

def new_item(request, pk):
	list_ = get_object_or_404(List, pk=pk)
	Item.objects.create(text=request.POST.get('item_text'), list=list_)
	return redirect('list_view', pk=list_.pk)