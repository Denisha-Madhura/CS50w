from django.shortcuts import render
import datetime

# Create your views here.
def index(request):
    return render(request, 'newYears/index.html',{
        "newyear": datetime.datetime.now().month == 1 and datetime.datetime.now().day == 1,
    })