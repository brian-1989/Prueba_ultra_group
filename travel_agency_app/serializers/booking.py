from rest_framework import serializers

class PassengerSerializer(serializers.Serializer):
    name = serializers.CharField(allow_blank=False, required=True, max_length=100)
    last_name = serializers.CharField(allow_blank=False, required=True, max_length=100)
    genre = serializers.CharField(allow_blank=False, required=True, max_length=100)
    document_type = serializers.CharField(allow_blank=False, required=True, max_length=100)
    document_number = serializers.CharField(allow_blank=False, required=True, max_length=100)
    email = serializers.CharField(allow_blank=False, required=True, max_length=100)
    cellphone_number = serializers.IntegerField(required=True)

class AddBookingSerializer(serializers.Serializer):
    passenger = serializers.ListField(child=PassengerSerializer())
    begin_date = serializers.CharField(allow_blank=False, required=True, max_length=100)
    end_date = serializers.CharField(allow_blank=False, required=True, max_length=100)
    hotel_name = serializers.CharField(allow_blank=False, required=True, max_length=100)
    room_location = serializers.CharField(allow_blank=False, required=True, max_length=100)
    emergency_contact_name = serializers.CharField(
        allow_blank=False, required=True, max_length=100)
    emergency_contact_cellpohne_number = serializers.IntegerField(required=True)

class UpdateBookingSerializer(serializers.Serializer):
    hotel_name = serializers.CharField(allow_blank=False, required=True, max_length=100)
    field = serializers.CharField(allow_blank=False, required=True, max_length=100)
    value = serializers.CharField(allow_blank=True, required=False, max_length=100)
    room_location = serializers.CharField(allow_blank=False, required=True, max_length=2)

class DeleteBookingSerializer(serializers.Serializer):
    hotel_name = serializers.CharField(allow_blank=False, required=True, max_length=100)
    room_location = serializers.CharField(allow_blank=False, required=True, max_length=2)