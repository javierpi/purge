from __future__ import absolute_import
import requests
from celery import shared_task
from purge.models import ToPurge, PurgeProyect
from django.conf import settings

# app = Celery('tasks', broker='amqp://guest@localhost//')


@shared_task
def add():
    return 1


@shared_task
def purge_():
    if settings.TASK_PURGE:
        projects = PurgeProyect.objects.all()
        for project in projects:
            servers = project.server
            protocolo = project.protocolo
            purge_method = project.purge_method
            delta_time = project.delta_time
            exclude_url = str(project.exclude_url).split(' ')

            try:
               clean_url(project, servers, protocolo, purge_method, delta_time, exclude_url)
                
            except Exception as e:
                print e
                print('error')
                # task_annotate('purge: Error conecting to ' + referer, 'ERROR', PurgeProyect, project.id)
            # clean_url.apply_async((project, server, protocolo, purge_method, delta_time, generate_new_cache, exclude_url), queue='purge')


def clean_url(project, servers, protocolo, purge_method, delta_time, exclude_url):

    # created_time = timezone.now() - timezone.timedelta(minutes=delta_time)
    purges_clean = ToPurge.objects.\
        filter(proyect=project).\
        filter(next_ask__gt=0)

    # Deleting cache
    for purge in purges_clean:
        aservers = str(servers).split(' ')
        for server in aservers:
            url = protocolo + server + str(purge) + purge_method
            print('Purging..', str(server), url)
            requests.get(url)
        
        purge.total_purged = int(purge.total_purged) + 1
        purge.save()

    # recalc
    purges_recalc = ToPurge.objects.filter(proyect=project)
    for recalc in purges_recalc:
        recalc.next_ask = int(recalc.future_ask)
        recalc.future_ask = 0
        recalc.save()

    print('Fin del purge para el server:', servers)
