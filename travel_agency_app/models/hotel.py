from django.db import models
from travel_agency_app.models.city import City

class Hotel(models.Model):
    id = models.AutoField(primary_key=True)
    create_date = models.CharField(max_length=20)
    hotel_name = models.CharField(max_length=20, unique=True)
    enable = models.BooleanField()
    city_name = models.ForeignKey(City, on_delete=models.CASCADE, default="")
