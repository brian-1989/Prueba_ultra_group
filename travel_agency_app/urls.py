from django.urls import path
from travel_agency_app.views.booking import (
    GetHotelAndRoomView,
    AddBookingView,
    UpdateBookingView,
    DeleteBookingView
)
from travel_agency_app.views.hotel import (
    GetAllHotelsView,
    CreateNewHotelView,
    UpdateHotelView,
    DeleteHotelView
)
from travel_agency_app.views.room import (
    AddRoomView,
    UpdateRoomView,
    DeleteRoomView
)

# Hotel
urlpatterns = [
    path('get_all_hotels/', GetAllHotelsView.as_view()),
    path('create_hotel/', CreateNewHotelView.as_view()),
    path('update_hotel/', UpdateHotelView.as_view()),
    path('delete_hotel/', DeleteHotelView.as_view()),
    path('add_room/', AddRoomView.as_view()),
    path('update_room/', UpdateRoomView.as_view()),
    path('delete_room/', DeleteRoomView.as_view()),
    path('get_hotels_and_rooms/', GetHotelAndRoomView.as_view()),
    path('add_booking/', AddBookingView.as_view()),
    path('update_booking/', UpdateBookingView.as_view()),
    path('delete_booking/', DeleteBookingView.as_view()),
]
