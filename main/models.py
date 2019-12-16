from django.db import models


def laptime_formatted(duration):
    seconds = duration.seconds + (duration.days * 24 * 60 * 60)
    microseconds = duration.microseconds
    return '{}:{:02d}.{:03d}'.format(seconds // 60, seconds % 60, microseconds // 1000)


class Driver(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Track(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class LapTime(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    best = models.DurationField()

    class Meta:
        unique_together = ('driver', 'track',)

    def formatted_time(self):
        return laptime_formatted(self.best)

    def __str__(self):
        return '{}: {} by {}'.format(self.track, self.formatted_time(), self.driver)
