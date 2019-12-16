import os

from django.http import Http404
from django.shortcuts import render

from main.models import Track, LapTime


def debug(request):
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        result = "<br>".join([r[0] for r in cursor.fetchall()])

        return render(request, 'debug.html', context={'debug_string': result,
                                                      'pwd': os.getcwd(),
                                                      'db_inf': str(os.stat("/tmp/db.sqlite3"))})


def track_index(request):
    return render(request, 'track_index.html', context={'tracks': Track.objects.order_by('name')})


def track_records(request, track_id):
    try:
        return render(request, 'track_records.html',
                      context={'laptimes': LapTime.objects.filter(track_id=track_id).order_by('best'),
                               'track': Track.objects.get(pk=track_id)})
    except Track.DoesNotExist:
        raise Http404
