from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'^$', indexView, name='index'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^salir/$', LogOut, name='logout'),
]