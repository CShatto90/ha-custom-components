"""Constants for the Houston Heavy Trash integration."""

DOMAIN = "houston_heavy_trash"
NAME = "Houston Heavy Trash"
VERSION = "1.0.0"
ATTRIBUTION = "Data provided by City of Houston"

# Configuration
CONF_ROUTE = "route"

# Defaults
DEFAULT_NAME = "Heavy Trash"
SCAN_INTERVAL = 30  # minutes

# API Configuration
ARCGIS_SERVICE_URL = "https://services.arcgis.com/NummVBqZSIJKUeVR/arcgis/rest/services/HeavyTrashProgress_view_layer/FeatureServer/0/query"

ATTR_STATUS = "status"
ATTR_DAYS_UNTIL_PICKUP = "days_until_pickup"
ATTR_LAST_UPDATE = "last_update"
ATTR_ROUTE = "route"

# ArcGIS REST API endpoints
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