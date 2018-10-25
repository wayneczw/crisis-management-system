# coding: utf-8
__all__ = ['periodic_psi_check']
from datetime import datetime
from flask import Flask, render_template, Blueprint
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map, icons
from .map_api import get_psi, get_dengue_clusters, get_weather, get_shelter, address_to_latlng
from SocialMedia.model import CrisisReport, Address, GeoCoordinate
from SocialMedia.controller import SocialMedia
import time, threading
from CallCenter.CallCenter_Model import retrieve_active_incident_reports


map_api = Blueprint('map', __name__, template_folder='templates', )

COLOR_CODE = dict(green='#228B22', blue='#4169e1', yellow='#ffcc00', orange='#FF4500', red='#B22222')

PSI_ICONS = {'E': "//maps.google.com/mapfiles/kml/paddle/E.png",
            'W': "//maps.google.com/mapfiles/kml/paddle/W.png",
            'S': "//maps.google.com/mapfiles/kml/paddle/S.png",
            'N': "//maps.google.com/mapfiles/kml/paddle/N.png",
            'C': "//maps.google.com/mapfiles/kml/paddle/C.png"
            }
WEATHER_ICONS = {"Partly Cloudy": "https://addons-media.operacdn.com/media/extensions/52/228552/0.1.0-rev1/icons/icon_64x64_944d829ba23973bd494ff4458c6536c0.png",
            "Partly Cloudy (Day)": "https://addons-media.operacdn.com/media/extensions/52/228552/0.1.0-rev1/icons/icon_64x64_944d829ba23973bd494ff4458c6536c0.png",
            "Partly Cloudy (Night)": "https://addons-media.operacdn.com/media/extensions/52/228552/0.1.0-rev1/icons/icon_64x64_944d829ba23973bd494ff4458c6536c0.png",
            "Cloudy": "https://addons-media.operacdn.com/media/extensions/52/228552/0.1.0-rev1/icons/icon_64x64_944d829ba23973bd494ff4458c6536c0.png",
            "Cloudy (Day)": "https://addons-media.operacdn.com/media/extensions/52/228552/0.1.0-rev1/icons/icon_64x64_944d829ba23973bd494ff4458c6536c0.png",
            "Cloudy (Night)": "https://addons-media.operacdn.com/media/extensions/52/228552/0.1.0-rev1/icons/icon_64x64_944d829ba23973bd494ff4458c6536c0.png",
            "Fair (Day)": "https://images.sftcdn.net/images/t_app-logo-l,f_auto,dpr_auto/p/6342e25c-9b2e-11e6-8327-00163ed833e7/297691412/heliospaint-logo.png",
            "Fair (Night)": "https://addons-media.operacdn.com/media/extensions/59/228359/0.2.8-rev1/icons/icon_64x64_0681774836f9505465805085bb518811.png",
            "Fair and Warm": "https://images.sftcdn.net/images/t_app-logo-l,f_auto,dpr_auto/p/6342e25c-9b2e-11e6-8327-00163ed833e7/297691412/heliospaint-logo.png",
            "Light Rain": "http://maps.google.com/mapfiles/kml/shapes/rainy.png",
            "Moderate Rain": "http://maps.google.com/mapfiles/kml/shapes/rainy.png",
            "Heavy Rain": "http://maps.google.com/mapfiles/kml/shapes/rainy.png",
            "Passing Showers": "http://maps.google.com/mapfiles/kml/shapes/rainy.png",
            "Light Showers": "http://maps.google.com/mapfiles/kml/shapes/rainy.png",
            "Showers": "http://maps.google.com/mapfiles/kml/shapes/rainy.png",
            "Heavy Showers": "https://addons.cdn.mozilla.net/user-media/addon_icons/0/398-64.png?modified=1441890566",
            "Thundery Showers": "http://maps.google.com/mapfiles/kml/shapes/thunderstorm.png",
            "Heavy Thundery Showers": "http://maps.google.com/mapfiles/kml/shapes/thunderstorm.png",
            "Heavy Thundery Showers with Gusty Winds": "http://maps.google.com/mapfiles/kml/shapes/thunderstorm.png"
            }
SHELTER_ICON = 'http://maps.google.com/mapfiles/kml/pal2/icon10.png'

REGION_COORD = dict(west={"lat": 1.35735, "lng": 103.7},
                    east={"lat": 1.35735, "lng": 103.94},
                    central={"lat": 1.35735, "lng": 103.82},
                    south={"lat": 1.29587, "lng": 103.82},
                    north={"lat": 1.41803, "lng": 103.82})

@map_api.route("/psi")
def psimapview():
    east_info, west_info, south_info, north_info, central_info = get_psi()

    psimap = Map(
        identifier="psimap",
        lat=1.3521,
        lng=103.8198,
        zoom=12,
        region='SG',
        style="height:800px;width:1200px;margin:0;",
        markers=[
            {   
                'icon': PSI_ICONS['E'],
                'lat':  east_info['lat'],
                'lng':  east_info['lng'],
                'infobox': "<b style='color:{};'> <h3>North PSI:</h3> <h4>{} {}</h4></b>".format(COLOR_CODE[east_info['color']], east_info['status'], east_info['psi'])
            },
            {
                'icon': PSI_ICONS['W'],
                'lat':  west_info['lat'],
                'lng':  west_info['lng'],
                'infobox': "<b style='color:{};'> <h3>West PSI:</h3> <h4>{} {}</h4></b>".format(COLOR_CODE[west_info['color']], west_info['status'], west_info['psi'])
            },
            {
                'icon': PSI_ICONS['S'],
                'lat':  south_info['lat'],
                'lng':  south_info['lng'],
                'infobox': "<b style='color:{};'> <h3>South PSI:</h3> <h4>{} {}</h4></b>".format(COLOR_CODE[south_info['color']], south_info['status'], south_info['psi'])
            },
            {
                'icon': PSI_ICONS['N'],
                'lat':  north_info['lat'],
                'lng':  north_info['lng'],
                'infobox': "<b style='color:{};'> <h3>North PSI:</h3> <h4>{} {}</h4></b>".format(COLOR_CODE[north_info['color']], north_info['status'], north_info['psi'])
            },
            {
                'icon': PSI_ICONS['C'],
                'lat':  central_info['lat'],
                'lng':  central_info['lng'],
                'infobox': "<b style='color:{};'> <h3>Central PSI:</h3> <h4>{} {}</h4></b>".format(COLOR_CODE[central_info['color']], central_info['status'], central_info['psi'])
            }
        ]
    )
    return render_template('psimap.html', psimap=psimap)


@map_api.route("/weather")
def weathermapview():
    weather_dict = get_weather()

    #create markers
    markers_list = list()
    for area, info_dict in weather_dict.items():
        tmp_dict = dict(icon=WEATHER_ICONS[info_dict['forecast']],
                        lat=info_dict['lat'],
                        lng=info_dict['lng'],
                        infobox="<h3>{}</h3> <h4>Forecast: {}</h4>".format(area, info_dict['forecast']))
        markers_list.append(tmp_dict)

    weathermap = Map(
        identifier="weathermap",
        lat=1.3521,
        lng=103.8198,
        zoom=12,
        region='SG',
        style="height:800px;width:1200px;margin:0;",
        markers=markers_list
    )

    return render_template('weathermap.html', weathermap=weathermap)


@map_api.route("/shelters")
def sheltermapview():
    shelters_dict = get_shelter()

    #create markers
    markers_list = list()
    for area, info_dict in shelters_dict.items():
        
        tmp_dict = dict(icon=SHELTER_ICON,
                        lat=info_dict['lat'],
                        lng=info_dict['lng'],
                        infobox="<h3> {}</h3> <h4>Address: {}</h4> <h4>Description: {}</h4>".format(area, info_dict['address'], info_dict['description']))
        markers_list.append(tmp_dict)

    sheltersmap = Map(
        identifier="sheltersmap",
        lat=1.3521,
        lng=103.8198,
        zoom=12,
        region='SG',
        style="height:800px;width:1200px;margin:0;",
        markers=markers_list
    )

    return render_template('sheltersmap.html', sheltersmap=sheltersmap)

@map_api.route("/dengue")
def denguemapview():

    dengue_clusters = get_dengue_clusters()

    markers_list = []
    for cluster in dengue_clusters:
        latlng = address_to_latlng(cluster['locality'])
        if cluster['num_all'] >= 10:
            icon = icons.dots.red
        else:
            icon = icons.dots.orange
        tmp_dict = dict(
            icon=icon,
            lat=latlng['lat'],
            lng=latlng['lng'],
            infobox="<h3> {}</h3> <h4>Cases with onset in last 2 weeks: {}</h4> <h4>Cases since start of cluster: {}</h4> ".format(cluster['cluster'], cluster['num_last2weeks'], cluster['num_all']))
        markers_list.append(tmp_dict)

    denguemap = Map(
        identifier="denguemap",
        lat=1.3521,
        lng=103.8198,
        zoom=12,
        region='SG',
        style="height:800px;width:1200px;margin:0;",
        markers=markers_list
    )
    return render_template('denguemap.html', denguemap=denguemap)

@map_api.route("/incidents")
def incidentsmapview():

    incidents_list = retrieve_active_incident_reports()
    print("Incidents:")
    print (incidents_list)
    # create markers
    markers_list = list()
    for incident in incidents_list:
        info_string = "<h6>ID: {}</h6> <h6>Report Date: {}</h6> <h6>Reporter: {}</h6>" + "<h6>Reporter's HP: {}</h6> <h6>Location: {}</h6> <h6>Type of Assistance Need: {}</h6>" + "<h6>Description: {}</h6> <h6>Priority for Severity of Injuries: {}</h6> " + "<h6>Priority for Impending Dangers: {}</h6> <h6>Priority for Presence of Nearby Help: {}</h6> <h6>Status: {}</h6>"
        if incident[10]=="REPORTED":
            icon = "http://maps.google.com/mapfiles/kml/pal3/icon59.png"
        else:
            icon = "http://maps.google.com/mapfiles/kml/pal3/icon37.png"
        tmp_dict = dict(icon=icon,
                        lat=incident[12],
                        lng=incident[13],
                        infobox=info_string.format(incident[0],incident[1],incident[2],incident[3],incident[4],incident[5],incident[6],incident[7],incident[8],incident[9], incident[10]))
        markers_list.append(tmp_dict)

    incidentsmap = Map(
        identifier="incidentsmap",
        lat=1.3521,
        lng=103.8198,
        zoom=12,
        region='SG',
        style="height:800px;width:1200px;margin:0;",
        markers=markers_list
    )

    return render_template('incidentsmap.html', incidentsmap=incidentsmap)

def periodic_psi_check():
    def _check_threshold(psi):
        if psi > 200:
            return True
        return False
    def _alert(info_dict, area):
        date = str(datetime.now().date())
        time = str(datetime.time(datetime.now()))
        coord = GeoCoordinate(latitude=REGION_COORD[area]['lat'], longitude=REGION_COORD[area]['lng'])
        address = Address(street_name=None, unit_number=None, postal_code=None, coordinates=coord)

        report = CrisisReport(identifier=1, name=area, address=address, category='Haze', description=info_dict['status'], date=date, time=time, advisory='Avoid out door activity')
        social_media = SocialMedia()

        social_media.alert_public(report)
        social_media.post_facebook(report)
 
    east_info, west_info, south_info, north_info, central_info = get_psi()

    if _check_threshold(east_info['psi']): _alert(east_info, 'east')
    if _check_threshold(west_info['psi']): _alert(west_info, 'west')
    if _check_threshold(south_info['psi']): _alert(south_info, 'south')
    if _check_threshold(north_info['psi']): _alert(north_info, 'north')
    if _check_threshold(central_info['psi']): _alert(central_info, 'central')

    threading.Timer(600, periodic_psi_check).start()


# if __name__ == "__main__":
#     app.run(debug=True, use_reloader=True)
