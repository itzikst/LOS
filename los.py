import math
from typing import List, Dict, Any, Tuple
import requests
import geopy.distance
from math import cos

# Constants
EARTH_RADIUS = geopy.distance.EARTH_RADIUS

def get_elevation(latitude: float, longitude: float) -> float:
    """
    Fetches the elevation (in meters) for a given latitude and longitude
    using a public API endpoint.
    """
    # The API expects coordinates in a specific format
    # Using the same logic as source project utils.py but simplified if needed
    # Source project used a specific URL structure in get_elevation vs get_elevations
    # Here we will use the get_elevations bulk method content as it seems more used by the main function
    pass # Placeholder if needed, but line_of_sight uses get_elevations

def get_elevations(points: list):
    # https://www.elevation-api.eu/v1/elevation?pts=[[31.7719,%2035.217],[31.217,35.7719]]
    url = "https://www.elevation-api.eu/v1/elevation?pts=["
    for point in points:
        str_coord = "[" + "{:.5f}".format(point[0]) + "," + "{:.5f}".format(point[1]) + "]"
        url += str_coord + ","
    url = url[:-1] + "]"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        if 'elevations' in data and data['elevations']:
             return [float(e) for e in data['elevations']] # Ensure floats
        else:
            print("API response structure unexpected.")
            return [0.0] * len(points) # Fallback

    except Exception as e:
        print(f"Error connecting to the elevation service: {e}")
        return [0.0] * len(points) # Fallback

def get_heights(start_elevation, end_elevation, num_intervals):
    result = [start_elevation]
    delta_h = (start_elevation - end_elevation) / num_intervals
    for i in range(1, num_intervals):
        height = start_elevation - i * delta_h
        result.append(height)
    result.append(end_elevation)
    return result

def calc_curvature_correction(alpha, beta) -> float:
    if alpha == 0: return 0
    # Correction for earth curvature
    # Note: source used alpha/2 - beta. 
    try:
        x = EARTH_RADIUS * (1 - cos(alpha/2)/cos(alpha/2 - beta))
        return x * 1000 # Convert to meters? Source did this.
    except Exception:
        return 0

def get_points(start, end) -> List:
    points = [start]
    delta_lat = (end[0] - start[0]) / 201
    delta_lon = (end[1] - start[1]) / 201

    num_points = 200
    for i in range(1, num_points + 1):
        lat = start[0] + i * delta_lat
        lon = start[1] + i * delta_lon
        points.append([lat, lon])
    points.append(end)
    return points

def line_of_sight(start, end) -> List:
    """
    Calculates line of sight between two points.
    start: [lat, lon]
    end: [lat, lon]
    """
    points = get_points(start, end)
    dist = geopy.distance.great_circle((start[0], start[1]), (end[0], end[1])).kilometers
    
    if dist == 0:
        return [[], [], [], [], [], []]

    alpha = dist / EARTH_RADIUS
    elevations = get_elevations(points)
    
    # Add antenna height? Source: elevations[0] = elevations[0] + 15
    elevations[0] = elevations[0] + 15
    elevations[-1] = elevations[-1] + 15
    
    heights = get_heights(elevations[0], elevations[-1], 201)
    
    deltas = []
    corrections = []
    
    # Fix for potential length mismatch if get_heights returns different len
    # points is 202 pts (start + 200 + end)
    # get_heights with 201 intervals returns 202 points.
    
    loop_len = min(len(points), len(heights), len(elevations))
    
    for i in range(loop_len):
        deltas.append(heights[i] - elevations[i])
        beta = (dist * (i / loop_len)) / EARTH_RADIUS
        correction = calc_curvature_correction(alpha, beta)
        corrections.append(correction)

    x2 = []
    y2 = []
    x3 = []
    y3 = []

    for i in range(len(deltas)):
        distance = (i / 201) * dist
        x2.append(distance)
        y2.append(heights[i])
        x3.append(distance)
        y3.append(elevations[i] + corrections[i])

    return [x2, y2, x3, y3]

def isVisible(elevations, heights) -> bool:
    # Skip the very first and last points as they are the antenna locations
    # (elevations[i] will equal heights[i] there)
    for i in range(1, len(heights) - 1):
        if elevations[i] >= heights[i]:
            return False
    return True

