import sys

egg_path='../lib/dist/carla-0.9.6-py3.6-linux-x86_64.egg'
sys.path.append(egg_path)

import carla

import threading
import numpy as np
import math

city_roads = [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 24, 25, 26, 27, 28, 29, 30, 32, 
51, 52, 54, 56, 58, 59, 60, 69, 70, 82, 83, 84, 86, 88, 89, 
105, 107, 114, 118, 125, 126, 132, 134, 137, 142, 144, 156, 157, 168, 169,
180, 184, 185, 186, 188, 189, 194, 195, 196, 198, 199, 200, 202, 207, 209, 
223, 227, 228, 246, 251, 253, 254, 259, 
288, 291, 292, 293, 303, 308, 309, 310, 316, 325, 326, 327, 337, 343, 346, 352, 353, 354, 356, 359, 360, 364, 
384, 385, 388, 389, 390, 393, 399, 400, 405, 408, 409, 412, 413, 415, 417, 419, 425, 426, 
441, 442, 452, 455, 460, 460, 460, 461, 462, 466, 468, 471, 480, 485, 489, 
509, 510, 520, 521, 580, 581, 582, 585, 586, 587, 590, 591, 594, 595, 603, 604, 
638, 644, 645, 647, 691, 692, 696, 697, 700, 701, 742, 743, 746, 749, 750, 752, 759, 760, 765, 768, 769, 772, 774, 777, 780, 781, 
800, 801, 891, 893, 894, 894, 898, 899, 913, 914, 934, 935, 940, 944, 949, 951, 955, 956, 957, 959, 965, 972, 973, 975, 978, 989, 992, 994, 995]

def show(env, loc,texto='O',c=carla.Color(r=255, g=0, b=0)):

	env.world.debug.draw_string(loc, texto, draw_shadow=False,
				                                       color=c, life_time=0.5,
				                                       persistent_lines=True)

def get_angle(loc_1, loc_2):
	return math.atan2((loc_1.y - loc_2.y),(loc_1.x - loc_2.x))

def valid(w1, w2, heading):
	if abs(get_angle(w1.transform.location,w2.transform.location) - heading) < np.pi/4:
		return True

	return False

def look(env, vehicle, distance):
	car_loc = vehicle.get_transform().location
	car_waypoint = env.map.get_waypoint(car_loc, project_to_road=True, lane_type=carla.LaneType.Driving)

	nearest_waypoints = [w for w in car_waypoint.next(distance) if w.road_id not in city_roads]

	if len(nearest_waypoints) == 0:
		return car_waypoint.next(distance)[0]

	return nearest_waypoints[0]

def generate_highwaypoints(env, gap=5.0):

	map_waypoints = env.map.generate_waypoints(gap)

	waypoints = [w for w in map_waypoints if p.road_id not in city_roads]

	return waypoints

def fill_config(actual, ref):

	new = {}
	for key in ref.keys():
		if key in actual.keys():
			new[key] = actual[key]
		else:
			new[key] = ref[key]

	return new

def get_rgb_image(image, config):
	i = np.array(image.raw_data)
	i2 = i.reshape((config['height'], config['width'], 4))
	i3 = i2[:,:,:3]

	return i3 

def load_map(env, mapa):
    env.world = env.client.load_world(mapa)

def change_weather(env, weather):
    env.world.set_weather(getattr(carla.WeatherParameters, weather))

def setup(env):
    if env.world.get_map().name != 'Town04':
        thread = threading.Thread(target=lambda:load_map(env,'Town04'))
        thread.start()

        thread.join()

    if env.world.get_weather() != 'ClearNoon':
        thread = threading.Thread(target=lambda:change_weather(env,'ClearNoon'))
        thread.start()

        thread.join()

def distancia(loc_1,loc_2):
	
    return math.sqrt((loc_1.x-loc_2.x)**2 + (loc_1.y-loc_2.y)**2)