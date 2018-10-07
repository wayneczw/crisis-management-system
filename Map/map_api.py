__all__ = ['get_psi', 'get_dengue_clusters', 'get_weather', 'get_shelter', 'address_to_latlng']

import json
import requests
import urllib.request
from urllib.request import Request, urlopen
import bs4


API_KEY = "AIzaSyDc1Hx9zrh10qY4FSl-A0OwIVKRNTBkZGs"

PSI_URL = 'https://api.data.gov.sg/v1/environment/psi'
DENGUE_URL = 'https://www.nea.gov.sg/dengue-zika/dengue/dengue-clusters'
WEATHER_URL = 'https://api.data.gov.sg/v1/environment/2-hour-weather-forecast'
SHELTER_URL = 'https://data.gov.sg/api/action/datastore_search?resource_id=4ee17930-4780-403b-b6d4-b963c7bb1c09'

REGION_LAT_LNG = dict(east=dict(lat=1.3413, lng=103.9638),
                west=dict(lat=1.3483, lng=103.6831),
                south=dict(lat=1.2957, lng=103.8065),
                north=dict(lat=1.4382, lng=103.7890),
                central=dict(lat=1.36, lng=103.8))

def get_psi():
    def _get_psi_info(region, psi_json_dict_list):
        return dict(lat=REGION_LAT_LNG[region], lng=REGION_LAT_LNG[region], psi=psi_json_dict_list[0]['items'][0]['readings']['pm25_twenty_four_hourly'][region])
    #end def

    def _check_status(info_dict):
        if info_dict['psi'] <= 50: return ('Healthy', 'green')
        elif info_dict['psi'] <= 100: return ('Moderate', 'blue')
        elif info_dict['psi'] <= 200: return ('Unhealthy', 'yellow')
        elif info_dict['psi'] <= 300: return ('Very Unhealthy', 'orange')
        else: return ('Hazardous', 'red')
    #end def

    '''
    :return: 4 dictionaries of the same formats
        {'status': 'Healthy',
        'psi': 30,
        'color': 'green',
        'lat': 130.21,
        'lng': 128.12
        }
    '''

    psi_response = urllib.request.urlopen(PSI_URL, timeout=5)
    psi = [line.decode('utf-8') for line in psi_response]
    psi_json_dict_list = [json.loads(js) for js in psi]

    east_info = _get_psi_info('east', psi_json_dict_list)
    west_info = _get_psi_info('west', psi_json_dict_list)
    south_info = _get_psi_info('south', psi_json_dict_list)
    north_info = _get_psi_info('north', psi_json_dict_list)
    central_info = _get_psi_info('central', psi_json_dict_list)

    east_info['status'], east_info['color'] = _check_status(east_info)
    west_info['status'], west_info['color'] = _check_status(west_info)
    south_info['status'], south_info['color'] = _check_status(south_info)
    north_info['status'], north_info['color'] = _check_status(north_info)
    central_info['status'], central_info['color'] = _check_status(central_info)

    return east_info, west_info, south_info, north_info, central_info
#end def

def get_dengue_clusters():
    '''
    :return: a list of dictionaries
        [{'locality': 'sldfjla',
        'cluster': 'jdsfaf',
        'num_last2weeks: 10,
        'num_all': 100},
                        ...
        ]
    '''

    results = []
    r = requests.get(DENGUE_URL)
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    for l in soup.findAll('td', attrs={'data-type':'locality'}):
        cluster = l.find('a')
        cases_last2weeks = l.find_next('td')
        cases_sincestart = l.find_next('td').find_next('td')
        locality = l.find_next('td').find_next('td').find_next('td')
        results.append({'locality': locality.text, 'cluster': cluster.text, 'num_last2weeks':int(cases_last2weeks.text), 'num_all':int(cases_sincestart.text)})
    #end for

    return results
#end def


def get_weather():
    '''
    :return: a dictionary of dictionaries
        {'Ang Mo Kio': {'forecast': 'sldfjla',
                        'label_location': {'latitude': '130.3', 'longitude': '130.2'}},
                        ...
        }
    '''
    weather_response = urllib.request.urlopen(WEATHER_URL, timeout=5)
    weather = [line.decode('utf-8') for line in weather_response]
    weather_json_dict_list = [json.loads(js) for js in weather]

    weather_dict = {item['name']: dict(lat=item['label_location']['latitude'], lng=item['label_location']['longitude']) for item in weather_json_dict_list[0]['area_metadata']} 

    for item in weather_json_dict_list[0]['items'][0]['forecasts']:
        weather_dict[item['area']]['forecast'] = item['forecast']
    #end for

    return weather_dict
#end def


def get_shelter():
    '''
    :return: a dictionary of dictionaries
        {'Pioneer MRT': {'address': 'sldfjla',
                        'postal_code': '123981',
                        'description': 'jfsao'},
                        ...
        }
    '''

    shelters_response = Request(SHELTER_URL, headers={'User-Agent': 'Mozilla/5.0'})
    shelters_response = urlopen(shelters_response).read().decode('utf-8')
    shelters_dict_list = json.loads(shelters_response)['result']['records']

    shelters_dict = dict()
    for item in shelters_dict_list:
        tmp_dict = dict(address=item['address'],
            postal_code=item['postal_code'],
            description=item['description'])
        tmp_dict.update(address_to_latlng(item['address']))

        shelters_dict[item['name']] = tmp_dict
    #end for

    return shelters_dict
#end def


def address_to_latlng(address):
    geo_api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'.format(address.replace(" ", "+"), API_KEY))
    geo_api_response_dict = geo_api_response.json()
    if geo_api_response_dict['status'] == 'OK':
        lat = geo_api_response_dict['results'][0]['geometry']['location']['lat']
        lng = geo_api_response_dict['results'][0]['geometry']['location']['lng']
    else:
        lat = 0
        lng = 0
    #end if

    return dict(lat=lat, lng=lng)
#end def
