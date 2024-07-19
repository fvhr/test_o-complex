from django.db import models


class City(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    request_count = models.PositiveIntegerField(
        default=0,
    )  # Поле для подсчета запросов

    def __str__(self):
        return self.name
