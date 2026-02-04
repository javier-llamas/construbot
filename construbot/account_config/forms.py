from django import forms
from django.utils.translation import gettext_lazy as _

from allauth.account.forms import LoginForm, PasswordField


class AccLoginForm(LoginForm):
    password = PasswordField(label=_("Contraseña"))
    remember = forms.BooleanField(label=_("Recuérdame"), required=False)
