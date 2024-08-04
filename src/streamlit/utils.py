# Add your utilities or helper functions to this file.

from dotenv import load_dotenv, find_dotenv
from pydantic import BaseModel
import time
import os

class PropertyDetails(BaseModel):
    location: str
    no_beds: int
    no_baths: int
    budget_high: int
    budget_low: int
    pets: str
    public_transit: bool
    move_in_date: str
    car_parking: bool
    other_ameneties: str
    # Will be filled with information relevant to making a decision but not explicitly mentioned by user
    extra_considerations: str    

class SearchResults(BaseModel):
    property_title: str
    property_address: str
    contact_information: int
    monthly_rent: int
    no_beds: int
    no_baths: int
    avail_move_in_date: str
    pet_considerations: str
    public_transit_options: str
    car_parking_options: str
    provided_ameneties: str
    extra_considerations: str 

# these expect to find a .env file at the directory above (../)                                                                                                                  # the format for that file is (without the comment)                                                                                                                                       #API_KEYNAME=AStringThatIsTheLongAPIKeyFromSomeService
def load_env():
    _ = load_dotenv(find_dotenv())

def get_api_key(service):
    load_env()
    api_key = os.getenv(service)
    return api_key


# break line every 80 characters if line is longer than 80 characters
# don't break in the middle of a word
def pretty_print_result(result):
  parsed_result = []
  for line in result.split('\n'):
      if len(line) > 80:
          words = line.split(' ')
          new_line = ''
          for word in words:
              if len(new_line) + len(word) + 1 > 80:
                  parsed_result.append(new_line)
                  new_line = word
              else:
                  if new_line == '':
                      new_line = word
                  else:
                      new_line += ' ' + word
          parsed_result.append(new_line)
      else:
          parsed_result.append(line)
  return "\n".join(parsed_result)

def stream_data(input):
    for word in input.split(" "):
        yield word + " "
        time.sleep(0.02)