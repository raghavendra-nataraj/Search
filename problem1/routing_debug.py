class city:
    def __init__(self, city_name, state_name, latitude, longitude):
        self.city = city_name
        self.state = state_name
        self.latitude = latitude
        self.longitude = longitude
        self.segmentlist = {}

in_city_gps = open("city-gps.txt")
city_data = in_city_gps.readlines()
cities = {}
for line in city_data:
    fields = line.split(' ')
    city_state = fields[0].split(',_')
    cities[city_state[0]] = city(city_state[0], city_state[1], fields[1], fields[2])
in_city_gps.close()
print cities["Abbot_Village"].state

