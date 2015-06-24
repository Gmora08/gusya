from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.WaitingListRegistration.as_view(), name='waiting_list'),
    url(r'^/(?P<activation_key>\w+)/$', views.RegisterByInvitation.as_view(), name='register_invitation'),
    url(r'^admin/$', views.LoginAdmin.as_view(), name='admin_login'),
    url(r'^admin/mail_sent/$', views.GetSentEmailUser.as_view(), name='mail_sent'),
    url(r'^admin/logout/$', views.logout_admin, name='admin_logout'),
    url(r'^admin/activate_user/$', views.SendEmailActivation.as_view(), name='active_user'),
    url(r'^admin/outstanding/(?P<id_user>\d{1,})/$', views.customer_to_outstanding, name='outstanding'),
    url(r'^admin/charge/$', views.Payment.as_view(), name='make_charge'),
    url(r'^admin/users/active$', views.show_active_users, name='active'),
    url(r'^admin/users/pending$', views.show_pending_users, name='wait'),
    url(r'^invitation/$', views.RegisterUserByInvitation.as_view(), name='register_invitate_user'),
    url(r'^confirm/$', views.register_card.as_view(), name='activate'),
    url(r'^faq/$', views.faq, name='faq'),
]
