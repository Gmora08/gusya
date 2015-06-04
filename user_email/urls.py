from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.WaitingListRegistration.as_view(), name='waiting_list'),
    url(r'^admin/$', views.LoginAdmin.as_view(), name='admin_login'),
    url(r'^admin/logout/$', views.logout_admin, name='admin_logout'),
    url(r'^admin/activate_user/$', views.SendEmailActivation.as_view(), name='active_user'),
    url(r'^admin/charge/$', views.Payment.as_view(), name='make_charge'),
    url(r'^confirm/(?P<activation_key>\w+)/$', views.register_card.as_view(), name='activate'),
    url(r'^admin/users/$', views.PhoneUsers, name='phone'),
]
