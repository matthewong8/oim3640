"""
MBTA Helper - Find nearest MBTA stops using Mapbox and MBTA APIs
"""

import requests
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
# Try loading from current directory first, then parent directories
env_path = Path('.env')
if not env_path.exists():
    env_path = Path('../.env')
if not env_path.exists():
    env_path = Path('../../.env')

load_dotenv(env_path)

# API Keys from .env file
MAPBOX_TOKEN = os.getenv('MAPBOX_API_KEY')
MBTA_TOKEN = os.getenv('MBTA_API_KEY')

# Debug: Check if keys are loaded
if not MAPBOX_TOKEN or not MBTA_TOKEN:
    print("\n⚠️  WARNING: Missing API keys!")
    print(f"  MAPBOX_API_KEY: {'Loaded ✓' if MAPBOX_TOKEN else 'NOT FOUND ✗'}")
    print(f"  MBTA_API_KEY: {'Loaded ✓' if MBTA_TOKEN else 'NOT FOUND ✗'}")
    print(f"  .env file checked at: {env_path.absolute()}")
    print(f"  .env file exists: {env_path.exists()}")
    print("\n  Make sure your .env file contains both MAPBOX_API_KEY and MBTA_API_KEY\n")
else:
    print("\n✓ API Keys loaded successfully")
    print(f"  MAPBOX_API_KEY: {'*' * (len(MAPBOX_TOKEN)-4) + MAPBOX_TOKEN[-4:]}")
    print(f"  MBTA_API_KEY: {'*' * (len(MBTA_TOKEN)-4) + MBTA_TOKEN[-4:]}\n")

MAPBOX_BASE_URL = 'https://api.mapbox.com/geocoding/v5/mapbox.places'
MBTA_BASE_URL = 'https://api-v3.mbta.com'


def get_coordinates(place_name):
    """
    Get latitude and longitude for a place name using Mapbox API
    
    Args:
        place_name (str): Name of the place (e.g., "Boston Common")
    
    Returns:
        tuple: (latitude, longitude) or None if not found
    """
    if not MAPBOX_TOKEN:
        print("ERROR: MAPBOX_API_KEY environment variable not set")
        return None
    
    try:
        # Mapbox API endpoint - search with Boston bias
        url = f"{MAPBOX_BASE_URL}/{place_name}.json"
        params = {
            'access_token': MAPBOX_TOKEN,
            'limit': 5,
            'proximity': '-71.0589,42.3601',  # Boston coordinates (lon, lat)
            'country': 'US',  # Limit to USA
            'bbox': '-71.5,42.0,-70.8,42.8'  # Boston area bounding box (minLon,minLat,maxLon,maxLat)
        }
        
        print(f"📍 Searching for: {place_name}")
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if not data['features']:
            print(f"  ✗ Location '{place_name}' not found in Boston area")
            return None
        
        # Extract coordinates from first result
        coordinates = data['features'][0]['geometry']['coordinates']
        longitude, latitude = coordinates[0], coordinates[1]
        
        # Verify we're in Boston area (rough check)
        if not (42.0 <= latitude <= 42.8 and -71.5 <= longitude <= -70.8):
            print(f"  ⚠️  WARNING: '{place_name}' found but NOT in Boston area")
            print(f"     Location: {data['features'][0]['place_name']}")
            print(f"     Coordinates: ({latitude:.4f}, {longitude:.4f})")
            return None
        
        print(f"  ✓ Found: {data['features'][0]['place_name']}")
        print(f"  Coordinates: ({latitude:.4f}, {longitude:.4f})")
        
        return (latitude, longitude)
    
    except requests.exceptions.RequestException as e:
        print(f"  ✗ Error calling Mapbox API: {e}")
        return None


def find_nearest_stop(latitude, longitude):
    """
    Find the nearest MBTA stop to given coordinates
    
    Args:
        latitude (float): Latitude coordinate
        longitude (float): Longitude coordinate
    
    Returns:
        dict: Stop information with name and wheelchair accessibility
              or None if not found
    """
    try:
        # MBTA API endpoint for stops
        url = f"{MBTA_BASE_URL}/stops"
        
        # Set up headers
        headers = {
            'Accept': 'application/json'
        }
        
        # Try with correct MBTA pagination syntax
        params = {
            'page[limit]': 50  # MBTA uses page[limit], not limit
        }
        
        print(f"🚇 Finding nearest MBTA stop...")
        print(f"   (Searching from coordinates: {latitude:.4f}, {longitude:.4f})")
        print(f"   Making request to: {url}")
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        print(f"   Response status: {response.status_code}")
        
        response.raise_for_status()
        
        data = response.json()
        
        if not data.get('data'):
            print("  ✗ No MBTA stops found in response")
            return None
        
        # Calculate distance to each stop and find nearest
        def distance(lat1, lon1, lat2, lon2):
            """Simple distance calculation (Euclidean)"""
            return ((lat2 - lat1)**2 + (lon2 - lon1)**2)**0.5
        
        nearest_stop = None
        min_distance = float('inf')
        
        for stop in data['data']:
            stop_lat = stop.get('attributes', {}).get('latitude')
            stop_lon = stop.get('attributes', {}).get('longitude')
            
            if stop_lat is not None and stop_lon is not None:
                dist = distance(latitude, longitude, stop_lat, stop_lon)
                if dist < min_distance:
                    min_distance = dist
                    nearest_stop = stop
        
        if not nearest_stop:
            print("  ✗ No valid MBTA stops found with coordinates")
            return None
        
        stop_info = {
            'name': nearest_stop.get('attributes', {}).get('name', 'Unknown'),
            'wheelchair_accessible': nearest_stop.get('attributes', {}).get('wheelchair_boarding', None),
            'latitude': nearest_stop.get('attributes', {}).get('latitude'),
            'longitude': nearest_stop.get('attributes', {}).get('longitude'),
            'id': nearest_stop.get('id')
        }
        
        print(f"  ✓ Nearest stop: {stop_info['name']}")
        print(f"  Distance: {min_distance:.4f} degrees")
        
        # Convert wheelchair accessibility to readable format
        wheelchair_val = stop_info['wheelchair_accessible']
        if wheelchair_val == 1:
            wheelchair_accessible = True
            print(f"  ♿ Wheelchair Accessible: Yes")
        elif wheelchair_val == 0:
            wheelchair_accessible = False
            print(f"  ♿ Wheelchair Accessible: No")
        else:
            wheelchair_accessible = None
            print(f"  ♿ Wheelchair Accessible: Unknown")
        
        stop_info['wheelchair_accessible'] = wheelchair_accessible
        
        return stop_info
    
    except requests.exceptions.RequestException as e:
        print(f"  ✗ Error calling MBTA API: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"    Response status: {e.response.status_code}")
            try:
                print(f"    Response text: {e.response.text[:300]}")
            except:
                pass
        return None


def find_stop_near(place_name):
    """
    Combined function: Find nearest MBTA stop to a place name
    
    Args:
        place_name (str): Name of the place (e.g., "Boston Common")
    
    Returns:
        tuple: (stop_name, wheelchair_accessible) or (None, None) if not found
    """
    print("\n" + "="*60)
    print(f"Looking for nearest MBTA stop to: {place_name}")
    print("="*60)
    
    # Step 1: Get coordinates
    coordinates = get_coordinates(place_name)
    if not coordinates:
        return (None, None)
    
    latitude, longitude = coordinates
    
    # Step 2: Find nearest stop
    stop_info = find_nearest_stop(latitude, longitude)
    if not stop_info:
        return (None, None)
    
    print("\n" + "─"*60)
    print("RESULT:")
    print(f"  Place: {place_name}")
    print(f"  Nearest Stop: {stop_info['name']}")
    print(f"  Wheelchair Accessible: {stop_info['wheelchair_accessible']}")
    print("─"*60 + "\n")
    
    return (stop_info['name'], stop_info['wheelchair_accessible'])


def main():
    """Test the MBTA helper with example locations"""
    
    print("\n" + "="*60)
    print("MBTA HELPER - Finding Nearest Stops")
    print("="*60)
    
    # Test locations
    test_places = [
        "Boston Common",
        "Fenway Park",
        "Harvard Square",
        "Logan Airport"
    ]
    
    results = []
    
    for place in test_places:
        stop_name, wheelchair_accessible = find_stop_near(place)
        results.append({
            'place': place,
            'stop': stop_name,
            'wheelchair': wheelchair_accessible
        })
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY OF RESULTS")
    print("="*60)
    for result in results:
        if result['stop']:
            wheelchair_str = "✓" if result['wheelchair'] else "✗" if result['wheelchair'] is False else "?"
            print(f"{result['place']:<20} → {result['stop']:<25} {wheelchair_str}")
        else:
            print(f"{result['place']:<20} → NOT FOUND")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()
