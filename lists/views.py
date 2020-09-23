from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item

def home(request):
	if request.method == 'POST':
		item = Item.objects.create(text=request.POST.get('item_text'))
		return redirect('home')

	return render(request, 'lists/home.html', {'items': Item.objects.all()})