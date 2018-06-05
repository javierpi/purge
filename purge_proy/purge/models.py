# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models import Sum


class PurgeProyect(models.Model):
    referer = models.CharField(max_length=30, unique=True)
    server = models.CharField(max_length=50, unique=False, help_text="Send purges to servers, separate by space")
    description = models.CharField('Proyect description', max_length=200, default='')
    protocolo = models.CharField(max_length=10, unique=False, default='http://')
    purge_method = models.CharField(max_length=10, unique=False, default='/PURGE')
    delta_time = models.PositiveSmallIntegerField(default=0)
    # generate_new_cache = models.BooleanField()
    exclude_url = models.CharField(max_length=200, unique=False, blank=True, null=True)

    def urlcount(self):
        return ToPurge.objects.filter(proyect=self.id).count()

    def next_ask(self):
        return ToPurge.objects.filter(proyect=self.id).filter(next_ask__gt=0).count()

    def future_ask(self):
        return ToPurge.objects.filter(proyect=self.id).filter(future_ask__gt=0).count()

    def total_asked(self):
        return ToPurge.objects.filter(proyect=self.id).aggregate(total_asked=Sum('total_asked'))

    def total_purged(self):
        return ToPurge.objects.filter(proyect=self.id).aggregate(total_purged=Sum('total_purged'))

    def reduction_percent(self):
        pur = ToPurge.objects.filter(proyect=self.id).aggregate(total_purged=Sum('total_purged'))
        asked = ToPurge.objects.filter(proyect=self.id).aggregate(total_asked=Sum('total_asked'))
        if pur['total_purged'] and asked['total_asked']:
            rat = (1 - (float(float(pur['total_purged']) / float(asked['total_asked'])))) * 100
        else:
            rat = 0.00
        return rat

    class Meta:
        verbose_name_plural = 'Purge Proyects'
        verbose_name = 'Purge Proyect'
        ordering = ["referer"]

    def __str__(self):
        return self.referer


class ToPurge(models.Model):
    proyect = models.ForeignKey(PurgeProyect, on_delete=models.CASCADE, blank=False, null=False)
    url = models.CharField(max_length=200, unique=False)
    created_at = models.DateTimeField(
        'created at',
        help_text="Please use the following format: <em>YYYY-MM-DD</em>.",
        auto_now_add=True
    )
    total_asked = models.IntegerField(default=0)
    total_purged = models.IntegerField(default=0)
    next_ask = models.IntegerField(default=0)
    future_ask = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'URLs to Purge'
        verbose_name = 'URL to Purge'
        ordering = ["proyect", "url"]
        unique_together = ("proyect", "url")

    def __str__(self):
        return self.url
