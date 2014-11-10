from django.contrib import admin
from fablocks import models


class RelationInline(admin.StackedInline):
    extra = 1
    fk_name = 'child'
    model = models.Relation


class BlockAdmin(admin.ModelAdmin):
    inlines = [RelationInline]


admin.site.register(models.Block, BlockAdmin)
admin.site.register(models.Image)
