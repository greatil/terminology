from django.db import models


class Catalog(models.Model):
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=300)
    description = models.TextField(blank=True)


class CatalogVersion(models.Model):
    catalogID = models.ForeignKey(Catalog, on_delete=models.CASCADE)
    version = models.CharField(max_length=50)
    startDate = models.DateField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['catalogID', 'version'], name='unique_catalogID_version'),
            models.UniqueConstraint(fields=['catalogID', 'startDate'], name='unique_catalogID_startDate'),
        ]


class CatalogElement(models.Model):
    catalogVersionID = models.ForeignKey(CatalogVersion, on_delete=models.CASCADE)
    elementCode = models.CharField(max_length=100)
    elementValue = models.CharField(max_length=300)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['catalogVersionID', 'elementCode'],
                                    name='unique_catalogVersionID_elementCode'),
        ]
