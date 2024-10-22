from django.contrib.auth.models import User
from django.db import models

class CountryWeather(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    country_name = models.CharField(max_length=100)
    temperature = models.FloatField()
    humidity = models.FloatField()
    wind_speed = models.FloatField(null=True)
    pressure = models.FloatField(null=True)
    visibility = models.FloatField(null=True)
    date = models.CharField(max_length=100, null=True)
    time = models.CharField(max_length=100, null=True)
    temp_min = models.FloatField(null=True)
    temp_max = models.FloatField(null=True)
    feels_like = models.FloatField(null=True)
    dew_point = models.FloatField(null=True)
    weather_condition = models.CharField(max_length=100, null=True)
                  

    def __str__(self):
        return self.country_name
