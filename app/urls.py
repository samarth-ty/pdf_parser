from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_form, name='saveInfo'),
    path('upload/', views.upload),
]