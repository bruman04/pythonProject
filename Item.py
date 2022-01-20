import itertools
from time import time_ns
class Item:


  def __init__(self, image, name, description, rate, on_loan, available, location):

      self.__id = time_ns()
      self.__image = image
      self.__name = name
      self.__description = description
      self.__rate = rate
      self.__on_loan = on_loan
      self.__available = available
      self.__location = location


  def get_image(self):
    return self.__image

  def get_id(self):
    return self.__id

  def get_name(self):
    return self.__name

  def get_description(self):
    return self.__description

  def get_rate(self):
    return self.__rate

  def get_on_loan(self):
    return self.__on_loan

  def get_available(self):
    return self.__available

  def get_location(self):
    return self.__location




  def set_image(self, image):
    self.__image = image

  def set_id(self, id):
    self.__id= id

  def set_name(self, name):
    self.__name = name

  def set_description(self, description):
    self.__description = description

  def set_rate(self, rate):
    self.__rate = rate

  def set_on_loan(self, on_loan):
    self.__on_loan = on_loan

  def set_available(self, available):
    self.__available= available

  def set_location(self, location):
    self.__location = location
