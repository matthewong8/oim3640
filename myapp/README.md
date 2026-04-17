# 🚇 MBTA Stop Finder

A web application that helps users find the nearest MBTA (Massachusetts Bay Transportation Authority) subway or light rail stops to any location in Boston. Includes real-time location data, wheelchair accessibility information, and an interactive map.

## Features

- 🔍 **Location Search** - Enter any place name in Boston (landmarks, addresses, parks, businesses)
- 📍 **Nearest Stop Detection** - Automatically finds the closest MBTA subway/light rail stop
- ♿ **Accessibility Information** - Shows wheelchair accessibility status for each stop
- 🗺️ **Interactive Map** - Visual representation of the location and nearest stop with connecting line
- 🎨 **Beautiful UI** - Modern, responsive design that works on desktop and mobile
- ⚡ **Error Handling** - Graceful handling of edge cases and API errors

## Tech Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **APIs**:
  - [Mapbox Geocoding API](https://docs.mapbox.com/api/search/geocoding/) - Location lookup
  - [MBTA API v3](https://api-v3.mbta.com/) - Real-time transit data
  - [Mapbox GL JS](https://docs.mapbox.com/mapbox-gl-js/) - Interactive maps
- **Environment**: Python 3.x, Anaconda

## Project Structure

```
myapp/
├── app.py                  # Flask application and routes
├── mbta_helper.py          # Core API integration logic
├── .env                    # API keys (not committed)
├── .env.example            # Example environment variables
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── templates/
│   ├── index.html          # Home page with search form
│   ├── results.html        # Results page with map
│   └── 404.html            # 404 error page (optional)
└── static/
    └── style.css           # Custom styling
```

## Setup Instructions

### Prerequisites

- Python 3.x (via Anaconda recommended)
- Mapbox account (free tier available)
- MBTA API key (free, no registration needed)

### 1. Clone/Download the Project

```bash
cd c:\Users\mong3\Documents\GitHub\oim3640\myapp
```

### 2. Install Dependencies

```bash
pip install flask python-dotenv requests
```

Or if you already have Flask installed:
```bash
pip install python-dotenv requests
```

### 3. Get API Keys

**Mapbox API Key:**
1. Go to [mapbox.com](https://mapbox.com)
2. Sign up for a free account
3. Go to your Account settings
4. Copy your default public token

**MBTA API Key:**
1. Go to [api-v3.mbta.com](https://api-v3.mbta.com/)
2. Sign up (optional, but recommended)
3. Copy your API key from the dashboard

### 4. Set Up Environment Variables

Create a `.env` file in the `myapp/` folder:

```
MAPBOX_API_KEY=your_mapbox_key_here
MBTA_API_KEY=your_mbta_key_here
```

**Important:** Never commit `.env` to version control! It's already in `.gitignore`.

### 5. Run the Application

```bash
python app.py
```

You should see:
```
✓ API Keys loaded successfully
 * Running on http://127.0.0.1:5000
```

### 6. Open in Browser

Go to: `http://localhost:5000`

## Usage

### Finding the Nearest MBTA Stop

1. **Enter a Location** - Type any place name in Boston
   - Examples: "Boston Common", "Fenway Park", "Harvard Square", "Logan Airport"
   
2. **Click "Find Nearest Stop"** - The app searches for the location and nearest transit stop

3. **View Results** - See:
   - Location name
   - Nearest MBTA stop name
   - Wheelchair accessibility status
   - Interactive map with both locations marked

4. **Interact with Map**:
   - Zoom and pan to explore
   - Click markers for more information
   - Blue marker = searched location
   - Red marker = nearest MBTA stop
   - Dashed line = connection between them

## How It Works

### Backend Flow

```
User Input (Place Name)
    ↓
Mapbox API → Get Coordinates (Lat/Lon)
    ↓
MBTA API → Find Nearest Stop
    ↓
Calculate Distance → Return Closest Stop
    ↓
Display Results with Map
```

### Key Components

**mbta_helper.py:**
- `get_coordinates(place_name)` - Converts place name to coordinates using Mapbox
- `find_nearest_stop(lat, lon)` - Finds closest MBTA stop using MBTA API
- `find_stop_near(place_name)` - Combines both functions (main entry point)

**app.py:**
- `home()` - Displays search form
- `results()` - Processes search and returns results
- Error handling for missing locations or API failures

## Accessibility Information

The app shows three wheelchair accessibility levels:

| Status | Meaning |
|--------|---------|
| ✓ Yes | Stop has wheelchair accessible features |
| ✗ No | Stop may not be fully wheelchair accessible |
| ? Unknown | Accessibility information not available |

⚠️ **Note:** For the most current accessibility information, always check the [official MBTA website](https://www.mbta.com/)

## Error Handling

The app gracefully handles:

- ❌ **Location not found** - Shows helpful message to try different spelling
- ❌ **No nearby stops** - Indicates that no MBTA stops exist near the location
- ❌ **API errors** - Displays user-friendly error messages
- ❌ **Invalid input** - Validates place name before searching

## Development

### Adding New Features

1. **Modify `mbta_helper.py`** for API logic
2. **Update `app.py`** for new routes
3. **Edit templates** for UI changes
4. **Update `style.css`** for styling

### Testing

```bash
# Test helper functions
python -c "from mbta_helper import find_stop_near; print(find_stop_near('Boston Common'))"
```

### Debug Mode

Debug mode is enabled by default. To disable for production:

Edit `app.py` line 74:
```python
app.run(debug=False, port=5000)  # Set to False for production
```

## Troubleshooting

### Issue: "MAPBOX_API_KEY not found"
**Solution:** Make sure `.env` file exists in `myapp/` folder with your API key

### Issue: "404 Client Error: Bad Request from MBTA API"
**Solution:** Make sure MBTA_API_KEY is valid and in the correct format in `.env`

### Issue: Port 5000 already in use
**Solution:** Edit `app.py` and change the port:
```python
app.run(debug=True, port=5001)  # Use port 5001 instead
```

### Issue: CSS/Map not loading
**Solution:** Clear browser cache (Ctrl+Shift+Delete) and reload

## Future Enhancements

- [ ] Real-time departure information
- [ ] Route planning between two locations
- [ ] Save favorite stops
- [ ] Multiple stop suggestions
- [ ] Nearby amenities (restaurants, shops, etc.)
- [ ] User accounts and preferences
- [ ] Mobile app version

## API Documentation

- [Mapbox Geocoding API Docs](https://docs.mapbox.com/api/search/geocoding/)
- [MBTA API v3 Docs](https://api-v3.mbta.com/)
- [Mapbox GL JS Docs](https://docs.mapbox.com/mapbox-gl-js/)

## License

This project is created for educational purposes.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify API keys are correct
3. Check that all dependencies are installed
4. Review error messages in the browser console (F12)

## Screenshots

### Home Page
Search form with example locations

### Results Page
- Location details
- Nearest stop information
- Wheelchair accessibility status
- Interactive Mapbox map with markers and connecting line

---

**Happy Transit Exploring! 🚇**
