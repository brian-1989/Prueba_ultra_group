from rest_framework.views import APIView
from rest_framework.request import Request
from travel_agency_app.domain.hotel import (
    CreateNewHotelDomain,
    UpdateHotelDomain,
    DeleteHotelDomain
)
from travel_agency_app.serializers.hotel import (
    CreateNewHotelSerializer,
    UpdateHotelSerializer
)
from travel_agency_app.use_cases.hotel import (
    GetAllHotelsUseCase,
    CreateNewHotelUseCase,
    UpdateHotelUseCase,
    DeleteHotelUseCase
)

class GetAllHotelsView(APIView):
    def get(self, request: Request):
        uc = GetAllHotelsUseCase()
        return uc.execute()

class CreateNewHotelView(APIView):
    def get(self, request: Request):
        serializer = CreateNewHotelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        domain = CreateNewHotelDomain(**serializer.data)
        uc = CreateNewHotelUseCase()
        return uc.execute(domain=domain)

    # def post(self, request: Request):
    #     serializer = CreateNewHotelSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     domain = CreateNewHotelDomain(**serializer.data)
    #     uc = CreateNewHotelUseCase()
    #     return uc.execute(domain=domain)

class UpdateHotelView(APIView):
    def put(self, request: Request):
        serializer = UpdateHotelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        domain = UpdateHotelDomain(**serializer.data)
        uc = UpdateHotelUseCase()
        return uc.execute(domain=domain)

class DeleteHotelView(APIView):
    def delete(self, request: Request):
        serializer = CreateNewHotelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        domain = DeleteHotelDomain(**serializer.data)
        uc = DeleteHotelUseCase()
        return uc.execute(domain=domain)
