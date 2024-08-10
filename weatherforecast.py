import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

def get_wetaher_forecast(date, latitude, longitude):

	url = "https://api.open-meteo.com/v1/forecast"
	params = {
		"latitude": latitude,
		"longitude": longitude,
		"minutely_15": ["sunshine_duration","temperature_2m", "relative_humidity_2m", "shortwave_radiation", "diffuse_radiation", "direct_normal_irradiance"],
		"start_date": date,
		"end_date": date
	}
	responses = openmeteo.weather_api(url, params=params)

	# Process first location. Add a for-loop for multiple locations or weather models
	response = responses[0]
	print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
	print(f"Elevation {response.Elevation()} m asl")
	print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
	print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

	# Process minutely_15 data. The order of variables needs to be the same as requested.
	minutely_15 = response.Minutely15()
	minutely_15_sunshine_duration = minutely_15.Variables(0).ValuesAsNumpy()
	minutely_15_temperature_2m = minutely_15.Variables(1).ValuesAsNumpy()
	minutely_15_relative_humidity_2m = minutely_15.Variables(2).ValuesAsNumpy()
	minutely_15_shortwave_radiation = minutely_15.Variables(3).ValuesAsNumpy()
	minutely_15_diffuse_radiation = minutely_15.Variables(4).ValuesAsNumpy()
	minutely_15_direct_normal_irradiance = minutely_15.Variables(5).ValuesAsNumpy()

	minutely_15_data = {"date": pd.date_range(
		start = pd.to_datetime(minutely_15.Time(), unit = "s", utc = True),
		end = pd.to_datetime(minutely_15.TimeEnd(), unit = "s", utc = True),
		freq = pd.Timedelta(seconds = minutely_15.Interval()),
		inclusive = "left"
	)}
	minutely_15_data["sunshine_duration"] = minutely_15_sunshine_duration
	minutely_15_data["temperature_2m"] = minutely_15_temperature_2m
	minutely_15_data["relative_humidity_2m"] = minutely_15_relative_humidity_2m
	minutely_15_data["shortwave_radiation"] = minutely_15_shortwave_radiation
	minutely_15_data["diffuse_radiation"] = minutely_15_diffuse_radiation
	minutely_15_data["direct_normal_irradiance"] = minutely_15_direct_normal_irradiance


	minutely_15_dataframe = pd.DataFrame(data = minutely_15_data)
	#print(minutely_15_dataframe)
	sun_list = []
	temp_list=[]
	hum_list=[]
	ghi_list = []
	dhi_list=[]
	dni_list=[]
	total_seconds = 0.0
	for index, row in minutely_15_dataframe.iterrows():
		if(row['date'].minute == 0):
			sun_list.append(round(total_seconds/60, 1))
			temp_list.append(round(float(row['temperature_2m']), 1))
			hum_list.append(round(float(row['relative_humidity_2m']), 1))
			ghi_list.append(round(float(row['shortwave_radiation']), 1))
			dhi_list.append(round(float(row['diffuse_radiation']), 1))
			dni_list.append(round(float(row['direct_normal_irradiance']), 1))
			total_seconds = 0.0
		else:
			total_seconds = total_seconds + float(row['sunshine_duration'])
        


	return sun_list, temp_list, hum_list, ghi_list, dhi_list, dni_list

get_wetaher_forecast("2024-08-05", "52.52", "13.405")
