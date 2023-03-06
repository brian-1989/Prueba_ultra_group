from rest_framework import serializers

class AddRoomSerializer(serializers.Serializer):
    hotel_name = serializers.CharField(allow_blank=False, required=True, max_length=100)
    amount = serializers.IntegerField(required=True)
    tax = serializers.IntegerField(required=True)
    room_type = serializers.CharField(allow_blank=False, required=True, max_length=100)
    room_location = serializers.CharField(allow_blank=False, required=True, max_length=2)

class UpdateRoomSerializar(serializers.Serializer):
    hotel_name = serializers.CharField(allow_blank=False, required=True, max_length=100)
    field = serializers.CharField(allow_blank=False, required=True, max_length=100)
    value = serializers.CharField(allow_blank=True, required=False, max_length=100)
    room_location = serializers.CharField(allow_blank=False, required=True, max_length=2)

class DeleteRoomSerializer(serializers.Serializer):
    hotel_name = serializers.CharField(allow_blank=False, required=True, max_length=100)
    room_location = serializers.CharField(allow_blank=False, required=True, max_length=2)
