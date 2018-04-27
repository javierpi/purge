# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from models import ToPurge, PurgeProyect


class ToPurge_Admin(admin.ModelAdmin):
    model = ToPurge
    list_display = ('proyect', 'url', 'created_at')
    list_filter = ('proyect',)


class PurgeProyect_Admin(admin.ModelAdmin):
    model = PurgeProyect
    list_display = ('referer', 'server', 'protocolo', 'delta_time', 'urlcount')
    list_filter = ('referer',)


admin.site.register(ToPurge, ToPurge_Admin)
admin.site.register(PurgeProyect, PurgeProyect_Admin)
