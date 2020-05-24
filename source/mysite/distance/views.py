from django.shortcuts import render
from distance.models import Distance, Location
from distance.forms import LocationForm
import urllib.request
from math import sin, cos, sqrt, atan2, radians
import json


endpoint = 'https://maps.googleapis.com/maps/api/geocode/json?'
API_KEY = ''


def IndexView(request):
    template_name = 'distance/index.html'
    form = LocationForm() # defined in forms.py
    return render(request, template_name, {'form': form})


def ResultsView(request):
    entered_origin = request.GET.get('origin')
    entered_destination = request.GET.get('destination')

    origin_data = Location(location = entered_origin)
    get_address_info(origin_data)
    origin_data.save()

    destination_data = Location(location = entered_destination)
    get_address_info(destination_data)
    destination_data.save()

    distance = Distance(
                        formatted_origin = origin_data.formatted_location,
                        origin_lat = origin_data.location_lat,
                        origin_long = origin_data.location_long,
                        formatted_destination=destination_data.formatted_location,
                        destination_lat = destination_data.location_lat,
                        destination_long = destination_data.location_long
                        )
    calculate_distance(distance)
    distance.save()

    # format data into a dictionary
    data = {
        "origin": {
            "entered_origin": origin_data.formatted_location,
            "origin_lat": origin_data.location_lat,
            "origin_long": origin_data.location_long,
            "formatted_origin": origin_data.formatted_location
        }, "destination": {
            "entered_destination": destination_data.formatted_location,
            "destination_lat": destination_data.location_lat,
            "destination_long": destination_data.location_long,
            "formatted_destination": destination_data.formatted_location
        }, "distance": distance.calculated_distance
    }

    data = json.loads(json.dumps(data)) # convert dictionary to json
    context = {'data': data}
    return render(request, 'distance/results.html', context)



def calculate_distance(data):
    # function to calculate distance between two GPS coordinates
    # set to None if one or both locations were not retrieved from Rest API

    if data.origin_lat == None or data.destination_lat == None:
        # case place or address not found with geocode api for inputted data
        calculated_distance = None
        return False

    radius = 6371000 # in meters
    phi_1 = radians(data.origin_lat)
    phi_2 = radians(data.destination_lat)
    delta_phi = radians(data.destination_lat - data.origin_lat)
    delta_lambda = radians(data.destination_long - data.origin_long)

    a = sin(delta_phi / 2)**2 + cos(phi_1) * cos(phi_2) * sin(delta_lambda / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    calc_distance = (radius * c) / 1000 # distance in kilometers
    calc_distance *= 0.621371 # convert to miles

    data.calculated_distance = round(calc_distance, 2)
    return True


def get_address_info(data):
    # rest api function that takes a location as a request and returns
    # complete address information including GPS coordinates and formatted address
    # from the google maps geocode api

    location = data.location.replace(' ', '+')
    location_nav_request = 'address={}&key={}'.format(location, API_KEY)
    location_request = endpoint + location_nav_request
    location_response = urllib.request.urlopen(location_request).read()
    location_data = json.loads(location_response)
    if (location_data['status']=="ZERO_RESULTS"):
        data.formatted_location = 'Address or place "{}" not found.'.format(data.location)
        return False
    else:
        location_coords = location_data['results'][0]['geometry']['location']
        data.location_lat = location_coords['lat']
        data.location_long = location_coords['lng']
        data.formatted_location = location_data['results'][0]['formatted_address']
        return True
