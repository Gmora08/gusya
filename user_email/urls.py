from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.WaitingListRegistration.as_view(), name='waiting_list'),
    url(r'^activate_user/$', views.SendEmailActivation.as_view(), name='active_user'),
    url(r'^confirm/(?P<activation_key>\w+)/', views.register_confirm, name='activate'),
]
