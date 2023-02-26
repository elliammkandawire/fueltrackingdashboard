import flask
import folium
import geocoder
import pandas as pd
from flask import request
import requests
from flask_restful import Resource, Api
import datetime

app = flask.Flask(__name__)
app.config["DEBUG"] = True
api = Api(app)
port = 5100


@app.route('/', methods=['GET'])
def home():
    createMap();
    return "<h1>Map Created Successfully</p>"

def createMap():
    # myloc = geocoder.ip('me')
    location = "C:\\Users\\ITGuest\\Documents\\Personal\\sangwani\\fueltrack\\stations.csv"
    filling_stations = pd.read_csv(location)

    #filling_stations = filling_stations[["Latitude", "Longitude", "Name"]]
    # latitude, longitude
    # m = folium.Map(location=(myloc.latlng[0],myloc.latlng[1]),zoom_start=14,tiles="cartodb positron")
    # map = folium.Map(location=(myloc.latlng[0],myloc.latlng[1]), zoom_start=14, control_scale=True)
    map = folium.Map(location=[filling_stations.latitude.mean(), filling_stations.longitude.mean()], zoom_start=13, control_scale=True)
    for index, filling_station_info in filling_stations.iterrows():
        cr_date = filling_station_info['nextDelivery']
        cr_date = datetime.datetime.strptime(cr_date, "%Y-%m-%dT%H:%M:%S.%fZ")
        cr_date = cr_date.strftime("%d/%m/%Y")
        petrol='No'
        diesel='No'
        if(filling_station_info['petrol']):
            petrol='Yes'
        if(filling_station_info['diesel']):
            diesel='Yes'
        html="<h4> {}</h3><ul> <li>Petrol - {}</li><li>Diesel - {}</li><li>Delivery - {}</li></ul></p>".format(filling_station_info['name'],petrol,diesel,cr_date)
        # html="
        #     <h4> {}</h3>
        #     <ul>
        #         <li>Petrol - {petrol}</li>
        #         <li>Diesel - {diesel}</li>
        #         <li>Delivery - {cr_date}</li>
        #     </ul>
        #     </p>".format(filling_station_info['name'])
            
        iframe = folium.IFrame(html=html, width=220, height=170)
        popup = folium.Popup(iframe, max_width=2650)
        color='orange'
        if filling_station_info['petrol']==1 and filling_station_info['diesel']==1:
          color='green';
        elif filling_station_info['petrol']==0 and filling_station_info['diesel']==0:
          color='red';
        folium.Marker([filling_station_info["latitude"], filling_station_info["longitude"]], popup=popup,icon=folium.Icon(color=color)).add_to(map)
    map.save("index.html")

if __name__ == "__main__":
    app.run()