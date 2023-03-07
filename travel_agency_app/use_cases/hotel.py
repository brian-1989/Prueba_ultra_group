from datetime import datetime
from travel_agency_app.domain.hotel import (
    CreateNewHotelDomain,
    UpdateHotelDomain,
    DeleteHotelDomain
)
from travel_agency_app.responses import ApiResponse
from travel_agency_app.models.city import City
from travel_agency_app.models.hotel import Hotel
import pytz

class GetAllHotelsUseCase:
    def execute(self):
        try:
            get_all_cities = City.objects.filter(enable=True).values("id", "city_name")
            response = {}
            for city in get_all_cities:
                print(city)
                get_hotels = Hotel.objects.filter(
                    city_name_id=city.get("id"), enable=True).values('hotel_name')
                hotel_list = list(get_hotels)
                if hotel_list != []:
                    response[city.get('city_name')] = [hotel for hotel in hotel_list]
            return ApiResponse.sucess(message=response)
        except Exception as exc:
            error_message = {
                "error_message": exc.args}
            return ApiResponse.failure(error_message=error_message)

class CreateNewHotelUseCase:
    def execute(self, domain: CreateNewHotelDomain):
        try:
            check_city = City.objects.filter(city_name=domain.city_name).values('id')
            if list(check_city) == []:
                error_message = {
                    "error_message": f"The {domain.city_name} city is not registered"}
                return ApiResponse.failure(error_message)
            check_hotel = Hotel.objects.filter(hotel_name=domain.hotel_name).values('id')
            if list(check_hotel) != []:
                error_message = {
                    "error_message": f"The {domain.hotel_name} hotel is already registered"}
                return ApiResponse.failure(error_message)
            get_city_instance = City.objects.get(city_name=domain.city_name)
            domain.city_name = get_city_instance
            domain.create_date = datetime.now(
                tz=pytz.timezone('America/Bogota')).strftime("%m/%d/%Y, %H:%M:%S")
            hotel_store = Hotel(**domain.__dict__)
            hotel_store.save()
            message = {"status": "Done"}
            return ApiResponse.sucess(message=message)
        except Exception as exc:
            error_message = {
                "error_message": exc.args}
            return ApiResponse.failure(error_message=error_message)

class UpdateHotelUseCase:
    def execute(self, domain: UpdateHotelDomain):
        try:
            check_hotel = Hotel.objects.filter(hotel_name=domain.hotel_name)
            if list(check_hotel) == []:
                error_message = {
                    "error_message": f"The {domain.hotel_name} hotel to update does not exist"}
                return ApiResponse.failure(error_message)
            get_hotel = Hotel.objects.get(hotel_name=domain.hotel_name)
            if domain.field == "hotel_name":
                get_hotel.hotel_name = domain.value
            elif domain.field == "enable":
                get_hotel.enable = domain.value
            else:
                error_message = {
                    "error_message": f"The {domain.field} field to update does not exist"}
                return ApiResponse.failure(error_message)
            get_hotel.save()
            message = {
                "message": f"The {domain.field} field has been update by {domain.value}"}
            return ApiResponse.sucess(message=message)
        except Exception as e:
            error_message = {
                "error_message": e.args}
            return ApiResponse.failure(error_message)

class DeleteHotelUseCase:
    def execute(self, domain: DeleteHotelDomain):
        try:
            check_hotel = Hotel.objects.filter(hotel_name=domain.hotel_name)
            if list(check_hotel) == []:
                error_message = {
                    "error_message": f"The {domain.hotel_name} hotel to delete does not exist"}
                return ApiResponse.failure(error_message)
            get_hotel = Hotel.objects.get(hotel_name=domain.hotel_name)
            get_hotel.delete()
            message = {
                "message": f"The {domain.hotel_name} hotel was deleted"}
            return ApiResponse.sucess(message=message)
        except Exception as e:
            error_message = {
                "error_message": e.args}
            return ApiResponse.failure(error_message)

