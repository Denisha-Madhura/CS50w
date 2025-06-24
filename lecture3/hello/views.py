from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'hello/index.html')

def den(request):
    return HttpResponse("Hello Denisha!")

def greet(request, name):
    return render(request, 'hello/greet.html', {
        'name': name.capitalize()
        }
        )# Capitalize the name for better 