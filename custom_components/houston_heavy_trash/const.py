"""Constants for the Houston Heavy Trash integration."""
from datetime import timedelta

DOMAIN = "houston_heavy_trash"
PLATFORMS = ["sensor", "calendar"]

# Configuration
CONF_ROUTES = "routes"
CONF_NAME = "name"
CONF_ROUTE_ID = "route_id"

# Defaults
DEFAULT_SCAN_INTERVAL = timedelta(minutes=30)
DEFAULT_NAME = "Heavy Trash"

# Sensor types
SENSOR_TYPES = {
    "status": {
        "name": "Status",
        "icon": "mdi:trash-can",
        "unit_of_measurement": None,
    },
    "next_pickup": {
        "name": "Next Pickup",
        "icon": "mdi:calendar",
        "unit_of_measurement": None,
    },
    "service_type": {
        "name": "Service Type",
        "icon": "mdi:information",
        "unit_of_measurement": None,
    },
    "service_week": {
        "name": "Service Week",
        "icon": "mdi:calendar-week",
        "unit_of_measurement": None,
    },
    "service_day": {
        "name": "Service Day",
        "icon": "mdi:calendar-today",
        "unit_of_measurement": None,
    },
    "quadrant": {
        "name": "Quadrant",
        "icon": "mdi:map-marker",
        "unit_of_measurement": None,
    },
}

# API
ARCGIS_SERVICE_URL = "https://services.arcgis.com/NummVBqZSIJKUeVR/arcgis/rest/services/HeavyTrashProgress_view_layer/FeatureServer/0/query"

ATTRIBUTION = "Data provided by City of Houston"

# Configuration
CONF_ROUTE = "route"

# Defaults
DEFAULT_NAME = "Heavy Trash"
SCAN_INTERVAL = 30  # minutes

# API Configuration
ARCGIS_BASE_URL = "https://services2.arcgis.com/5I5F5H5T7wzJ5Nq7/arcgis/rest/services"
ARCGIS_LAYER_URL = f"{ARCGIS_BASE_URL}/HeavyTrashRoutes/FeatureServer/0/query"

# Query parameters
ARCGIS_QUERY_PARAMS = {
    "where": "1=1",
    "outFields": "ROUTE,STATUS,DAYS_UNTIL_PICKUP",
    "returnGeometry": "false",
    "f": "json"
}

# Status mapping
STATUS_MAPPING = {
    "In Progress": "Pickup in Progress",
    "1-3 Days": "1-3 Days Until Pickup",
    "4-7 Days": "4-7 Days Until Pickup",
    "8+ Days": "8+ Days Until Pickup",
    "Completed": "Pickup Completed",
    "Unknown": "Unknown Status"
}

# ArcGIS Dashboard URL
DASHBOARD_URL = "https://mycity.maps.arcgis.com/apps/dashboards/cb0ac86b3b434513b5f22428385820f3"

CONFIG_INSTRUCTIONS = """
To find your route ID:

1. Open the [Heavy Trash Progress Dashboard]({dashboard_url})
2. Use the search function or zoom to your location
3. Click on your area to see the route information
4. The route ID will be in the format `SW4TH_08` where:
   - First two letters indicate the quadrant (NE, NW, SE, SW)
   - Next part indicates the week (1st, 2nd, 3rd, 4th)
   - Last part indicates the day (TH for Thursday, etc.)
   - Final number is the route number
"""

# Sensor attributes
ATTR_ROUTE_ID = "route_id"
ATTR_SERVICE_TYPE = "service_type"
ATTR_SERVICE_WEEK = "service_week"
ATTR_SERVICE_DAY = "service_day"
ATTR_QUADRANT = "quadrant"
ATTR_NEXT_PICKUP = "next_pickup"
ATTR_STATUS = "status"

# Service types
SERVICE_TYPE_HEAVY_TRASH = "HT"

# Status values
STATUS_COMPLETED = "Completed"
STATUS_IN_PROGRESS = "In Progress"
STATUS_SCHEDULED = "Scheduled"
STATUS_UNKNOWN = "Unknown"

# Update interval (in minutes)
UPDATE_INTERVAL = 30 