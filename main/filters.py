import django_filters

from main.models import LapTime, Car


class LapTimeFilter(django_filters.FilterSet):
    car = django_filters.ModelChoiceFilter(queryset=Car.objects.all())

    class Meta:
        model = LapTime
        fields = ['car']