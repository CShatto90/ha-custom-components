"""Data update coordinator for Houston Heavy Trash."""
from __future__ import annotations

import aiohttp
import logging
from datetime import datetime, timezone
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    CONF_ROUTE_ID,
    CONF_ROUTES,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    ARCGIS_SERVICE_URL,
)

_LOGGER = logging.getLogger(__name__)

class HoustonHeavyTrashDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the ArcGIS API."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=DEFAULT_SCAN_INTERVAL,
        )
        self._entry = entry
        self._routes = entry.data[CONF_ROUTES]

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from the ArcGIS REST API."""
        try:
            async with aiohttp.ClientSession() as session:
                # Get data for all configured routes
                route_data = {}
                for route in self._routes:
                    route_id = route[CONF_ROUTE_ID]
                    query_params = {
                        "where": f"NAME LIKE '%{route_id}%'",
                        "outFields": "*",
                        "returnGeometry": "false",
                        "f": "json"
                    }
                    
                    async with session.get(ARCGIS_SERVICE_URL, params=query_params) as response:
                        if response.status != 200:
                            _LOGGER.error("Error fetching data for route %s: %s", route_id, response.status)
                            continue
                        
                        data = await response.json()
                        
                        if "error" in data:
                            _LOGGER.error("ArcGIS API error for route %s: %s", route_id, data["error"])
                            continue
                        
                        if not data.get("features"):
                            _LOGGER.warning("No data found for route: %s", route_id)
                            continue
                        
                        # Get the first feature (should only be one for a specific route)
                        feature = data["features"][0]
                        route_data[route_id] = feature["attributes"]
                
                if not route_data:
                    raise UpdateFailed("No data received for any routes")
                
                return route_data
                
        except Exception as err:
            _LOGGER.error("Error communicating with ArcGIS API: %s", err)
            raise UpdateFailed(f"Error communicating with API: {err}") 