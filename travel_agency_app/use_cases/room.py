from datetime import datetime
from travel_agency_app.domain.room import (
    AddRoomDomain,
    UpdateRoomDomain,
    DeleteRoomDomain
)
from travel_agency_app.models.hotel import Hotel
from travel_agency_app.models.room import Room
from travel_agency_app.responses import ApiResponse
import pytz

class AddRoomUseCase:
    def execute(self, domain: AddRoomDomain):
        try:
            check_hotel = list(Hotel.objects.filter(hotel_name=domain.hotel_name).values('id'))
            if check_hotel == []:
                error_message = {
                    "error_message": f"The {domain.hotel_name} hotel is already registered"}
                return ApiResponse.failure(error_message)
            check_room = Room.objects.filter(
                hotel_name=check_hotel[0].get("id"), room_location=domain.room_location)
            if list(check_room) != []:
                error_message = {
                    "error_message": f"The {domain.room_location} room is already registered at {domain.hotel_name} hotel"}
                return ApiResponse.failure(error_message)
            domain.create_date = datetime.now(
                tz=pytz.timezone('America/Bogota')).strftime("%m/%d/%Y, %H:%M:%S")
            hotel_name = domain.hotel_name
            get_hotel_instance = Hotel.objects.get(hotel_name=hotel_name)
            domain.hotel_name = get_hotel_instance
            domain.booking = False
            room_store = Room(**domain.__dict__)
            room_store.save()
            message = {
                "message": f"The {domain.room_location} room has been added at {hotel_name} hotel"}
            return ApiResponse.sucess(message=message)
        except Exception as exc:
            error_message = {
                "error_message": exc.args}
            return ApiResponse.failure(error_message)

class UpdateRoomUseCase:
    def execute(self, domain: UpdateRoomDomain):
        try:
            check_hotel = list(Hotel.objects.filter(hotel_name=domain.hotel_name))
            if check_hotel == []:
                error_message = {
                    "error_message": f"The {domain.hotel_name} hotel is not registered"}
                return ApiResponse.failure(error_message)
            get_hotel_id = Hotel.objects.get(hotel_name=domain.hotel_name).pk
            check_room = Room.objects.filter(
                hotel_name=get_hotel_id, room_location=domain.room_location)
            if list(check_room) == []:
                error_message = {
                    "error_message": f"The {domain.room_location} room is not registered at {domain.hotel_name} hotel"}
                return ApiResponse.failure(error_message)
            get_room = Room.objects.get(
                room_location=domain.room_location, hotel_name=get_hotel_id)
            if domain.field == "amount":
                get_room.amount = domain.value
            elif domain.field == "tax":
                get_room.tax = domain.value
            elif domain.field == "room_type":
                get_room.room_type = domain.value
            elif domain.field == "room_location":
                get_room.room_location = domain.value
            elif domain.field == "enable":
                get_room.enable = domain.value
            elif domain.field == "booking":
                print('hellooooooooooooooooooo')
                print(domain.value)
                get_room.booking = domain.value
            else:
                error_message = {
                    "error_message": f"The {domain.field} field to update does not exist"}
                return ApiResponse.failure(error_message)
            get_room.save()
            message = {
                "message": f"The {domain.field} field has been update by {domain.value}"}
            return ApiResponse.sucess(message=message)
        except Exception as exc:
            error_message = {
                "error_message": exc.args}
            return ApiResponse.failure(error_message)

class DeleteRoomUseCase:
    def execute(self, domain: DeleteRoomDomain):
        try:
            check_hotel = list(Hotel.objects.filter(hotel_name=domain.hotel_name))
            if check_hotel == []:
                error_message = {
                    "error_message": f"The {domain.hotel_name} hotel is not registered"}
                return ApiResponse.failure(error_message)
            get_hotel_id = Hotel.objects.get(hotel_name=domain.hotel_name).pk
            check_room = Room.objects.filter(
                hotel_name=get_hotel_id, room_location=domain.room_location)
            if list(check_room) == []:
                error_message = {
                    "error_message": f"The {domain.room_location} room is not registered at {domain.hotel_name} hotel"}
                return ApiResponse.failure(error_message)
            Room.objects.get(
                hotel_name=get_hotel_id, room_location=domain.room_location).delete()
            message = {
                "message": f"The {domain.room_location} room has been deleted at {domain.hotel_name} hotel"}
            return ApiResponse.sucess(message=message)
        except Exception as exc:
            error_message = {
                "error_message": exc.args}
            return ApiResponse.failure(error_message)
