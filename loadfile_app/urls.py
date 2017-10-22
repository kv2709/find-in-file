from django.conf.urls import url
from . import views

urlpatterns = [
    #Home page for work phone-dealer
    url(r'^$', views.index, name='index'),
    #
    url(r'^str_input/$', views.str_input, name='str_input'),
    #
    url(r'^load_file/$', views.load_file, name='load_file'),
    #Page with result search
    url(r'^search_result$', views.search_result, name='search_result'),
    #About page
    url(r'^about$', views.about, name='about'),

]
