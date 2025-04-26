"""Constants for the Houston Trash integration."""
from datetime import timedelta

DOMAIN = "houston_trash"
PLATFORMS = ["sensor", "calendar"]

# Configuration
CONF_BASE_URL = "base_url"

# Defaults
DEFAULT_SCAN_INTERVAL = timedelta(hours=12)
DEFAULT_NAME = "Houston Trash"

# ArcGIS Dashboard URL
DASHBOARD_URL = "https://mycity.maps.arcgis.com/apps/dashboards/cb0ac86b3b434513b5f22428385820f3"

CONFIG_INSTRUCTIONS = """
To find your route ID:

1. Open the [Trash Collection Dashboard]({dashboard_url})
2. Use the search function or zoom to your location
3. Click on your area to see the route information
4. The route ID will be in the format `SW4TH_08` where:
   - First two letters indicate the quadrant (NE, NW, SE, SW)
   - Next part indicates the week (1st, 2nd, 3rd, 4th)
   - Last part indicates the day (TH for Thursday, etc.)
   - Final number is the route number
"""

# Sensor types
SENSOR_TYPES = {
    "waste": {
        "name": "Trash Next Pickup",
        "icon": "mdi:delete-circle",
        "unit_of_measurement": None,
    },
    "recycle": {
        "name": "Recycling Next Pickup",
        "icon": "mdi:recycle",
        "unit_of_measurement": None,
    },
}

# Calendar types
CALENDAR_TYPES = {
    "waste": {
        "name": "Trash Pickup Calendar",
        "icon": "mdi:delete-circle",
    },
    "recycle": {
        "name": "Recycling Pickup Calendar",
        "icon": "mdi:recycle",
    },
} 