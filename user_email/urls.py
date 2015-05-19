from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.WaitingListRegistration.as_view(), name='waiting_list'),
]
