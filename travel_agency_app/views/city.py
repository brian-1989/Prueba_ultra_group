from rest_framework.request import Request
from rest_framework.views import APIView
from travel_agency_app.domain.city import (
    CreateNewCityDomain,
    UpdateCityDomain,
    DeleteCityDomain
)
from travel_agency_app.serializers.city import (
    CreateNewCitySerializer,
    UpdateCitySerializer
)
from travel_agency_app.use_cases.city import (
    GetAllCitiesUseCase,
    CreateNewCityUseCase,
    UpdateCityUseCase,
    DeleteCityUseCase
)

class GetAllCitiesView(APIView):
    def get(self, request: Request):
        uc = GetAllCitiesUseCase()
        return uc.execute()

class CreateNewCityView(APIView):
    def post(self, request: Request):
        serializer = CreateNewCitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        domain = CreateNewCityDomain(**serializer.data)
        uc = CreateNewCityUseCase()
        return uc.execute(domain=domain)

class UpdateCityView(APIView):
    def put(self, request: Request):
        serializer = UpdateCitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        domain = UpdateCityDomain(**serializer.data)
        uc = UpdateCityUseCase()
        return uc.execute(domain=domain)

class DeleteCityView(APIView):
    def delete(self, request: Request):
        serializer = CreateNewCitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        domain = DeleteCityDomain(**serializer.data)
        uc = DeleteCityUseCase()
        return uc.execute(domain=domain)
