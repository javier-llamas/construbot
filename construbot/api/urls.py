from django.urls import re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from . import views

app_name = 'construbot.api'

urlpatterns = [
    re_path('customer/list/', views.CustomerList.as_view(), name='customerlist'),
    re_path(r'^api-token-auth/', TokenObtainPairView.as_view()),
    re_path(r'^api-token-refresh/', TokenRefreshView.as_view()),
    re_path(r'^api-token-verify/', TokenVerifyView.as_view()),
    re_path(r'^users/unique/$', views.email_uniqueness, name='get_user'
    ),
    re_path(r'^create/$', views.create_customer_user_and_company, name='creation'
    ),
    re_path(r'^change-usr-pwd/$', views.change_user_password, name='change_pwd'
    ),
    re_path(r'^migraciones/Cliente/$', views.DataMigration.cliente_migration, name='migracion_de_clientes'
    ),
    re_path(r'^migraciones/Sitio/$', views.DataMigration.sitio_migration, name='migracion_de_sitios'
    ),
    re_path(r'^migraciones/Destinatario/$', views.DataMigration.destinatario_migration, name='migracion_de_sitios'
    ),
    re_path(r'^migraciones/Contrato/$', views.DataMigration.contrato_concept_and_estimate_migration, name='migracion_de_contratos'
    ),
]
