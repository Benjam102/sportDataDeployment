import requests
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
import re

def get_coordinates(address):
    url = f"https://nominatim.openstreetmap.org/search?q={address}&format=json"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200 and data:
        latitude = data[0]['lat']
        longitude = data[0]['lon']
        return float(latitude), float(longitude)
    else:
        # print("Impossible d'obtenir les coordonnées.")
        return None

def get_weather(adress, date, hour):
    coordinates = get_coordinates(adress)
    if coordinates:
        if date < str(pd.Timestamp.now().date()):
            url = "https://archive-api.open-meteo.com/v1/archive"
        else:
            url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": coordinates[0],
            "longitude": coordinates[1],
            "start_date": date,
            "end_date": date,
            "hourly": ["temperature_2m", "relative_humidity_2m", "surface_pressure", "precipitation", "wind_speed_10m","weather_code"]
        }

        cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        openmeteo = openmeteo_requests.Client(session=retry_session)

        responses = openmeteo.weather_api(url, params=params)

        response = responses[0]
        hourly = response.Hourly()
        hourly_data = {"date": pd.to_datetime(hourly.Time(), unit="s", utc=True).date}

        start_hour = pd.Timestamp(f"{date} 00:00:00", tz="UTC")
        end_hour = pd.Timestamp(f"{date} 23:00:00", tz="UTC")
        hour_range = pd.date_range(start=start_hour, end=end_hour, freq="h")
        hourly_data["hour"] = pd.to_datetime(hour_range).strftime('%H:%M:%S')


        for i in range(len(params["hourly"])):
            variable_name = params["hourly"][i]
            variable_data = hourly.Variables(i).ValuesAsNumpy()
            hourly_data[variable_name] = variable_data
        hourly_dataframe = pd.DataFrame(data=hourly_data)
        #hourly_dataframe.set_index(["hour"], inplace=True)

        hourly_dataframe.drop(columns=["date"], inplace=True)
        #hourly_dataframe.to_csv("weather_data.csv")
        hourly_dataframe.drop(columns=["hour"], inplace=True)
        i = hour  # Indice des valeurs à isoler (par exemple)
        isolated_hourly_data = {}
        for variable_name, variable_values in hourly_dataframe.items():
            #isolated_hourly_data[variable_name] = variable_values[i:i+3].mean()
            isolated_hourly_data[variable_name] = variable_values[i]
        return isolated_hourly_data
    else:
        return None


chemin_img = ["/static/IMG/meteo/soleil_0.png",
              "/static/IMG/meteo/nusoleil_1_2_3.png",
              "/static/IMG/meteo/brouillard_45_48.png",
              "/static/IMG/meteo/bruine_51_53_55.png",
              "/static/IMG/meteo/pluie_56_57_61_63_65_66_67.png",
              "/static/IMG/meteo/neigeux_71_73_75.png",
              "/static/IMG/meteo/neigeux_77.png",
              "/static/IMG/meteo/pluvieux_80_81_82.png",
              "/static/IMG/meteo/neigeux_85_86.png",
              "/static/IMG/meteo/orage_95.png",
              "/static/IMG/meteo/orage_96_99.png"
              ]


def associate_weather_code(code) :
    if code != None :
        for index, c in enumerate(chemin_img) :
            # Utiliser une expression régulière pour extraire tous les nombres du chemin sous forme d'un tableau
            nombres = re.findall(r'\d+', c)
            
            if str(int(code)) in nombres :
                return chemin_img[index]

    return None
        
       
