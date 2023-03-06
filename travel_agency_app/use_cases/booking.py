from datetime import datetime
from django.conf import settings
from email.message import EmailMessage
from travel_agency_app.domain.booking import (
    AddBookingDomain,
    UpdateBookingDomain,
    DeleteBookingDomain
)
from travel_agency_app.models.booking import Booking, Passenger
from travel_agency_app.models.hotel import Hotel
from travel_agency_app.models.room import Room
from travel_agency_app.responses import ApiResponse
import pytz
import smtplib, ssl


class GetHotelAndRoomUseCase:
    def execute(self):
        try:
            get_hotels = Hotel.objects.filter(
                enable=True).values(
                "id", "hotel_name")
            response = {}
            for hotel in get_hotels:
                get_rooms = Room.objects.filter(
                    hotel_name_id=hotel.get("id"), enable=True, booking=False).values(
                    'amount', 'tax', 'room_type', 'room_location')
                room_list = list(get_rooms)
                if room_list != []:
                    response[hotel.get('hotel_name')] = [room for room in room_list]
            return ApiResponse.sucess(message=response)
        except Exception as exc:
            error_message = {
                "error_message": exc.args}
            return ApiResponse.failure(error_message)

class AddBookingUseCase:
    def execute(self, domain: AddBookingDomain):
        check_dates = self.check_dates(domain=domain)
        if check_dates and check_dates.status_code == 400:
            return check_dates
        response_add_booking = self.add_booking(domain=domain)
        if response_add_booking and response_add_booking.status_code == 400:
            return response_add_booking
        response_add_passenger = self.add_passenger(domain=domain)
        if response_add_passenger and response_add_passenger.status_code == 400:
            return response_add_booking
        self.send_email(domain=domain)
        message = {"status": "Done"}
        return ApiResponse.sucess(message=message)

    def check_dates(self, domain: AddBookingDomain):
        begin_date = datetime.strptime(domain.begin_date, "%d/%m/%Y").date()
        end_date = datetime.strptime(domain.end_date, "%d/%m/%Y").date()
        today_date = datetime.now(tz=pytz.timezone('America/Bogota')).date()
        if begin_date < today_date:
            error_message = {
                "error_message": f"The {domain.begin_date} date is invalid"}
            return ApiResponse.failure(error_message)
        elif end_date < today_date:
            error_message = {
                "error_message": f"The {domain.end_date} date is invalid"}
            return ApiResponse.failure(error_message)
        elif begin_date > end_date:
            error_message = {
                "error_message": f"The {domain.begin_date} and {domain.end_date} dates is invalid"}
            return ApiResponse.failure(error_message)
        else:
            return

    def check_booking(self, domain: AddBookingDomain):
        print(domain.hotel_name)
        get_booking = Booking.objects.get(
            hotel_name=domain.hotel_name)
        today_date = datetime.now(tz=pytz.timezone('America/Bogota')).date()
        end_date = datetime.strptime(get_booking.end_date, "%d/%m/%Y").date()
        if end_date > today_date:
            get_booking.delete()
            get_hotel_id = Hotel.objects.get(hotel_name=domain.hotel_name).pk
            get_room = Room.objects.get(
                room_location=domain.room_location, hotel_name=get_hotel_id)
            get_room.booking = False
        return

    def add_booking(self, domain: AddBookingDomain):
        try:
            print(domain.hotel_name)
            check_booking = Booking.objects.filter(
                hotel_name=domain.hotel_name, room_location=domain.room_location)
            if list(check_booking) != []:
                error_message = {
                    "error_message": f"The {domain.room_location} at {domain.hotel_name} hotel, is reserved"}
                return ApiResponse.failure(error_message)
            check_hotel = Hotel.objects.filter(hotel_name=domain.hotel_name)
            if list(check_hotel) == []:
                error_message = {
                    "error_message": f"The {domain.hotel_name} hotel to update does not exist"}
                return ApiResponse.failure(error_message)
            get_hotel_id = Hotel.objects.get(hotel_name=domain.hotel_name).pk
            check_room = Room.objects.filter(
                hotel_name=get_hotel_id, room_location=domain.room_location)
            if list(check_room) == []:
                error_message = {
                    "error_message": f"The {domain.room_location} room is not registered at {domain.hotel_name} hotel"}
                return ApiResponse.failure(error_message)
            domain.create_date = datetime.now(
                tz=pytz.timezone('America/Bogota')).strftime("%m/%d/%Y, %H:%M:%S")
            add_booking = Booking(
                create_date=domain.create_date,
                begin_date=domain.begin_date,
                end_date=domain.end_date,
                hotel_name=domain.hotel_name,
                room_location=domain.room_location,
                emergency_contact_name=domain.emergency_contact_name,
                emergency_contact_cellpohne_number=domain.emergency_contact_cellpohne_number)
            add_booking.save()
            get_room = Room.objects.get(
                hotel_name=get_hotel_id,
                room_location=domain.room_location)
            get_room.booking = True
            get_room.save()
            return
        except Exception as exc:
            error_message = {
                "error_message": exc.args}
            return ApiResponse.failure(error_message)

    def add_passenger(self, domain: AddBookingDomain):
        try:
            get_booking_instance = Booking.objects.get(room_location=domain.room_location)
            for passenger in domain.passenger:
                passenger.booking = get_booking_instance
                add_passenger = Passenger(**passenger.__dict__)
                add_passenger.save()
            return
        except Exception as exc:
            error_message = {
                "error_message": exc.args}
            return ApiResponse.failure(error_message)

    def send_email(self, domain: AddBookingDomain):
        subject = "Welcome to your booking"
        message_to_send = f"Hi {domain.passenger[0].name} {domain.passenger[0].last_name}, thank you registering your reservation at {domain.hotel_name} hotel, in the {domain.room_location} room"
        # port for SSL
        port = settings.SMTP_PORT
        # smtp mail server that uses gmail mail
        smtp_server = settings.SMTP_SERVER
        # sender email
        sender_email = settings.SENDER_EMAIL
        # receiver email
        receiver_email = domain.passenger[0].email
        # app password
        password = settings.EMAIL_PASSWORD
        message = EmailMessage()
        message['Subject'] = subject
        message['From'] = sender_email
        message['To'] = receiver_email
        message.set_content(message_to_send)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port=port, context=context) as server_connection:
            server_connection.login(sender_email, password)
            server_connection.send_message(message)

class UpdateBookingUseCase:
    def execute(self, domain: UpdateBookingDomain):
        try:
            check_hotel = list(Hotel.objects.filter(hotel_name=domain.hotel_name))
            if check_hotel == []:
                error_message = {
                    "error_message": f"The {domain.hotel_name} hotel is already registered"}
                return ApiResponse.failure(error_message)
            get_hotel_id = Hotel.objects.get(hotel_name=domain.hotel_name).pk
            check_room = Room.objects.filter(
                hotel_name=get_hotel_id, room_location=domain.room_location)
            if list(check_room) == []:
                error_message = {
                    "error_message": f"The {domain.room_location} room is not registered at {domain.hotel_name} hotel"}
                return ApiResponse.failure(error_message)
            get_booking = Booking.objects.get(
                hotel_name=domain.hotel_name, room_location=domain.room_location)
            if domain.field == "begin_date":
                check_date = self.check_dates(
                    begin_date=domain.value, end_date=get_booking.end_date)
                if check_date and check_date.status_code == 400:
                    return check_date
                get_booking.begin_date = domain.value
            elif domain.field == "end_date":
                check_date = self.check_dates(
                    begin_date=get_booking.begin_date, end_date=domain.value)
                if check_date and check_date.status_code == 400:
                    return check_date
                get_booking.end_date = domain.value
            elif domain.field == "emergency_contact_name":
                get_booking.emergency_contact_name = domain.value
            elif domain.field == "emergency_contact_cellpohne_number":
                get_booking.emergency_contact_cellpohne_number = domain.value
            else:
                error_message = {
                    "error_message": f"The {domain.field} field to update does not exist"}
                return ApiResponse.failure(error_message)
            get_booking.save()
            message = {
                "message": f"The {domain.field} field has been update by {domain.value}"}
            return ApiResponse.sucess(message=message)
        except Exception as exc:
            error_message = {
                "error_message": exc.args}
            return ApiResponse.failure(error_message)

    def check_dates(self, begin_date, end_date):
        begin_date_obj = datetime.strptime(begin_date, "%d/%m/%Y").date()
        end_date_obj = datetime.strptime(end_date, "%d/%m/%Y").date()
        today_date = datetime.now(tz=pytz.timezone('America/Bogota')).date()
        if begin_date_obj < today_date:
            error_message = {
                "error_message": f"The {begin_date} date is invalid"}
            return ApiResponse.failure(error_message)
        elif end_date_obj < today_date:
            error_message = {
                "error_message": f"The {end_date} date is invalid"}
            return ApiResponse.failure(error_message)
        elif begin_date_obj > end_date_obj:
            error_message = {
                "error_message": f"The {begin_date} and {end_date} dates is invalid"}
            return ApiResponse.failure(error_message)
        else:
            return

class DeletebookingUseCase:
    def execute(self, domain: DeleteBookingDomain):
        try:
            check_hotel = list(Hotel.objects.filter(hotel_name=domain.hotel_name))
            if check_hotel == []:
                error_message = {
                    "error_message": f"The {domain.hotel_name} hotel is not registered"}
                return ApiResponse.failure(error_message)
            get_hotel_id = Hotel.objects.get(hotel_name=domain.hotel_name).pk
            check_booking = Booking.objects.filter(
                hotel_name=domain.hotel_name, room_location=domain.room_location)
            if list(check_booking) == []:
                error_message = {
                    "error_message": f"The booking is not registered"}
                return ApiResponse.failure(error_message)
            Booking.objects.get(
                hotel_name=domain.hotel_name, room_location=domain.room_location).delete()
            message = {
                "message": f"The booking of room {domain.room_location}, {domain.hotel_name} Hotel, has been eliminated."}
            return ApiResponse.sucess(message=message)
        except Exception as exc:
            error_message = {
                "error_message": exc.args}
            return ApiResponse.failure(error_message)