from django.db import models

from django.conf import settings


def laptime_formatted(duration):
    divide = 10**3
    fstr = '{:03d}'
    if settings.PRECISION == 'hundredths':
        divide *= 1000//100
        fstr = '{:02d}'
    elif settings.PRECISION == 'tenths':
        divide *= 1000//10
        fstr = '{:01d}'

    seconds = duration.seconds + (duration.days * 24 * 60 * 60)
    min_sec = '{}:{:02d}'.format(*divmod(seconds, 60))
    fraction = fstr.format(duration.microseconds // divide)
    return ".".join((min_sec, fraction))


class Driver(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Track(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Car(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class LapTime(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    best = models.DurationField()
    notes = models.CharField(max_length=500, null=True, blank=True)
    media = models.URLField(max_length=500, null=True, blank=True)

    class Meta:
        unique_together = ('driver', 'track', 'car')

    def formatted_time(self):
        return laptime_formatted(self.best)

    def __str__(self):
        return '{}, {}: {} by {}'.format(self.track, self.car, self.formatted_time(), self.driver)
