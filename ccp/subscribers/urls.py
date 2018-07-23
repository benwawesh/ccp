from django.conf.urls import url
from . import views


app_name ='subscribers'
urlpatterns = [
    url(r'^subscribers_list$', views.subscribers_list, name='subscribers_list'),
    url(r'^subscribers_list/(?P<offset>[0-9]+)/$', views.subscribers_list, name='subscribers_list'),

]