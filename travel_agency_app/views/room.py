from rest_framework.views import APIView
from rest_framework.request import Request
from travel_agency_app.domain.room import (
    AddRoomDomain,
    UpdateRoomDomain,
    DeleteRoomDomain
)
from travel_agency_app.serializers.room import (
    AddRoomSerializer,
    UpdateRoomSerializar,
    DeleteRoomSerializer
)
from travel_agency_app.use_cases.room import (
    AddRoomUseCase,
    UpdateRoomUseCase,
    DeleteRoomUseCase
)

class AddRoomView(APIView):
    def post(self, request: Request):
        serializer = AddRoomSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        domain = AddRoomDomain(**serializer.data)
        uc = AddRoomUseCase()
        return uc.execute(domain=domain)

class UpdateRoomView(APIView):
    def put(self, request: Request):
        serializer = UpdateRoomSerializar(data=request.data)
        serializer.is_valid(raise_exception=True)
        domain = UpdateRoomDomain(**serializer.data)
        uc = UpdateRoomUseCase()
        return uc.execute(domain=domain)
        

class DeleteRoomView(APIView):
    def delete(self, request: Request):
        serialiazer = DeleteRoomSerializer(data=request.data)
        serialiazer.is_valid(raise_exception=True)
        domain = DeleteRoomDomain(**serialiazer.data)
        uc = DeleteRoomUseCase()
        return uc.execute(domain=domain)
