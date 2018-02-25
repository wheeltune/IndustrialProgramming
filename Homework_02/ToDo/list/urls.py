from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('markDone', views.markDone, name='markDone'),
    path('remove', views.remove, name='remove'),
]
