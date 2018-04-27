# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# from django.shortcuts import render
from .models import ToPurge, PurgeProyect
from .tasks import add
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.views.generic.detail import DetailView


def add_url(request, *args):
    saved_args = str(request).split(' ')
    referer = get_client_ip(request)
    try:
        proyect = PurgeProyect.objects.get(referer=referer)
        cuenta = 0
        excludes = str(proyect.exclude_url).split(' ')

        for k in saved_args:
            cuenta = cuenta + 1
            if cuenta == 3:
                k = k.replace("'", "")
                # Elimina todos los /purge
                k = k.replace("/purge", "")
                k = k.replace("/PURGE", "")
                url = k.split('>')
                for t in url:
                    urltoadd = t.strip()
                    agrega = True
                    for exclude in excludes:
                        if exclude in urltoadd:
                            # print("Saltar ", urltoadd, " dado que existe ", exclude)
                            agrega = False
                    if len(urltoadd) > 0 and agrega:
                        # print urltoadd
                        try:
                            obj = ToPurge.objects.get(proyect=proyect, url=urltoadd)
                            obj.total_asked = obj.total_asked + 1
                            obj.future_ask = obj.future_ask + 1
                            obj.save()
                        except ToPurge.DoesNotExist:
                            obj = ToPurge(
                                proyect=proyect,
                                url=urltoadd,
                                total_asked=1,
                                total_purged=0,
                                next_ask=0,
                                future_ask=1)
                            obj.save()
                        return HttpResponse('Si addurl 2')
                    else:
                        return HttpResponse('NO por url no permitida')
        return HttpResponse('Si addurl 2')
    except PurgeProyect.DoesNotExist:
        return HttpResponseNotFound('<h1>Proyect referer dont exists</h1>' + referer)


def get_referer(clientip):
    entry = PurgeProyect.objects.get(referer=clientip)
    if entry.exists():
        return entry
    else:
        return False


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class show_purge_uniqueview(DetailView):
    model = PurgeProyect
    template_name = 'purge/topurge_detail.html'

    def get_context_data(self, **kwargs):
        context = super(show_purge_uniqueview, self).get_context_data(**kwargs)
        context['unique'] = ToPurge.objects.filter(proyect=self.get_object()).order_by('-total_asked')
        context['unique3'] = ToPurge.objects.filter(next_ask__gt=0).filter(proyect=self.get_object())

        return context
