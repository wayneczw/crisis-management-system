# coding: utf-8

from flask import Flask, render_template, Blueprint
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map, icons
from .map_api import get_psi, get_dengue_clusters, get_weather, get_shelter, address_to_latlng

map_api = Blueprint('map', __name__, template_folder='templates', )

COLOR_CODE = dict(green='#228B22', blue='#4169e1', yellow='#ffcc00', orange='#FF4500', red='#B22222')

PSI_ICONS = {'E': "//maps.google.com/mapfiles/kml/paddle/E.png",
            'W': "//maps.google.com/mapfiles/kml/paddle/W.png",
            'S': "//maps.google.com/mapfiles/kml/paddle/S.png",
            'N': "//maps.google.com/mapfiles/kml/paddle/N.png",
            'C': "//maps.google.com/mapfiles/kml/paddle/C.png"
            }
WEATHER_ICONS = {"Partly Cloudy": "https://addons-media.operacdn.com/media/extensions/52/228552/0.1.0-rev1/icons/icon_64x64_944d829ba23973bd494ff4458c6536c0.png",
            "Cloudy": "https://addons-media.operacdn.com/media/extensions/52/228552/0.1.0-rev1/icons/icon_64x64_944d829ba23973bd494ff4458c6536c0.png",
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
#end def


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
#end def

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
    #end for

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
#end def

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
    #end for

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
#end def

@map_api.route("/incidents")
def incidentsmapview(incidents_list):


    # create markers
    markers_list = list()
    for incident in incidents_list.items():
        tmp_dict = dict(icon='http://maps.google.com/mapfiles/kml/pal2/icon10.png',
                        lat=incident['lat'],
                        lng=incident['lng'],
                        infobox="<h4>Name: {}</h4> <h4>Report Date: {}</h4> <h4>Address: {}</h4> <h4>Description: {}</h4> <h4>Level: {}</h4> <h4>Assignee: {}</h4>".format(incident['name'],
                                                                                                                                                                           incident['report_date'],
                                                                                                                                                                           incident['address'],
                                                                                                                                                                           incident['description'],
                                                                                                                                                                           incident['level'],
                                                                                                                                                                           incident['assignee']
                                                                                                                                                                           ))
        markers_list.append(tmp_dict)
    # end for

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
#end def


# if __name__ == "__main__":
#     app.run(debug=True, use_reloader=True)
