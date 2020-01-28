import os
from collections import defaultdict

from django.db.models import Min
from django.http import Http404
from django.shortcuts import render

from main.filters import LapTimeFilter
from main.models import Track, LapTime, SanctionedCar


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
        sanctioned_cars = SanctionedCar.objects.filter(track=track_id).order_by('car__name')

        laptimes = LapTime.objects.filter(
            track=track_id,
            car__sanctionedcar__in=sanctioned_cars).order_by('car', 'best')
        filtered_by_car = LapTimeFilter(request.GET, queryset=laptimes)

        car_order = [id for id, _ in filtered_by_car.qs.order_by('best').values_list('car__id').annotate(best=Min('best'))]

        by_car = defaultdict(list)
        for laptime in filtered_by_car.qs:
            by_car[laptime.car.id].append(laptime)

        final_order = []
        for car_id in car_order:
            final_order.extend(by_car[car_id])

        return render(request, 'track_records.html',
                      context={'laptimes': final_order,
                               'track': Track.objects.get(pk=track_id),
                               'sanctioned_cars': [x.car for x in sanctioned_cars]
                               })
    except Track.DoesNotExist:
        raise Http404
