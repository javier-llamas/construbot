from allauth.account.forms import LoginForm, PasswordField
from django import forms
from django.utils.translation import pgettext, gettext, gettext_lazy as _


class AccLoginForm(LoginForm):
    password = PasswordField(label=_("Contraseña"))
    remember = forms.BooleanField(label=_("Recuérdame"), required=False)
