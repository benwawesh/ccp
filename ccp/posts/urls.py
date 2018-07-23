from django.conf.urls import url
from . import views

app_name = 'posts'

urlpatterns = [
    url(r'^create_post_page$', views.create_post_index, name='create_post_page'),
    url(r'^post_results$', views.get_posts, name='post_results'),
    url(r'^up_vote$', views.up_vote, name='up_vote'),
    url(r'^down_vote$', views.down_vote, name='down_vote'),

]