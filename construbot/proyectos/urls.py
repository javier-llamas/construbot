from django.urls import re_path

from . import views

app_name = 'construbot.proyectos'

urlpatterns = [
    re_path(r'^$', views.ProyectDashboardView.as_view(),
        name='proyect_dashboard'
    ),
    re_path(r'^listado/contratos/$', views.ContratoListView.as_view(),
        name='listado_de_contratos'
    ),
    re_path(r'^listado/clientes/$', views.ClienteListView.as_view(),
        name='listado_de_clientes'
    ),
    re_path(r'^listado/sitios/$', views.SitioListView.as_view(),
        name='listado_de_sitios'
    ),
    re_path(r'^listado/destinatarios/$', views.DestinatarioListView.as_view(),
        name='listado_de_destinatarios'
    ),
    re_path(r'^contrato/catalogo-edit/(?P<pk>\d+)/$', views.CatalogoConceptosInlineFormView.as_view(),
        name='catalogo_conceptos'
    ),
    re_path(r'^contrato/retenciones-edit/(?P<pk>\d+)/$', views.CatalogoRetencionesInlineFormView.as_view(),
        name='catalogo_retenciones'
    ),
    re_path(r'^contrato/catalogo-unidades/$', views.CatalogoUnitsInlineFormView.as_view(),
        name='catalogo_de_unidades'
    ),
    re_path(r'^contrato/catalogo-conceptos/(?P<pk>\d+)/$', views.CatalogoConceptos.as_view(),
        name='catalogo_conceptos_listado'
    ),
    re_path(r'^contrato/detalle/(?P<pk>\d+)/$', views.ContratoDetailView.as_view(),
        name='contrato_detail'
    ),
    re_path(r'^cliente/detalle/(?P<pk>\d+)/$', views.ClienteDetailView.as_view(),
        name='cliente_detail'
    ),
    re_path(r'^sitio/detalle/(?P<pk>\d+)/$', views.SitioDetailView.as_view(),
        name='sitio_detail'
    ),
    re_path(r'^destinatario/detalle/(?P<pk>\d+)/$', views.DestinatarioDetailView.as_view(),
        name='destinatario_detail'
    ),
    re_path(r'^estimacion/detalle/(?P<pk>\d+)/$', views.EstimateDetailView.as_view(),
        name='estimate_detail'
    ),
    re_path(r'^estimacion/(?P<pk>\d+)/reporte-subcontratistas/$', views.SubcontratosReport.as_view(),
        name='reporte-subcontratistas'
    ),
    re_path(r'^estimacion/pdf/(?P<pk>\d+)/$', views.EstimatePdfPrint.as_view(),
        name='estimate_detailpdf'
    ),
    re_path(r'^generador/pdf/(?P<pk>\d+)/$', views.GeneratorPdfPrint.as_view(),
        name='generator_detailpdf'
    ),
    re_path(r'^contrato/nuevo/$', views.ContratoCreationView.as_view(),
        name='nuevo_contrato'
    ),
    re_path(r'^subcontrato/nuevo/(?P<pk>\d+)/$', views.SubcontratoCreationView.as_view(),
        name='nuevo_subcontrato'
    ),
    re_path(r'^cliente/nuevo/$', views.ClienteCreationView.as_view(),
        name='nuevo_cliente'
    ),
    re_path(r'^sitio/nuevo/$', views.SitioCreationView.as_view(),
        name='nuevo_sitio'
    ),
    re_path(r'^destinatario/nuevo/$', views.DestinatarioCreationView.as_view(),
        name='nuevo_destinatario'
    ),
    re_path(r'^estimacion/nuevo/(?P<pk>\d+)/$', views.EstimateCreationView.as_view(),
        name='nueva_estimacion'
    ),
    re_path(r'^editar/contrato/(?P<pk>\d+)/$', views.ContratoEditView.as_view(),
        name='editar_contrato'
    ),
    re_path(r'^editar/cliente/(?P<pk>\d+)/$', views.ClienteEditView.as_view(),
        name='editar_cliente'
    ),
    re_path(r'^editar/sitio/(?P<pk>\d+)/$', views.SitioEditView.as_view(),
        name='editar_sitio'
    ),
    re_path(r'^editar/destinatario/(?P<pk>\d+)/$', views.DestinatarioEditView.as_view(),
        name='editar_destinatario'
    ),
    re_path(r'^editar/estimacion/(?P<pk>\d+)/$', views.EstimateEditView.as_view(),
        name='editar_estimacion'
    ),
    re_path(r'^eliminar/(?P<model>\w+)/(?P<pk>\d+)/$', views.DynamicDelete.as_view(),
        name='eliminar'
    ),
    re_path(r'cliente-autocomplete/$', views.ClienteAutocomplete.as_view(create_field='cliente_name'),
        name='cliente-autocomplete'
    ),
    re_path(r'subcontratista-autocomplete/$', views.SubcontratistaAutocomplete.as_view(create_field='cliente_name'),
        name='subcontratista-autocomplete'
    ),
    re_path(r'sitio-autocomplete/$', views.SitioAutocomplete.as_view(create_field='sitio_name'),
        name='sitio-autocomplete'
    ),
    re_path(r'destinatario-autocomplete/$', views.DestinatarioAutocomplete.as_view(create_field='destinatario_text'),
        name='destinatario-autocomplete'
    ),
    re_path(r'^unit-autocomplete/$', views.UnitAutocomplete.as_view(create_field='unit'),
        name='unit-autocomplete'
    ),
    re_path(r'^user-autocomplete/$', views.UserAutocomplete.as_view(),
        name='user-autocomplete'
    ),
    re_path(r'^company-autocomplete/$', views.CompanyAutocomplete.as_view(),
        name='company-autocomplete'
    ),
    re_path(r'^nivelacceso-autocomplete/$', views.NivelAccesoAutocomplete.as_view(),
        name='nivelacceso-autocomplete'
    ),

]
