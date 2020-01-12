import datetime

from django import forms
from django.contrib import admin

from main.models import Driver, Track, LapTime, laptime_formatted, Car


class LapTimeField(forms.DurationField):
    def prepare_value(self, value):
        if isinstance(value, datetime.timedelta):
            return laptime_formatted(value)
        return value


class LapTimeAdminForm(forms.ModelForm):
    best = LapTimeField()

    class Meta:
        model = LapTime
        fields = ('best', )


class LapTimeListAdminForm(forms.ModelForm):
    best = LapTimeField()

    class Meta:
        model = LapTime
        fields = ('best', )


class CarAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name',)


class DriverAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name',)


class TrackAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name',)


class LapTimeAdmin(admin.ModelAdmin):
    fields = ('best', 'driver', 'car', 'track', 'media', 'notes')
    list_display = ('best', 'friendly')
    list_editable = ('best', )
    list_display_links = ('friendly', )
    list_filter = ('track__name', )
    ordering = ('best', )

    def get_changelist_form(self, request, **kwargs):
        kwargs.setdefault('form', LapTimeListAdminForm)
        return super().get_changelist_form(request, **kwargs)

    def friendly(self, obj):
        return str(obj)
    friendly.short_description = 'Details'

    form = LapTimeAdminForm


admin.site.register(Car, CarAdmin)
admin.site.register(Driver, DriverAdmin)
admin.site.register(Track, TrackAdmin)
admin.site.register(LapTime, LapTimeAdmin)
