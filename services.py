import requests
import json

# Creating an object 'Location' for identifying the given location uniquely

class Location(object):
    
    # Constructor for location object
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon
        self._data = None

    # Method for pulling irradiance data from ISRO Vedas
    def irradiance_data(self):
        if self._data is None:
            url = f'https://vedas.sac.gov.in/powerGisService/insol_temp_calc/{self.lon}/{self.lat}/kwh'
            headers = {
            'Accept' : '*/*'
            }
            response = requests.get(url=url, headers=headers)
            self._data = response.json()
        return self._data
    
    # Method for parsing the json irradiance data
    def irradiance_parsing(self):
        years = self.irradiance_data()['insol_year_lst']
        yearwise_irradiation = []
        for year in years:
            yearwise_irradiation.append(int(self.irradiance_data()['insol_years_data'][f'{year}_sum']))
        return yearwise_irradiation
    
    # Method for parsing the json irradiance data in dict format
    def irradiance_parsing_dict(self):
        data = self.irradiance_data()
        years = data['insol_year_lst']
        yearwise_irradiation = {}
        for year in years:
            yearwise_irradiation[year] = int(data['insol_years_data'][f'{year}_sum'])
        return yearwise_irradiation

    
    # Method for getting the max irradiance and associated year
    def max_irradiance_and_year(self):
        data = self.irradiance_parsing_dict()
        max_year = max(data, key=data.get)
        max_irradiation = max(data.values())
        return max_year,max_irradiation
    
    # Method of getting the min irradiance and associated year
    def min_irradiance_and_year(self):
        data = self.irradiance_parsing_dict()
        min_year = min(data,key=data.get)
        min_irradiation = min(data.values())
        return min_year, min_irradiation
    
    # Method of getting average irradiance
    def avg_irradiance (self):
        data = self.irradiance_parsing_dict()
        avg_irrad = int(sum(data.values())/len(data.values()))
        return avg_irrad
    
class Site_details :
    def __init__ (self, location_obj, pr):
        self.pr = pr
        # self.est_gen = est_gen
        self.location = location_obj

    def max_generation(self):
        max_irrad = self.location.max_irradiance_and_year()[1]
        max_gen = self.pr * max_irrad
        return max_gen

    def min_generation(self):
        min_irrad = self.location.min_irradiance_and_year()[1]
        min_gen = min_irrad*self.pr
        return min_gen

    def avg_generation(self):
        avg_irrad = self.location.avg_irradiance()
        avg_gen = avg_irrad * self.pr
        return avg_gen
    
# Created creamline Object

project_location = Location(15.91,79.74)

max_year, max_irradiation = project_location.max_irradiance_and_year()
min_year, min_irrad  = project_location.min_irradiance_and_year()
avg_irrad = project_location.avg_irradiance()

# print(f'Max irradiance of {max_irradiation} occured in year {max_year} \n')
# print(f'Min irradiance of {min_irrad} occured in year {min_year} \n')
# print(f'Average irradiance is {avg_irrad}')

site_details = Site_details(project_location, 0.81, 1350)

max_gen = site_details.max_generation()
min_gen = site_details.min_generation()
avg_gen = site_details.avg_generation()



