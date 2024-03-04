import datetime
from datetime import date, timedelta
from typing import List

import requests

from classes.easyjet import Easyjet, EasyjetSearchbar
from classes.holiday import Holiday


class Query:
    """
    a `Query` contains all relevant user entered information used to formulate provider query urls.
    """

    def __init__(self, start: str, duration: int, departure, destination, who) -> None:
        if not start:
            self.start = datetime.datetime.strftime(
                datetime.datetime.now() + timedelta(1), "%d%m%Y"
            )
        else:
            self.start = start

        self.duration = duration
        self.departure = departure
        self.destination = destination
        self.who = who

    def build_easyjet(
        self,
        startDate,
        flex=0,
        duration=7,
        departure="LGW",
        geo="ES",
        rooms=[{"adults": 2, "children": 0, "infants": 0}],
        searchType="normal",
        destination={"code": "ES", "type": "country"},
    ) -> str:
        def create_rooms(rooms):
            ret = ""
            for i, room in enumerate(rooms):
                ret += f"&room[{i}].adults={room['adults']}&room[{i}].children={room['children']}&room[{i}].infants={room['infants']}"
            return ret

        ret = (
            "https://www.easyjet.com/holidays/_api/v1.0/search/packages"
            + f"?startDate={startDate}"
            + f"&flexibleDays={flex}"
            + f"&duration[0]={duration}"
            + f"&departure={departure}"
            + f"&geography={geo.split(',')[0]}"
            + f"&automaticAllocation=true"
            + create_rooms(rooms)
            + f"&take=20"
            + f"&page=1"
            + f"&searchType={searchType}"
            + f"&distressedFlightsOnly=false"
            + f"&placementId=hotels_list"
            + f"&destinations[0]={destination['type']}:{destination['code'].split(',')[0]}"
        )
        print(ret)
        return ret

    def query(self) -> List[Holiday]:
        """
        Sends query to providers and collects responses
        """

        # Currently only for easyjet as it is designed.

        easyjet_req = requests.get(
            self.build_easyjet(
                self.start,
                0,
                self.duration,
                self.departure,
                self.destination,
                [{"adults": self.who, "children": 0, "infants": 0}],
                "normal",
                {"code": self.destination, "type": "country"},
            )
        )
        print(easyjet_req)
        easyjets_json = easyjet_req.json()["offers"]
        easyjets = []
        for ej in easyjets_json:
            easyjet = Easyjet.from_json(ej)
            easyjet.url = easyjet.build_offerlink(self.who, self.departure)
            print(easyjet)
            easyjets.append(easyjet)

        ret = self.bubble_sort_holidays(easyjets)
        return ret

    def bubble_sort_holidays(self, holidays: List[Holiday]) -> List[Holiday]:
        n = len(holidays)
        for i in range(n):
            for j in range(0, n - i - 1):
                if holidays[j].price > holidays[j + 1].price:
                    holidays[j], holidays[j + 1] = holidays[j + 1], holidays[j]
        return holidays

    def __str__(self) -> str:
        # on d date goto y location for t days to return to x location
        return str(self.start) + self.destination + str(self.duration) + self.departure


class SearchbarResult:
    def __init__(self, name, code, _type, available, provider) -> None:
        """
        Params
        --------

        """
        # general
        self.name = name
        self.type = _type
        # provider specific
        self.code = code
        self.available = available
        self.provider = provider

    @staticmethod
    def from_easyjet(data):
        name = data["name"]
        code = data["code"]
        t = data["type"]
        a = data["available"] == "true"
        return SearchbarResult(name, code, t, a, "ej")

    @staticmethod
    def from_thomascook(data):
        name = data["name"]
        code = data["id"]
        t = data["type"]
        a = data["count"] != "0"
        return SearchbarResult(name, code, t, a, "tc")

    @staticmethod
    def from_jet2(data):
        ...


class Searchbar:
    """
    An instance of `Searchbar` is created for the search page to fetch the correct data to use for search quey
    """

    def __init__(self) -> None:
        self.easyjet = EasyjetSearchbar()
        self.ALLOWTYPES = ["Country", "1"]
        self.results: List[SearchbarResult] = []

    def fetch_results(self, query):
        self.results = []
        ejres = self.easyjet.query(query)
        for res in ejres:
            self.results.append(SearchbarResult.from_easyjet(res))
        ret = self.join_result()
        return ret

    def join_result(self) -> List[dict]:
        # find locations with matching names and create dict name: {easyjet: {...}, thomascook: {...}, ...}
        res = {}
        ret = []
        for result in self.results:
            print(
                result.name, result.provider, result.code, result.available, result.type
            )
            if result.type in self.ALLOWTYPES:
                res[result.name] = {}
                res[result.name]["ej"] = {"code": ""}
                res[result.name]["tc"] = {"code": ""}
                res[result.name]["j2"] = {"code": ""}
                res[result.name]["tu"] = {"code": ""}
                res[result.name][result.provider] = {"code": result.code}
        for k, v in res.items():
            print(k, v)
            tmp = v
            tmp["name"] = k
            ret.append(tmp)
        return ret
