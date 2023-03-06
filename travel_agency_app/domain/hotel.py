import dataclasses

@dataclasses.dataclass
class CreateNewHotelDomain:
    create_date: str = None
    hotel_name: str = None
    enable: bool = True

@dataclasses.dataclass
class UpdateHotelDomain:
    hotel_name: str = None
    field: str = None
    value: str = None

@dataclasses.dataclass
class DeleteHotelDomain:
    hotel_name: str = None