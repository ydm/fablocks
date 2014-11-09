from django.contrib import admin
from fablocks import models


class RelationInline(admin.StackedInline):
    model = models.Relation
    fk_name = 'child'
    extra = 1


class BlockAdmin(admin.ModelAdmin):
    inlines = [RelationInline]


admin.site.register(models.Block, BlockAdmin)
