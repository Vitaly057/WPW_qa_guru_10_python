import dataclasses


@dataclasses.dataclass
class User:
    username: str
    password: str