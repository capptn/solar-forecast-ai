# Import Meteostat library and dependencies
from datetime import datetime
from meteostat import Hourly, Daily
from meteostat import Stations
from meteostat import Point

stations = Stations()
stations = stations.nearby(51.3656, 7.3834)

station = stations.fetch(1)

print(station)

# Set time period
start = datetime(2024, 7, 28)
end = datetime(2024, 7, 28, 23, 59)

# Get hourly data
data = Hourly(station, start, end)
data = data.fetch()

berlin = Point(52.5200, 13.4050)



dataD = Daily(berlin, start, end)
dataD = dataD.fetch()

# Print DataFrame
print(data)
print(dataD)

data.to_csv('wetterdaten_stuendlich.csv')


# Create Point for Vancouver, BC
bergkamen = Point(51.3656, 7.3834, 70)
print(bergkamen)