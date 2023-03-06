from django.db import models
from travel_agency_app.models.hotel import Hotel

class Room(models.Model):
    id = models.AutoField(primary_key=True)
    create_date = models.CharField(max_length=20)
    amount = models.IntegerField()
    tax = models.IntegerField()
    room_type = models.CharField(max_length=20)
    room_location = models.CharField(max_length=15)
    enable = models.BooleanField()
    booking = models.BooleanField()
    hotel_name = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="hotel")