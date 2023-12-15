from datetime import date, timedelta
import datetime

import requests

class Query:
  def __init__(self, start:date=None, duration:int=7, ) -> None:
    if not start: start = datetime.datetime.now() + timedelta(1)


  def query(self):
    """
    Sends query to providers and collects responses
    """

    # Currently only for easyjet as it is designed.

    requests.get()



