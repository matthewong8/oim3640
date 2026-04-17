"""
MBTA Web App - Find nearest MBTA stops
Flask application for the MBTA helper
"""

from flask import Flask, render_template, request, redirect, url_for
import mbta_helper
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MAPBOX_TOKEN = os.getenv('MAPBOX_API_KEY')

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    """Home page with search form"""
    return render_template('index.html')


@app.route('/results', methods=['POST'])
def results():
    """Results page - handles form submission"""
    
    # Get the place name from the form
    place_name = request.form.get('place_name', '').strip()
    
    # Validate input
    if not place_name:
        return render_template('index.html', error='Please enter a place name')
    
    if len(place_name) < 2:
        return render_template('index.html', error='Place name must be at least 2 characters')
    
    # Find the nearest stop
    try:
        # Get coordinates for the location
        location_coords = mbta_helper.get_coordinates(place_name)
        if not location_coords:
            return render_template(
                'index.html',
                error=f'Could not find a location matching "{place_name}". Please check the spelling and try again.'
            )
        
        location_lat, location_lon = location_coords
        
        # Find the nearest stop
        stop_info = mbta_helper.find_nearest_stop(location_lat, location_lon)
        
        if not stop_info:
            return render_template(
                'index.html',
                error=f'No MBTA stops found near "{place_name}". Try a different location.'
            )
        
        stop_name = stop_info['name']
        wheelchair_accessible = stop_info['wheelchair_accessible']
        stop_lat = stop_info['latitude']
        stop_lon = stop_info['longitude']
        
        # Format wheelchair accessibility for display
        if wheelchair_accessible is True:
            wheelchair_status = '✓ Yes'
            wheelchair_class = 'accessible'
        elif wheelchair_accessible is False:
            wheelchair_status = '✗ No'
            wheelchair_class = 'not-accessible'
        else:
            wheelchair_status = '? Unknown'
            wheelchair_class = 'unknown'
        
        return render_template(
            'results.html',
            place_name=place_name,
            stop_name=stop_name,
            wheelchair_status=wheelchair_status,
            wheelchair_class=wheelchair_class,
            location_lat=location_lat,
            location_lon=location_lon,
            stop_lat=stop_lat,
            stop_lon=stop_lon,
            mapbox_token=MAPBOX_TOKEN
        )
    
    except Exception as e:
        # Catch any unexpected errors
        error_message = f'An error occurred while processing your request: {str(e)}'
        return render_template('index.html', error=error_message)


@app.route('/search', methods=['GET'])
def search():
    """Redirect to home (allows users to search again)"""
    return redirect(url_for('home'))


@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    return render_template('500.html', error=str(e)), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
