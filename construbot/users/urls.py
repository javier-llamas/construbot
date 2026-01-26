from django.urls import re_path

from . import views

app_name = 'construbot.users'

urlpatterns = [
    re_path(r'^$', views.UserListView.as_view(),
        name='list'
    ),
    re_path(r'^remove-is-new/(?P<pk>\d+)/$', views.RemoveIsNewUserStatus.as_view(),
        name='remove_is_new'
    ),
    re_path(r'^eliminar/(?P<model>\w+)/(?P<pk>\d+)/$', views.UserDeleteView.as_view(),
        name='delete_user'
    ),
    re_path(r'^password/$', views.PasswordRedirectView.as_view(),
        name='password_change_redirect'
    ),
    re_path(r'^~redirect/$', views.UserRedirectView.as_view(),
        name='redirect'
    ),
    re_path(r'^new/$', views.UserCreateView.as_view(),
        name='new'
    ),
    re_path(r'^nuevo/company/$', views.CompanyCreateView.as_view(),
        name='new_company'
    ),
    re_path(r'^company-update/(?P<pk>\d+)/$', views.CompanyEditView.as_view(),
        name='company_edit'
    ),
    re_path(r'^listado/company/$', views.CompanyListView.as_view(),
        name='company_list'
    ),
    # De momento se desactiva la vista.
    # re_path(
    #     regex=r'^detalle/company/(?P<pk>\d+)/$',
    #     view=views.CompanyDetailView.as_view(),
    #     name='company_detail'
    # ),
    re_path(r'^detalle/company/(?P<pk>\d+)/$', views.CompanyChangeViewFromList.as_view(),
        name='company_detail'
    ),
    re_path(r'^detalle/(?:(?P<username>[\w.@+-]+)/)?$', views.UserDetailView.as_view(),
        name='detail'
    ),
    re_path(r'^update/(?:(?P<username>[\w.@+-]+)/)?$', views.UserUpdateView.as_view(),
        name='update'
    ),
    re_path(r'^company-change/(?P<company>[\w ]+)/$', views.CompanyChangeView.as_view(),
        name='company-change'
    ),
]
