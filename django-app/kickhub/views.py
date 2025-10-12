from django.shortcuts import render
#from django.http import HttpResponse

# Create your views here.

def index(request):
  context = {
    'page_title': 'Welcome!',
    'message': 'This is a dynamic message from our Django view.',
  }
  return render(request, 'index.html', context)

  
