"""Test script for Houston Heavy Trash API."""
import asyncio
import aiohttp
import json
from datetime import datetime, timezone

# Test route - you can change this to test different routes
TEST_ROUTE = "NE4TH_08"

# ArcGIS REST API endpoint
ARCGIS_SERVICE_URL = "https://services.arcgis.com/NummVBqZSIJKUeVR/arcgis/rest/services/HeavyTrashProgress_view_layer/FeatureServer/0/query"

def calculate_status(attrs):
    """Calculate the status based on the attributes."""
    now = datetime.now(timezone.utc)
    
    if attrs.get("ServiceCompleted") == "Yes":
        return "Completed"
    
    if attrs.get("ServicedToday") == "Yes":
        return "In Progress"
        
    if attrs.get("ServicedTomorrow") == "Yes":
        tomorrow_date = datetime.fromtimestamp(attrs.get("TomorrowServiceDate")/1000, timezone.utc)
        days_until = (tomorrow_date - now).days
        return f"Scheduled in {days_until} days"
    
    if attrs.get("ServicedDate"):
        service_date = datetime.fromtimestamp(attrs.get("ServicedDate")/1000, timezone.utc)
        days_until = (service_date - now).days
        if days_until <= 3:
            return "1-3 Days"
        elif days_until <= 7:
            return "4-7 Days"
        else:
            return "8+ Days"
            
    return "Unknown"

# Query parameters
ARCGIS_QUERY_PARAMS = {
    "where": "NAME LIKE '%{}%'".format(TEST_ROUTE),  # Search for specific route
    "outFields": "NAME,ServicedToday,ServicedTomorrow,ServicedDate,TomorrowServiceDate,ServiceCompleted,CompletedDate,SERVICE_TY",
    "returnGeometry": "false",
    "f": "json"
}

async def test_endpoint():
    """Test the ArcGIS endpoint."""
    print(f"Testing Heavy Trash Progress endpoint for route: {TEST_ROUTE}")
    print(f"API URL: {ARCGIS_SERVICE_URL}")
    print(f"Query parameters: {json.dumps(ARCGIS_QUERY_PARAMS, indent=2)}")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(ARCGIS_SERVICE_URL, params=ARCGIS_QUERY_PARAMS) as response:
                print(f"\nResponse Status: {response.status}")
                
                if response.status != 200:
                    print(f"Error: {response.status}")
                    return
                
                data = await response.json()
                
                if "error" in data:
                    print(f"\nAPI Error: {data['error']}")
                    return
                
                if not data.get("features"):
                    print(f"\nNo data found for route: {TEST_ROUTE}")
                    return
                
                # Print information for the route
                for feature in data["features"]:
                    attrs = feature["attributes"]
                    status = calculate_status(attrs)
                    
                    print("\nRoute Information:")
                    print(f"Name: {attrs.get('NAME')}")
                    print(f"Service Type: {attrs.get('SERVICE_TY')}")
                    print(f"Current Status: {status}")
                    print(f"Serviced Today: {attrs.get('ServicedToday')}")
                    print(f"Serviced Tomorrow: {attrs.get('ServicedTomorrow')}")
                    
                    if attrs.get("ServicedDate"):
                        print(f"Service Date: {datetime.fromtimestamp(attrs.get('ServicedDate')/1000).strftime('%Y-%m-%d')}")
                    
                    if attrs.get("TomorrowServiceDate"):
                        print(f"Tomorrow Service Date: {datetime.fromtimestamp(attrs.get('TomorrowServiceDate')/1000).strftime('%Y-%m-%d')}")
                    
                    if attrs.get("ServiceCompleted") == "Yes":
                        print(f"Completed Date: {datetime.fromtimestamp(attrs.get('CompletedDate')/1000).strftime('%Y-%m-%d')}")
                    
                    print("-" * 50)
                
    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_endpoint()) 