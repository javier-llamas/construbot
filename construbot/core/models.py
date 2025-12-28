# from django.contrib.gis.db import models
# from django.urls import reverse


# class Estado(models.Model):
#     nombre = models.CharField(max_length=45, unique=True)

#     def __str__(self):
#         return self.nombre


# class Municipio(models.Model):
#     clave = models.CharField(max_length=5, unique=True)
#     nombre = models.CharField(max_length=90, unique=True)
#     estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
#     geo = models.MultiPolygonField(geography=True)

#     def __str__(self):
#         return self.nombre


# class Empresa(models.Model):
#     nombre = models.CharField(max_length=250, blank=True, null=True)
#     logo = models.ImageField(upload_to='logos', blank=True, null=True)
#     verified = models.BooleanField(default=False)
#     rfc = models.CharField(max_length=20, blank=True, null=True)
#     sector = models.ManyToManyField('core.Sector', through='core.SectorEmpresa')

#     class Meta:
#         verbose_name = 'Empresa'
#         verbose_name_plural = 'Empresas'

#     def __str__(self):
#         return self.marca  # pragma: no cover
    

# class CentroTrabajo(models.Model):
#     name = models.CharField(max_length=80)
#     empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
#     position = models.PointField(srid=4326, null=True, blank=True)
#     direccion = models.CharField(max_length=120, null=True, blank=True)
#     municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, null=True, blank=True)

#     def get_absolute_url(self):
#         return reverse('proyectos:sitio_detail', kwargs={'pk': self.id})

#     def get_contratos_ordenados(self):
#         return self.contrato_set.all().order_by('-fecha')

#     def __str__(self):
#         return self.sitio_name

#     class Meta:
#         verbose_name = "Sitio"
#         verbose_name_plural = "Sitios"


# class Sector(models.Model):
#     nombre = models.CharField(max_length=45, unique=True)

#     def __str__(self):
#         return self.nombre


# class SectorEmpresaRquisicion(models.Model):
#     sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
#     empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
#     requisicion = models.ForeignKey('core.Requisicion', on_delete=models.CASCADE)

#     def __str__(self):
#         return self.sector.nombre + " - " + self.empresa.nombre + " - " + self.requisicion.titulo[:20]

# class Requisicion(models.Model):
#     no_partida = models.IntegerField()
#     fecha = models.DateTimeField()
#     titulo = models.CharField(max_length=80)
#     credito_comercial_dias = models.IntegerField()
#     financiamiento_dias = models.IntegerField()
#     sector_tags = models.ManyToManyField(Sector, through='core.SectorEmpresaRquisicion')
