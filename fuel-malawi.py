import folium
import geocoder
import pandas as pd

myloc = geocoder.ip('me')
location = "filling-stations.csv"
filling_stations = pd.read_csv(location)

#filling_stations = filling_stations[["Latitude", "Longitude", "Name"]]
# latitude, longitude
# m = folium.Map(location=(myloc.latlng[0],myloc.latlng[1]),zoom_start=14,tiles="cartodb positron")
map = folium.Map(location=(myloc.latlng[0],myloc.latlng[1]), zoom_start=14, control_scale=True)
for index, filling_station_info in filling_stations.iterrows():
    html=f"""
        <h3> {filling_station_info['Name']}</h3>
        <ul>
            <li>Petrol - {filling_station_info['Petrol']}</li>
            <li>Diesel - {filling_station_info['Diesel']}</li>
        </ul>
        </p>
        """
    iframe = folium.IFrame(html=html, width=200, height=150)
    popup = folium.Popup(iframe, max_width=2650)
    folium.Marker([filling_station_info["Latitude"], filling_station_info["Longitude"]], popup=popup).add_to(map)
map.save("index.html")