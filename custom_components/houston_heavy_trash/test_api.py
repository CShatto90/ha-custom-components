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

async def test_endpoint():
    """Test the ArcGIS endpoint and explore available data."""
    print(f"Testing Heavy Trash Progress endpoint for route: {TEST_ROUTE}")
    print(f"API URL: {ARCGIS_SERVICE_URL}")
    
    # First, get all available fields
    fields_params = {
        "f": "json"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            # Get layer information
            async with session.get(ARCGIS_SERVICE_URL.replace("/query", ""), params=fields_params) as response:
                if response.status == 200:
                    layer_info = await response.json()
                    print("\nAvailable Fields:")
                    for field in layer_info.get("fields", []):
                        print(f"- {field['name']} ({field['type']}): {field.get('alias', 'No description')}")
                
            # Now get data for our route
            query_params = {
                "where": f"NAME LIKE '%{TEST_ROUTE}%'",
                "outFields": "*",  # Get all fields
                "returnGeometry": "false",
                "f": "json"
            }
            
            print(f"\nQuery parameters: {json.dumps(query_params, indent=2)}")
            
            async with session.get(ARCGIS_SERVICE_URL, params=query_params) as response:
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
                
                # Print all available information for the route
                for feature in data["features"]:
                    attrs = feature["attributes"]
                    status = calculate_status(attrs)
                    
                    print("\nRoute Information:")
                    print(f"Status: {status}")
                    for key, value in attrs.items():
                        if isinstance(value, (int, float)) and key.endswith("Date"):
                            # Convert timestamp to readable date
                            try:
                                value = datetime.fromtimestamp(value/1000).strftime('%Y-%m-%d')
                            except:
                                pass
                        print(f"{key}: {value}")
                    print("-" * 50)
                
    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_endpoint()) 