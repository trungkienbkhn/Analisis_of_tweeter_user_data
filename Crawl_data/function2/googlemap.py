from geopy.geocoders import Nominatim
geolocator = Nominatim()
location = geolocator.geocode("Hồ Chí Minh")
print(location.latitude, location.longitude)