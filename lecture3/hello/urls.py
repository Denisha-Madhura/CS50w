from django.urls import path
from . import views

urlpatterns=[
    path("", views.index, name='index'),
    path("den", views.den, name='denisha'),
    path("<str:name>", views.greet, name='greet')
]