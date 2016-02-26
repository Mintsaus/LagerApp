
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.startpage),
    url(r'^products$', views.products),
    url(r'^add', views.add_order),
    url(r'^transaction', views.transaction),

]