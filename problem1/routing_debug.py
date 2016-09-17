class city:
    def __init__(self, city_name, state_name, latitude, longitude):
        self.city = city_name
        self.state = state_name
        self.latitude = latitude
        self.longitude = longitude
        self.segmentlist = {}

# class segment:
#     def __init__(self, from_city, to_city, length, speed, highway_name):
#         self.from_city = city_name
#         self.to_city = to_city
#         self.length = length
#         self.speed = speed
#         self.highway_name = highway_name

in_city_gps = open("city-gps.txt")
city_data = in_city_gps.readlines()
cities = {}
for line in city_data:
    fields = line.split(' ')
    city_state = fields[0].split(',_')
    cities[city_state[0]] = city_state[0]
    cities[city_state[0]] = city(city_state[0], city_state[1], fields[1], fields[2])
    # print "City Name:" + city_state[0]
    # print "State Name:" + city_state[1]
    # print "Latitude:" + fields[1]
    # print "Longitude:" + fields[2]
in_city_gps.close()
print cities["Abbot_Village"].state

# in_road_seg = open("road-segments.txt")
# seg_data = in_road_seg.readlines()
# cities = {}
# for line in seg_data:
#     fields = line.split(' ')
#     city_state = fields[0].split(',_')
#     cities[city_state[0]] = city_state[0]
#     cities[city_state[0]] = city(city_state[0], city_state[1], fields[1], fields[2])
#     # print "City Name:" + city_state[0]
#     # print "State Name:" + city_state[1]
#     # print "Latitude:" + fields[1]
#     # print "Longitude:" + fields[2]
# in_city_gps.close()