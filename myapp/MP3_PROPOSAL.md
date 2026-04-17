# MBTA Stop Finder - Project Proposal

## What I'm Building
A web application that allows users to enter any location in Boston and find the nearest MBTA stop with accessibility information displayed on an interactive map.

## Why I Chose This
A lot of people use public transportation and it is a very common mode of transportation. It can be confusing to find which stop is closest or which stop is the right stop to reach your destination, especially when you may be unfamiliar with the area. This web app makes it much easier for citizens to navigate the MBTA system and get real guidance from the application.

## Core Features
- Take user input (address or name of place)
- Find the nearest MBTA stop through the MBTA API
- Display the stop name and wheelchair accessibility status
- Show an interactive map with location and stop markers
- Provide error handling for invalid locations

## What I Learned

### Technologies Used
- **Backend**: Python Flask framework
- **Frontend**: HTML5, CSS3, JavaScript
- **APIs**: 
  - Mapbox Geocoding API (location lookup)
  - MBTA API v3 (transit data)
  - Mapbox GL JS (interactive maps)
- **Environment**: Python 3.x, pip packages

### Key Challenges & Solutions

1. **API Integration**
   - **Challenge**: Getting the MBTA API to work with correct parameters
   - **Solution**: Learned that MBTA uses JSON:API format with `page[limit]` instead of `limit`
   - **Takeaway**: API documentation is critical; error messages guide the way

2. **Geolocation Accuracy**
   - **Challenge**: Mapbox was returning locations outside Boston area
   - **Solution**: Added bounding box constraints and verification checks
   - **Takeaway**: Geocoding APIs need geographic constraints for accuracy

3. **Distance Calculation**
   - **Challenge**: MBTA API doesn't provide built-in nearest-stop filtering
   - **Solution**: Fetched all stops and calculated distance manually
   - **Takeaway**: Sometimes you need to implement logic client-side

4. **Map Integration**
   - **Challenge**: Passing coordinates from Flask to JavaScript template
   - **Solution**: Used Jinja2 template variables in JavaScript
   - **Takeaway**: Backend and frontend need to communicate data clearly

### Skills Developed
- ✅ API integration and error handling
- ✅ Flask web framework fundamentals
- ✅ Front-end to back-end data flow
- ✅ Geographic data processing
- ✅ Interactive map implementation
- ✅ User input validation
- ✅ Environment variable management (security best practices)

### What I'd Improve Next
- Add real-time departure information
- Implement route planning between two locations
- Add user authentication and saved favorites
- Create a mobile-optimized version
- Add more detailed stop information (accessibility features, nearby amenities)
- Implement caching for performance optimization

## Deliverables Met
- ✅ Functional web app that finds nearest MBTA stops
- ✅ Professional UI with CSS styling
- ✅ API pipeline working (Mapbox + MBTA)
- ✅ Interactive map with markers
- ✅ Error handling and validation
- ✅ Complete README with setup instructions
- ✅ Clean, modular code architecture

## How to Run
```bash
cd myapp
pip install flask python-dotenv requests
# Add .env with MAPBOX_API_KEY and MBTA_API_KEY
python app.py
# Open http://localhost:5000
```

## Project Repository Structure
```
myapp/
├── app.py                    # Flask routes
├── mbta_helper.py            # API logic
├── README.md                 # Setup & usage guide
├── PROPOSAL.md               # This file
├── LEARNING_LOG.md           # Learning outcomes
├── .env                      # API keys (not committed)
├── templates/
│   ├── index.html            # Home page
│   └── results.html          # Results with map
└── static/
    └── style.css             # Styling
```
