from rest_framework.serializers import ModelSerializer

from documents.models import Catalog, CatalogVersion


class CatalogVersionSerializer(ModelSerializer):
    class Meta:
        model = CatalogVersion
        fields = ('version', 'startDate')


class CatalogsSerializer(ModelSerializer):
    catalog_version_set = CatalogVersionSerializer(many=True, read_only=True)

    class Meta:
        model = Catalog
        fields = ('id', 'code', 'name', 'catalog_version_set')
