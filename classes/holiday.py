import datetime
from typing import List


class Holiday:
    def __init__(
        self,
        name: str,
        starrating: int,
        rating: int,
        ratings: int,
        price: float,
        deposit: float,
        stay: int,
        images: List[str],
        date: str,
    ) -> None:
        self.name: str = name
        self.starrating: int = int(starrating)
        self.rating: float = rating
        self.ratings: int = ratings
        self.price: float = price
        self.deposit: float = deposit
        self.stay: int = stay
        self.images: List[str] = images
        self.url = ""

        def to_from_str(t: str) -> str:
            t = t.split("T")[0]
            t = t.replace("/", "")
            t = t.replace("-", "")
            ret = datetime.datetime.strptime(t, "%Y%m%d").date() + datetime.timedelta(
                self.stay
            )
            return ret.strftime("%d-%m-%Y")

        self.date: str = date
        self.to: str = to_from_str(date)

    def get_provider(self) -> str:
        t = type(self)
        return str(t)

    def __str__(self) -> str:
        print(self.name, self.price)
        return str(self.name) + ": " + str(self.price)

    def to_json(self) -> dict:
        return self.__dict__
