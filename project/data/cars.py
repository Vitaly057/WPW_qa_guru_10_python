import dataclasses


@dataclasses.dataclass
class Car:
    vin: str
    manufacturer: str
    model: str