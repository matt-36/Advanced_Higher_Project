from typing import List

import requests
from classes.holiday import Holiday

class Easyjet(Holiday):
    def __init__(self, 
            # super parameters**
            name: str,
            rating: float,
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
            transfer_id
            ) -> None:

        super().__init__(
            name,
            rating,
            ratings,
            price,
            deposit,
            stay,
            images,
            date
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

    def build_offerlink(self, flex, departure):
        date = self.date
        to = date[0:len(date)-3] + (date.split("-")[2] + self.stay)
        dst = self.hotel_location_code
        geog = self.hotel_country_code + f",{dst}"
        orgs = ""
        for i, airport in enumerate(departure):
            orgs += f"&org[{i}] = {airport}"
        # for i, unit in enumerate(offer['accom']['unit']):
        #   rooms += f"&"
        
        ret = "https://easyjet.com/holidays" +\
        self.hotel_url +\
        f"?ibf=true" +\
        f"&to={to}" +\
        f"&from={date}" +\
        f"&dst={dst}" +\
        f"&geog={geog}" +\
        f"&flex={flex}" +\
        f"&sAccId=" +\
        orgs
        # rooms +\
        ""

        return ret
    @staticmethod
    def from_json(data):
        #holiday
        name = data["hotel"]["name"]
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

        return Easyjet(name, rating, ratings, price, deposit, stay, images, date, resort_code, resort_name, resort_url, hotel_country_code, hotel_location_code, hotel_url, transport_id, accom_id, accom_pack_id, accom_unit_codes, accom_unit_boards, transfer_id)



class EasyjetSearchbar():
  def __init__(self) -> None: ...

  def query(self, query) -> List[dict]:
    # send request
    print(query)
    uri = "https://www.easyjet.com/holidays/_api/v1.0/destinations/search?query=" +\
        query +\
    "&flexibleDays=0"
    ret = requests.get(uri).json()
    print(ret)
    # sanatize data
    return ret["destinations"]