
from django.conf.urls import url, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^$', views.add_order),
    url(r'^transactions/$', views.transactions),
    url(r'^add/$', views.add_order),
    url(r'^transaction/$', views.transaction),
    url(r'^saldo/$', views.saldo),
    url(r'^login/$', auth_views.login, {'template_name': 'LagerApp/login.html'}),
    url(r'^logout/$', auth_views.logout, {'template_name': 'LagerApp/logout.html'}),
    url(r'^', include('django.contrib.auth.urls'))
]