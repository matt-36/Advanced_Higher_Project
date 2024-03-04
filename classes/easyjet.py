import datetime
from typing import List

import requests

from classes.holiday import Holiday


class Easyjet(Holiday):
    def __init__(
        self,
        # super parameters**
        name: str,
        starrating: int,
        rating: int,
        ratings: int,
        price: float,
        deposit: float,
        stay: int,
        images: List[str],
        date: str,
        # subclass parameters*
        resort_code,
        resort_name,
        resort_url,
        hotel_country_code,
        hotel_location_code,
        hotel_url,
        transport_id,
        accom_id,
        accom_pack_id,
        accom_unit_codes,
        accom_unit_boards,
        transfer_id,
    ) -> None:

        super().__init__(
            name, starrating, rating, ratings, price, deposit, stay, images, date
        )

        self.resort_code = resort_code
        self.resort_name = resort_name
        self.resort_url = resort_url
        self.hotel_country_code = hotel_country_code
        self.hotel_location_code = hotel_location_code
        self.hotel_url = hotel_url
        self.transport_id = transport_id
        self.accom_id = accom_id
        self.accom_pack_id = accom_pack_id
        self.accom_unit_codes = accom_unit_codes
        self.accom_unit_boards = accom_unit_boards
        self.transfer_id = transfer_id

    def build_offerlink(self, who, departure) -> str:
        print(self.date)
        tmp = self.date.split("T")[0]
        print(tmp)
        date = datetime.datetime.strptime(tmp, "%Y-%m-%d")
        to = date + datetime.timedelta(days=self.stay)
        date = date.strftime("%d-%m-%Y")
        to = to.strftime("%d-%m-%Y")
        dst = self.hotel_country_code
        geog = f"{dst}," + self.hotel_location_code
        org = departure

        ret = (
            "https://easyjet.com/holidays"
            + self.hotel_url
            + "?ibf=true"
            + f"&to={to}"
            + f"&from={date}"
            + f"&dst={dst}"
            + f"&geog={geog}"
            + "&flex=0"
            + "&sAccId="
            + f"&org={org}"
            + "&aa=1"
            + f"&rooms={who}"
            + f"&outId={self.transport_id[0]}"
            + f"&inId={self.transport_id[1]}"
            + f"&accId={self.accom_id}"
            + f"&packId={self.accom_pack_id}"
            + f"&offerCode={self.accom_id}_{self.accom_pack_id}_{self.accom_unit_codes[0]}"
            + f"&boardType={self.accom_unit_boards[0]}"
            + f"&offerRooms={who}/{self.accom_unit_codes[0]}"
            # + f"&transfer={self.transfer_id[0]}"
            # + f"&dtransfer={self.transfer_id[0]}"
        )

        return ret

    @staticmethod
    def from_json(data):
        # holiday
        name = data["hotel"]["name"]
        starrating = data["hotel"]["starRating"]
        rating = data["hotel"]["rating"]
        ratings = data["hotel"]["numberOfReviews"]
        price = data["price"]
        deposit = data["deposit"]
        stay = data["stay"]
        images = [img["medium"] for img in data["hotel"]["images"]]
        date = data["date"]
        # easyjet
        resort_code = data["hotel"]["resort"]["code"]
        resort_name = data["hotel"]["resort"]["name"]
        resort_url = data["hotel"]["resort"]["url"]
        hotel_country_code = data["hotel"]["country"]["code"]
        hotel_location_code = data["hotel"]["location"]["code"]
        hotel_url = data["hotel"]["url"]
        transport_id = [tp["id"] for tp in data["transport"]["routes"]]
        accom_id = data["accom"]["id"]
        accom_pack_id = data["accom"]["packageId"]
        accom_unit_codes = [unit["code"] for unit in data["accom"]["unit"]]
        accom_unit_boards = [unit["board"] for unit in data["accom"]["unit"]]
        transfer_id = [transfer["code"] for transfer in data["transfers"]]

        return Easyjet(
            name,
            starrating,
            rating,
            ratings,
            price,
            deposit,
            stay,
            images,
            date,
            resort_code,
            resort_name,
            resort_url,
            hotel_country_code,
            hotel_location_code,
            hotel_url,
            transport_id,
            accom_id,
            accom_pack_id,
            accom_unit_codes,
            accom_unit_boards,
            transfer_id,
        )

    def get_provider(self) -> str:
        return "EasyJet"


class EasyjetSearchbar:
    def __init__(self) -> None:
        ...

    def query(self, query) -> List[dict]:
        # send request
        print(query)
        uri = (
            "https://www.easyjet.com/holidays/_api/v1.0/destinations/search?query="
            + query
            + "&flexibleDays=0"
        )
        ret = requests.get(uri).json()["destinations"]
        print(ret)
        # sanatize data
        return ret