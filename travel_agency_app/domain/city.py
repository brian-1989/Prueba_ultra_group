import dataclasses

@dataclasses.dataclass
class CreateNewCityDomain:
    create_date: str = None
    city_name: str = None
    enable: bool = True

@dataclasses.dataclass
class UpdateCityDomain:
    city_name: str = None
    field: str = None
    value: str = None

@dataclasses.dataclass
class DeleteCityDomain:
    city_name: str = None
