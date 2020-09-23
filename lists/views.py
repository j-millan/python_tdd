from django.shortcuts import render
from django.http import HttpResponse

def home(request):
	context = {}
	if request.method == 'POST':
		context['new_todo_item'] = request.POST.get('item_text')
	return render(request, 'lists/home.html', context)