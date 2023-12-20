from typing import List
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

    
    def from_json(json):
        #holiday
        name = json["hotel"]["name"]
        rating = json["hotel"]["rating"]
        ratings = json["hotel"]["numberOfReviews"]
        price = json["price"]
        deposit = json["deposit"]
        stay = json["stay"]
        images = [img["medium"] for img in json["hotel"]["images"]]
        date = json["date"]
        # easyjet
        resort_code = json["hotel"]["resort"]["code"]
        resort_name = json["hotel"]["resort"]["name"]
        resort_url = json["hotel"]["resort"]["url"]
        hotel_country_code = json["hotel"]["country"]["code"]
        hotel_location_code = json["hotel"]["location"]["code"]
        hotel_url = json["hotel"]["url"]
        transport_id = [tp["id"] for tp in json["transport"]["routes"]]
        accom_id = json["accom"]["id"]
        accom_pack_id = json["accom"]["packageId"]
        accom_unit_codes = [unit["code"] for unit in json["accom"]["unit"]]
        accom_unit_boards = [unit["board"] for unit in json["accom"]["unit"]]
        transfer_id = [transfer["code"] for transfer in json["transfers"]]

        return Easyjet(name, rating, ratings, price, deposit, stay, images, date, resort_code, resort_name, resort_url, hotel_country_code, hotel_location_code, hotel_url, transport_id, accom_id, accom_pack_id, accom_unit_codes, accom_unit_boards, transfer_id)