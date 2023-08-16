from django.contrib import admin
from .models import Catalog, CatalogVersion, CatalogElement


class CatalogElementInline(admin.StackedInline):
    model = CatalogElement


class CatalogVersionInline(admin.StackedInline):
    model = CatalogVersion


class CatalogAdmin(admin.ModelAdmin):
    inlines = [CatalogVersionInline]
    list_display = ('id', 'code', 'name', 'version', 'startDate')

    def version(self, obj):
        try:
            return CatalogVersion.objects.filter(catalogID_id=obj.id).first().version
        except AttributeError:
            return None

    def startDate(self, obj):
        try:
            return CatalogVersion.objects.filter(catalogID_id=obj.id).first().startDate
        except AttributeError:
            return None


class CatalogVersionAdmin(admin.ModelAdmin):
    list_display = ('catalogID', 'version', 'startDate', 'code', 'name')
    inlines = [CatalogElementInline]

    def code(self, obj):
        try:
            return CatalogVersion.objects.filter(catalogID_id=obj.id).first().catalogID.code
        except AttributeError:
            return None

    def name(self, obj):
        try:
            return CatalogVersion.objects.filter(catalogID_id=obj.id).first().catalogID.name
        except AttributeError:
            return None

class CatalogElementAdmin(admin.ModelAdmin):
    list_display = ('catalogVersionID', 'elementCode', 'elementValue')


admin.site.register(Catalog, CatalogAdmin)
admin.site.register(CatalogVersion, CatalogVersionAdmin)
admin.site.register(CatalogElement, CatalogElementAdmin)
