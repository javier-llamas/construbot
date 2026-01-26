from django.urls import re_path

from . import views


urlpatterns = [
    re_path(r'^signup/$', views._SignupView.as_view(), name='account_signup'),
    re_path(r'^login/$', views._LoginView.as_view(), name='account_login'),
    re_path(r'^logout/$', views._LogoutView.as_view(), name='account_logout'),

    re_path(r'^password/change/(?:(?P<username>[\w.@+-]+)/)?$', views._PasswordChangeView.as_view(),
        name='account_change_password'),
    re_path(r'^password/set/$', views._PasswordSetView.as_view(), name='account_set_password'),

    re_path(r'^inactive/$', views._AccountInactiveView.as_view(), name='account_inactive'),

    # E-mail
    re_path(r'^email/$', views._EmailView.as_view(), name='account_email'),
    re_path(r'^confirm-email/$', views._EmailVerificationSentView.as_view(),
        name='account_email_verification_sent'),
    re_path(r'^confirm-email/(?P<key>[-:\w]+)/$', views._ConfirmEmailView.as_view(),
        name='account_confirm_email'),

    # password reset
    re_path(r'^password/reset/$', views._PasswordResetView.as_view(),
        name='account_reset_password'),
    re_path(r'^password/reset/done/$', views._PasswordResetDoneView.as_view(),
        name='account_reset_password_done'),
    re_path(r'^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$',
        views._PasswordResetFromKeyView.as_view(),
        name='account_reset_password_from_key'),
    re_path(r'^password/reset/key/done/$', views._PasswordResetFromKeyDoneView.as_view(),
        name='account_reset_password_from_key_done'),
]
