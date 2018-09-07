# coding: utf-8

from flask import Flask, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map, icons
import urllib.request
import json

app = Flask(__name__, template_folder="templates")

app.config['GOOGLEMAPS_KEY'] = "AIzaSyAYnlWxEoOaBVFkv6VijmIEZ1pumZfhFoA"
GoogleMaps(app, key="AIzaSyAYnlWxEoOaBVFkv6VijmIEZ1pumZfhFoA")


REGION_LAT_LNG = dict(east=dict(lat=1.3413, lng=103.9638),
                west=dict(lat=1.3483, lng=103.6831),
                south=dict(lat=1.2957, lng=103.8065),
                north=dict(lat=1.4382, lng=103.7890))

COLOR_CODE = dict(green='#228B22', blue='#4169e1', yellow='#ffcc00', orange='#FF4500', red='#B22222')

@app.route("/")
def mapview():
    def _get_psi_info(region, psi_json_dict_list):
        return dict(lat=REGION_LAT_LNG[region], lng=REGION_LAT_LNG[region], psi=psi_json_dict_list[0]['items'][0]['readings']['pm25_twenty_four_hourly'][region])
    #end def

    def _check_status(info_dict):
        if info_dict['psi'] <= 50 & info_dict['psi'] >=0: return ('Healthy', 'green')
        elif info_dict['psi'] <= 100: return ('Moderate', 'blue')
        elif info_dict['psi'] <= 200: return ('Unhealthy', 'yellow')
        elif info_dict['psi'] <= 300: return ('Very Unhealthy', 'orange')
        else: return ('Hazardous', 'red')
    #end def

    psi_response = urllib.request.urlopen('https://api.data.gov.sg/v1/environment/psi', timeout=5)
    psi = [line.decode('utf-8') for line in psi_response]
    psi_json_dict_list = [json.loads(js) for js in psi]

    east_info = _get_psi_info('east', psi_json_dict_list)
    west_info = _get_psi_info('west', psi_json_dict_list)
    south_info = _get_psi_info('south', psi_json_dict_list)
    north_info = _get_psi_info('north', psi_json_dict_list)

    east_info['status'], east_info['color'] = _check_status(east_info)
    west_info['status'], west_info['color'] = _check_status(west_info)
    south_info['status'], south_info['color'] = _check_status(south_info)
    north_info['status'], north_info['color'] = _check_status(north_info)

    psimap = Map(
        identifier="psimap",
        lat=1.3521,
        lng=103.8198,
        zoom=12,
        region='SG',
        style="height:800px;width:1200px;margin:0;",
        markers=[
            {
                'icon': icons.alpha.E,
                'lat':  east_info['lat'],
                'lng':  east_info['lng'],
                'infobox': "<b style='color:{};'>East PSI: \n {}\n{}</b>".format(COLOR_CODE[east_info['color']], east_info['status'], east_info['psi'])
            },
            {
                'icon': icons.alpha.W,
                'lat':  west_info['lat'],
                'lng':  west_info['lng'],
                'infobox': "<b style='color:{};'>West PSI: \n {}\n{}</b>".format(COLOR_CODE[west_info['color']], west_info['status'], west_info['psi'])
            },
            {
                'icon': icons.alpha.S,
                'lat':  south_info['lat'],
                'lng':  south_info['lng'],
                'infobox': "<b style='color:{};'>South PSI: \n {}\n{}</b>".format(COLOR_CODE[south_info['color']], south_info['status'], south_info['psi'])
            },
            {
                'icon': icons.alpha.N,
                'lat':  north_info['lat'],
                'lng':  north_info['lng'],
                'infobox': "<b style='color:{};'>North PSI: \n {}\n{}</b>".format(COLOR_CODE[north_info['color']], north_info['status'], north_info['psi'])
            }
        ]
    )
    return render_template('map.html', psimap=psimap)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
