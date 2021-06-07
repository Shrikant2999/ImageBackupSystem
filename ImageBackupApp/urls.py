
from django.urls import path

from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('upload', views.upload, name='upload'),
    path('allimages', views.allImages, name='allImages'),
    path('download', views.download, name='download'),
    path('delete', views.delete, name='delete')

]