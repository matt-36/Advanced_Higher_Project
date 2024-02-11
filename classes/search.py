from datetime import date, timedelta
import datetime
from typing import List

import requests

from classes.holiday import Holiday
from classes.easyjet import Easyjet, EasyjetSearchbar

class Query:
  """
  a `Query` contains all relevant user entered information used to formulate provider query urls.
  """
  def __init__(self, start:str, duration:int, departure, destination, who) -> None:
    if not start: self.start = datetime.datetime.strftime(datetime.datetime.now() + timedelta(1), "%d%m%Y")
    else: self.start = start

    self.duration = duration
    self.departure = departure
    self.destination = destination
    self.who = who
  # def build_easyjet(self) -> str:
  #   return "/search/packages?startDate=2024-06-05&flexibleDays=0&duration[0]=7&departure=LGW&geography=GR,GRZA&automaticAllocation=true&room[0].adults=2&room[0].children=0&room[0].infants=0&=&=&take=10&page=1&searchType=normal&distressedFlightsOnly=false&placementId=hotels_list"
  def build_easyjet(startDate, flex=0, duration=7, departure="LGW", geo="ES", rooms=[{"adults":2,"children":0,"infants":0}], searchType="normal", destination={"code":"ES","type":"country"}) -> str:
    def create_rooms(rooms):
      ret = ""
      for i,room in enumerate(rooms):
        ret += f"&room[{i}].adults={room['adults']}&room[{i}].children={room['children']}&room[{i}].infants={room['infants']}"
      return ret
    ret = "https://www.easyjet.com/holidays/_api/v1.0" + "search/packages" +\
    f"?startDate={startDate}" +\
    f"&flexibleDays={flex}" +\
    f"&duration[0]={duration}" +\
    f"&departure={departure}" +\
    f"&geography={geo}" +\
    f"&automaticAllocation=true" +\
    create_rooms(rooms) +\
    f"&take=10" +\
    f"&page=1" +\
    f"&searchType={searchType}" +\
    f"&distressedFlightsOnly=false" +\
    f"&placementId=hotels_list" +\
    f"&destination={destination}"
    return ret

  
  def query(self) -> List[Holiday]:
    """
    Sends query to providers and collects responses
    """

    # Currently only for easyjet as it is designed.

    easyjet_req = requests.get(
      self.build_easyjet()
    )
    easyjets_json = easyjet_req.json()["offers"]
    easyjets = []
    for ej in easyjets_json:
      easyjet = Easyjet.from_json(ej)
      print(easyjet)
      easyjets.append(easyjet)

    return easyjets


  def __str__(self) -> str:
    # on d date goto y location for t days to return to x location
    return str(self.start) + self.destination + str(self.duration) + self.departure



class SearchbarResult():
  def __init__(self, name,code,_type,available,provider) -> None:
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
    return SearchbarResult(name,code,t,a, "ej")

  @staticmethod
  def from_thomascook(data):
    name = data["name"]
    code = data["id"]
    t = data["type"]
    a = data["count"] != "0"
    return SearchbarResult(name,code,t,a, "tc")

  @staticmethod
  def from_jet2(data): ...





class Searchbar():
  """
  An instance of `Searchbar` is created for the search page to fetch the correct data to use for search quey
  """
  def __init__(self) -> None:
    self.easyjet = EasyjetSearchbar()
    ...
    self.results: List[SearchbarResult] = []

  def fetch_results(self, query):
    ejres = self.easyjet.query(query)
    for res in ejres:
      self.results.append(
        SearchbarResult.from_easyjet(res)
      )
    # join results here
    print(ejres)
    return ejres

  def join_result(self) -> List[dict]:
    # find locations with matching names and create dict name: {easyjet: {...}, thomascook: {...}, ...}
    ret = {}
    for result in self.results:
      ret[result.name]
    return [{}]