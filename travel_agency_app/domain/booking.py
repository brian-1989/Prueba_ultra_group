import dataclasses
import json

@dataclasses.dataclass
class Passenger:
    name: str = None
    last_name: str = None
    genre: str = None
    document_type: str = None
    document_number: int = 0
    email: str = None
    cellphone_number: str = None
    booking: str = None

    @classmethod
    def from_dict(cls, data):
        return cls(
            name = data['name'],
            last_name = data['last_name'],
            genre = data['genre'],
            document_type = data['document_type'],
            document_number = data['document_number'],
            email = data['email'],
            cellphone_number = data['cellphone_number']
        )

@dataclasses.dataclass
class AddBookingDomain:
    passenger: Passenger = None
    create_date: str = None
    begin_date: str = None
    end_date: str = None
    hotel_name: str = None
    room_location: str = None
    emergency_contact_name: str = None
    emergency_contact_cellpohne_number: int = 0

    @classmethod
    def from_dict(cls, data):
        return cls(
            passenger = [Passenger.from_dict(passenger) for passenger in json.loads(json.dumps(data['passenger']))],
            begin_date = data['begin_date'],
            end_date = data['end_date'],
            hotel_name = data['hotel_name'],
            room_location = data['room_location'],
            emergency_contact_name = data['emergency_contact_name'],
            emergency_contact_cellpohne_number = data['emergency_contact_cellpohne_number']
        )

@dataclasses.dataclass
class UpdateBookingDomain:
    hotel_name: str = None
    room_location: str = None
    field: str = None
    value: str = None

@dataclasses.dataclass
class DeleteBookingDomain:
    hotel_name: str = None
    room_location: str = None

@dataclasses.dataclass
class BookingSearchDomian:
    begin_date: str = None
    end_date: str = None
    hotel_name: str = None
    room_location: str = None
    passenger_number: int = 0
    city_name: str = None
