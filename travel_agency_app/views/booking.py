from collections import OrderedDict
from rest_framework.views import APIView
from rest_framework.request import Request
from travel_agency_app.domain.booking import (
    AddBookingDomain,
    UpdateBookingDomain,
    DeleteBookingDomain,
    BookingSearchDomian
)
from travel_agency_app.use_cases.booking import (
    GetHotelAndRoomUseCase,
    AddBookingUseCase,
    UpdateBookingUseCase,
    DeletebookingUseCase,
    BookingSearchUseCase
)
from travel_agency_app.serializers.booking import (
    AddBookingSerializer,
    UpdateBookingSerializer,
    DeleteBookingSerializer,
    BookingSearchSerializer
)

class GetHotelAndRoomView(APIView):
    def get(self, requets: Request):
        uc = GetHotelAndRoomUseCase()
        return uc.execute()

class AddBookingView(APIView):
    def post(self, request: Request):
        serializer = AddBookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        domain = AddBookingDomain.from_dict(serializer.data)
        uc = AddBookingUseCase()
        return uc.execute(domain=domain)

class UpdateBookingView(APIView):
    def put(self, request: Request):
        serializer = UpdateBookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        domain = UpdateBookingDomain(**serializer.data)
        uc = UpdateBookingUseCase()
        return uc.execute(domain=domain)

class DeleteBookingView(APIView):
    def delete(self, request: Request):
        serialiazer = DeleteBookingSerializer(data=request.data)
        serialiazer.is_valid(raise_exception=True)
        domain = DeleteBookingDomain(**serialiazer.data)
        uc = DeletebookingUseCase()
        return uc.execute(domain=domain)

class BookingSearchView(APIView):
    def post(self, request: Request):
        serialiazer = BookingSearchSerializer(data=request.data)
        serialiazer.is_valid(raise_exception=True)
        domian = BookingSearchDomian(**serialiazer.data)
        uc = BookingSearchUseCase()
        return uc.excute(domain=domian)
