import datetime
from typing import List

class Holiday:
  """
  `Holiday` represents the general information which is not included within provider specific URL builder functions.
  """
  def __init__(self, name: str, 
               rating: float, 
               ratings: int, 
               price: float, 
               deposit: float, 
               stay: int, 
               images: List[str], 
               date: str) -> None:
    self.name = name
    self.rating = rating
    self.ratings = ratings
    self.price = price
    self.deposit = deposit
    self.stay = stay
    self.images = images

    def to_from_str(t: str) -> datetime.datetime:
      t = t.split("T")[0]
      t = t.replace("/", "")
      t = t.replace("-", "")
      ret = datetime.datetime.strptime(t, "%Y%m%d").date() + datetime.timedelta(self.stay)
      return datetime.datetime.strftime(ret, "%d-%m-%Y")
    
    self.date = date
    self.to = to_from_str(date)


  def get_provider(self) -> str:
    t = type(self)
    return t
  
  def __str__(self) -> str:
    print(self.name, self.price)
    return str(self.name) + ": " + str(self.price)

  def to_json(self) -> dict:
    return self.__dict__
