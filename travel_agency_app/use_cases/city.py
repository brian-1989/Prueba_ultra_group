from datetime import datetime
from travel_agency_app.domain.city import (
    CreateNewCityDomain,
    UpdateCityDomain,
    DeleteCityDomain
)
from travel_agency_app.models.city import City
from travel_agency_app.responses import ApiResponse
import pytz

class GetAllCitiesUseCase:
    def execute(self):
        try:
            get_all_cities = City.objects.all().values("city_name")
            response = dict(cities = list(get_all_cities))
            return ApiResponse.sucess(message=response)
        except Exception as exc:
            error_message = {
                "error_message": exc.args}
            return ApiResponse.failure(error_message=error_message)

class CreateNewCityUseCase:
    def execute(self, domain: CreateNewCityDomain):
        try:
            check_city = City.objects.filter(city_name=domain.city_name)
            if list(check_city) != []:
                error_message = {
                    "error_message": f"The {domain.city_name} city is already registered"}
                return ApiResponse.failure(error_message)
            domain.create_date = datetime.now(
                tz=pytz.timezone('America/Bogota')).strftime("%m/%d/%Y, %H:%M:%S")
            city_store = City(**domain.__dict__)
            city_store.save()
            message = {"status": "Done"}
            return ApiResponse.sucess(message=message)
        except Exception as exc:
            error_message = {
                "error_message": exc.args}
            return ApiResponse.failure(error_message=error_message)

class UpdateCityUseCase:
    def execute(self, domain: UpdateCityDomain):
        try:
            check_city = City.objects.filter(city_name=domain.city_name)
            if list(check_city) == []:
                error_message = {
                    "error_message": f"The {domain.city_name} city to update does not exist"}
                return ApiResponse.failure(error_message)
            get_city = City.objects.get(city_name=domain.city_name)
            if domain.field == "city_name":
                get_city.city_name = domain.value
            elif domain.field == "enable":
                get_city.enable = domain.value
            else:
                error_message = {
                    "error_message": f"The {domain.field} field to update does not exist"}
                return ApiResponse.failure(error_message)
            get_city.save()
            message = {
                "message": f"The {domain.field} field has been update by {domain.value}"}
            return ApiResponse.sucess(message=message)
        except Exception as e:
            error_message = {
                "error_message": e.args}
            return ApiResponse.failure(error_message)

class DeleteCityUseCase:
    def execute(self, domain: DeleteCityDomain):
        try:
            check_city = City.objects.filter(city_name=domain.city_name)
            if list(check_city) == []:
                error_message = {
                    "error_message": f"The {domain.city_name} city to delete does not exist"}
                return ApiResponse.failure(error_message)
            get_city = City.objects.get(city_name=domain.city_name)
            get_city.delete()
            message = {
                "message": f"The {domain.city_name} city was deleted"}
            return ApiResponse.sucess(message=message)
        except Exception as e:
            error_message = {
                "error_message": e.args}
            return ApiResponse.failure(error_message)
