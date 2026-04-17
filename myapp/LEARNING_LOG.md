# MBTA Stop Finder - Learning Log

## Week 1: Planning & API Setup

### What I Did
- Planned the project architecture (separation of concerns)
- Set up Mapbox and MBTA API accounts
- Created initial helper functions for API calls
- Tested API endpoints with curl and Python requests

### What I Learned
- How to authenticate with Mapbox API using access tokens
- MBTA API returns data in JSON:API format (different from typical REST)
- Importance of geographic bounding boxes for geocoding accuracy
- How to handle API errors gracefully

### Challenges
- Initially didn't understand MBTA API response structure
- Had to debug coordinate system (longitude, latitude order)
- Realized API required specific parameter formatting

### Key Takeaways
- Read API documentation thoroughly before coding
- Test API calls independently before integrating into app
- Use environment variables for sensitive API keys

---

## Week 2: Flask Web App Development

### What I Did
- Built Flask app with home and results routes
- Created HTML templates for user interface
- Implemented form validation and error handling
- Added custom CSS styling

### What I Learned
- Flask routing and template rendering with Jinja2
- How to pass data between routes using POST/GET
- Form handling and input validation
- CSS styling for responsive design

### Challenges
- Had to restructure helper functions to get individual coordinates
- Handling both place not found and stop not found errors
- Responsive design for mobile devices

### Key Takeaways
- Separation of concerns makes code maintainable
- Input validation prevents bugs and improves user experience
- Mobile-first CSS design approach is important

---

## Week 3: Map Integration & Polish

### What I Did
- Integrated Mapbox GL JS for interactive maps
- Added markers for location and stop
- Implemented map auto-zoom and connecting line
- Enhanced UI with animations and better styling
- Created comprehensive README and documentation

### What I Learned
- How to use Mapbox GL JS API for real-time map rendering
- GeoJSON format for displaying geographic features
- Template variables in JavaScript (Jinja2 integration)
- Importance of user documentation

### Challenges
- Passing Flask variables to JavaScript without breaking JSON syntax
- Getting map bounds to fit both markers properly
- Styling Mapbox popups and markers

### Key Takeaways
- Documentation makes projects maintainable
- User experience matters as much as functionality
- Testing in multiple browsers/devices is important

---

## Technical Skills Gained

### Backend
- ✅ Python Flask framework
- ✅ API integration and error handling
- ✅ Environment variable management
- ✅ Geographic data processing

### Frontend
- ✅ HTML5 semantic markup
- ✅ CSS3 styling and animations
- ✅ JavaScript DOM manipulation
- ✅ Responsive design principles

### DevOps/Best Practices
- ✅ Git version control
- ✅ .gitignore for sensitive files
- ✅ Code modularity and organization
- ✅ API documentation reading

### Problem-Solving
- ✅ Debugging API errors
- ✅ Working with third-party APIs
- ✅ Handling edge cases (invalid input, missing data)
- ✅ Performance optimization

---

## Reflection

### What Went Well
- API integration was smoother than expected once I understood the format
- Flask made building the web app intuitive
- The separation between `mbta_helper.py` and `app.py` made testing easier
- User feedback helped improve the interface

### What Was Challenging
- Initial confusion about API parameter formats (especially MBTA's `page[limit]`)
- Integrating front-end JavaScript with back-end Flask variables
- Getting the map to display correctly with Jinja2 templating

### If I Could Do It Again
- I would test API responses more thoroughly before building the Flask app
- I would write unit tests for the helper functions
- I would involve users in testing earlier to catch UI issues

### Future Learning Goals
- Learn about asynchronous requests (AJAX) for real-time updates
- Explore caching strategies for API calls
- Study more advanced map interactions
- Build a mobile app version using React Native

---

## Time Breakdown

| Task | Time | Notes |
|------|------|-------|
| Planning & Setup | 2 hours | Getting API keys, initial setup |
| API Integration | 4 hours | Debugging API errors, understanding formats |
| Flask App | 5 hours | Routes, templates, validation |
| Map Integration | 3 hours | Mapbox setup, marker placement |
| Styling & Polish | 3 hours | CSS, animations, responsive design |
| Documentation | 2 hours | README, PROPOSAL, LEARNING_LOG |
| Testing & Debugging | 3 hours | Edge cases, browser testing |
| **Total** | **22 hours** | |

---

## Resources Used

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Mapbox API Docs](https://docs.mapbox.com/api/)
- [MBTA API v3 Docs](https://api-v3.mbta.com/)
- [Mapbox GL JS Documentation](https://docs.mapbox.com/mapbox-gl-js/)
- [MDN Web Docs](https://developer.mozilla.org/) - HTML, CSS, JavaScript reference
- Stack Overflow - Troubleshooting specific issues

---

## Conclusion

This project helped me understand the full stack of web development - from backend API integration to frontend visualization. The most valuable lesson was that good architecture and documentation make a huge difference in project maintainability. I'm excited to build more complex projects with these skills!
