from django.conf import settings
from django.urls import include, re_path
from django.conf.urls.static import static
from django.contrib import admin
from django.views import defaults as default_views
from construbot.users.views import UserRedirectView

urlpatterns = [
    re_path(r'^$', UserRedirectView.as_view(), name='home'),
]
if not settings.CONSTRUBOT_AS_LIBRARY:
    urlpatterns += [
        # Standalone allauth configuration
        # User management
        re_path(r'^accounts/', include('construbot.account_config.urls')),
        # Django Admin, use {% url 'admin:index' %}
        re_path(settings.ADMIN_URL, admin.site.urls),
    ]

urlpatterns += [
    # Your stuff: custom urls includes go here
    re_path(r'^proyectos/', include('construbot.proyectos.urls', namespace='proyectos')),
    # In-app user management
    re_path(r'^users/', include('construbot.users.urls', namespace='users')),
    # REST API
    re_path(r'^api/v1/', include('construbot.api.urls', namespace='api')),

    re_path(r'^core/', include('construbot.core.urls', namespace='core')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG and not settings.CONSTRUBOT_AS_LIBRARY:  # pragma: no cover
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        re_path(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        re_path(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        re_path(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        re_path(r'^500/$', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            re_path(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
