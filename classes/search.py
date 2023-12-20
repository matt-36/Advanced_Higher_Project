from datetime import date, timedelta
import datetime
from typing import List

import requests

from classes.holiday import Holiday
from classes.easyjet import Easyjet

class Query:
  """
  a `Query` contains all relevant user entered information used to formulate provider query urls.
  """
  def __init__(self, start:str, duration:int, departure, destination) -> None:
    if not start: self.start = datetime.datetime.strftime(datetime.datetime.now() + timedelta(1), "%d%m%Y")
    else: self.start = start

    self.duration = duration
    self.departure = departure
    self.destination = destination
  def build_easyjet(self) -> str:
    return "https://www.easyjet.com/holidays/_api/v1.0/search/packages?startDate=2024-06-05&flexibleDays=0&duration[0]=7&departure=LGW&geography=GR,GRZA&automaticAllocation=true&room[0].adults=2&room[0].children=0&room[0].infants=0&=&=&take=10&page=1&searchType=normal&distressedFlightsOnly=false&placementId=hotels_list"
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
    return self.start + self.destination + self.duration + self.departure
    




