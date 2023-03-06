import dataclasses

@dataclasses.dataclass
class AddRoomDomain:
    create_date: str = None
    hotel_name: str = None
    amount: int = 0
    tax: int = 0
    room_type: str = None
    room_location: str = None
    enable: bool = True
    booking: bool = True

@dataclasses.dataclass
class UpdateRoomDomain:
    hotel_name: str = None
    room_location: str = None
    field: str = None
    value: str = None

@dataclasses.dataclass
class DeleteRoomDomain:
    hotel_name: str = None
    room_location: str = None
