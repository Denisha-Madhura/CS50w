from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:entry_name>/', views.entry, name="entry"),
    path('create/', views.create, name = "create"),
    path('wiki/', views.random_page, name='random'),
    path('wiki/', views.search, name = 'search'),
    path("edit/<str:entry_name>/", views.edit, name="edit")
]
