import datetime

from django import forms
from django.contrib import admin

from main.models import Driver, Track, LapTime, laptime_formatted


class LapTimeField(forms.DurationField):
    def prepare_value(self, value):
        if isinstance(value, datetime.timedelta):
            return laptime_formatted(value)
        return value


class CustomDriverChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class CustomTrackChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class LapTimeAdminForm(forms.ModelForm):
    best = LapTimeField()
    driver = CustomDriverChoiceField(queryset=Driver.objects.all())
    track = CustomTrackChoiceField(queryset=Track.objects.all())

    class Meta:
        model = LapTime
        fields = ('best', 'driver', 'track')


class LapTimeListAdminForm(forms.ModelForm):
    best = LapTimeField()

    class Meta:
        model = LapTime
        fields = ('best', )


class DriverAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name',)


class TrackAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name',)


class LapTimeAdmin(admin.ModelAdmin):
    fields = ('best', 'driver', 'track')
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


admin.site.register(Driver, DriverAdmin)
admin.site.register(Track, TrackAdmin)
admin.site.register(LapTime, LapTimeAdmin)
