from django.db import models

class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    create_date = models.CharField(max_length=20)
    begin_date  = models.CharField(max_length=20)
    end_date  = models.CharField(max_length=20)
    hotel_name = models.CharField(max_length=20)
    room_location = models.CharField(max_length=15)
    emergency_contact_name  = models.CharField(max_length=20)
    emergency_contact_cellpohne_number  = models.CharField(max_length=20)

class Passenger(models.Model):
    id = models.AutoField(primary_key=True)
    name =  models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    genre = models.CharField(max_length=20)
    document_type = models.CharField(max_length=20)
    document_number = models.IntegerField()
    email = models.CharField(max_length=50)
    cellphone_number = models.IntegerField()
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
