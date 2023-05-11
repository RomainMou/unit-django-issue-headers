from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("ascii", views.ascii, name='ascii'),
    path("timeout", views.timeout, name='timeout')
]
