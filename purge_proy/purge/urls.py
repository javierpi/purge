from django.conf.urls import url
from purge.views import add_url


urlpatterns = [
    #    url(r'^$', views.index, name='index'),
    url(r'^', add_url, name='add_url'),
]
