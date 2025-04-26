"""Sensor platform for the Houston Heavy Trash integration."""
from __future__ import annotations

import aiohttp
import logging
from datetime import datetime, timezone

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.entity import DeviceInfo

from .const import (
    ATTR_DAYS_UNTIL_PICKUP,
    ATTR_LAST_UPDATE,
    ATTR_ROUTE,
    ATTR_STATUS,
    CONF_ROUTE,
    DOMAIN,
    ARCGIS_SERVICE_URL,
    SCAN_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator = HoustonHeavyTrashCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    
    # Create all sensors for this route
    entities = [
        HoustonHeavyTrashStatusSensor(coordinator, entry),
        HoustonHeavyTrashServiceTypeSensor(coordinator, entry),
        HoustonHeavyTrashServicedTodaySensor(coordinator, entry),
        HoustonHeavyTrashServicedTomorrowSensor(coordinator, entry),
        HoustonHeavyTrashServiceDateSensor(coordinator, entry),
        HoustonHeavyTrashTomorrowServiceDateSensor(coordinator, entry),
        HoustonHeavyTrashServiceCompletedSensor(coordinator, entry),
        HoustonHeavyTrashCompletedDateSensor(coordinator, entry),
    ]
    
    async_add_entities(entities)

class HoustonHeavyTrashCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the ArcGIS dashboard."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=SCAN_INTERVAL),
        )
        self._entry = entry
        self._route = entry.data[CONF_ROUTE]

    async def _async_update_data(self):
        """Fetch data from the ArcGIS REST API."""
        try:
            async with aiohttp.ClientSession() as session:
                # Add route filter to query parameters
                query_params = {
                    "where": f"NAME LIKE '%{self._route}%'",
                    "outFields": "NAME,ServicedToday,ServicedTomorrow,ServicedDate,TomorrowServiceDate,ServiceCompleted,CompletedDate,SERVICE_TY",
                    "returnGeometry": "false",
                    "f": "json"
                }
                
                async with session.get(ARCGIS_SERVICE_URL, params=query_params) as response:
                    if response.status != 200:
                        raise UpdateFailed(f"Error fetching data: {response.status}")
                    
                    data = await response.json()
                    
                    if "error" in data:
                        raise UpdateFailed(f"ArcGIS API error: {data['error']}")
                    
                    if not data.get("features"):
                        return {
                            "status": "Unknown",
                            "service_type": "Unknown",
                            "serviced_today": "No",
                            "serviced_tomorrow": "No",
                            "service_date": None,
                            "tomorrow_service_date": None,
                            "service_completed": "No",
                            "completed_date": None,
                            "last_update": datetime.now(timezone.utc).isoformat(),
                        }
                    
                    # Get the first feature (should only be one for a specific route)
                    feature = data["features"][0]
                    attributes = feature["attributes"]
                    
                    return {
                        "status": self._calculate_status(attributes),
                        "service_type": attributes.get("SERVICE_TY", "Unknown"),
                        "serviced_today": attributes.get("ServicedToday", "No"),
                        "serviced_tomorrow": attributes.get("ServicedTomorrow", "No"),
                        "service_date": attributes.get("ServicedDate"),
                        "tomorrow_service_date": attributes.get("TomorrowServiceDate"),
                        "service_completed": attributes.get("ServiceCompleted", "No"),
                        "completed_date": attributes.get("CompletedDate"),
                        "last_update": datetime.now(timezone.utc).isoformat(),
                    }
                    
        except Exception as err:
            _LOGGER.error("Error communicating with ArcGIS API: %s", err)
            raise UpdateFailed(f"Error communicating with API: {err}")

    def _calculate_status(self, attrs):
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

class HoustonHeavyTrashBaseSensor(SensorEntity):
    """Base class for Houston Heavy Trash sensors."""

    def __init__(
        self,
        coordinator: HoustonHeavyTrashCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        self._coordinator = coordinator
        self._entry = entry
        self._route = entry.data[CONF_ROUTE]
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._route)},
            name=f"Route: {self._route}",
            manufacturer="City of Houston",
            model="Heavy Trash Route",
        )

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self._coordinator.last_update_success

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await super().async_added_to_hass()
        self._coordinator.async_add_listener(self.async_write_ha_state)

    async def async_will_remove_from_hass(self) -> None:
        """When entity will be removed from hass."""
        self._coordinator.async_remove_listener(self.async_write_ha_state)
        await super().async_will_remove_from_hass()

    async def async_update(self) -> None:
        """Update the entity."""
        await self._coordinator.async_request_refresh()

class HoustonHeavyTrashStatusSensor(HoustonHeavyTrashBaseSensor):
    """Status sensor for Houston Heavy Trash."""

    def __init__(self, coordinator, entry):
        """Initialize the status sensor."""
        super().__init__(coordinator, entry)
        self._attr_name = f"Heavy Trash Status"
        self._attr_unique_id = f"{entry.entry_id}-status"
        self._attr_icon = "mdi:trash-can"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return self._coordinator.data["status"]

class HoustonHeavyTrashServiceTypeSensor(HoustonHeavyTrashBaseSensor):
    """Service Type sensor for Houston Heavy Trash."""

    def __init__(self, coordinator, entry):
        """Initialize the service type sensor."""
        super().__init__(coordinator, entry)
        self._attr_name = f"Heavy Trash Service Type"
        self._attr_unique_id = f"{entry.entry_id}-service-type"
        self._attr_icon = "mdi:information"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return self._coordinator.data["service_type"]

class HoustonHeavyTrashServicedTodaySensor(HoustonHeavyTrashBaseSensor):
    """Serviced Today sensor for Houston Heavy Trash."""

    def __init__(self, coordinator, entry):
        """Initialize the serviced today sensor."""
        super().__init__(coordinator, entry)
        self._attr_name = f"Heavy Trash Serviced Today"
        self._attr_unique_id = f"{entry.entry_id}-serviced-today"
        self._attr_icon = "mdi:calendar-today"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return self._coordinator.data["serviced_today"]

class HoustonHeavyTrashServicedTomorrowSensor(HoustonHeavyTrashBaseSensor):
    """Serviced Tomorrow sensor for Houston Heavy Trash."""

    def __init__(self, coordinator, entry):
        """Initialize the serviced tomorrow sensor."""
        super().__init__(coordinator, entry)
        self._attr_name = f"Heavy Trash Serviced Tomorrow"
        self._attr_unique_id = f"{entry.entry_id}-serviced-tomorrow"
        self._attr_icon = "mdi:calendar-arrow-right"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return self._coordinator.data["serviced_tomorrow"]

class HoustonHeavyTrashServiceDateSensor(HoustonHeavyTrashBaseSensor):
    """Service Date sensor for Houston Heavy Trash."""

    def __init__(self, coordinator, entry):
        """Initialize the service date sensor."""
        super().__init__(coordinator, entry)
        self._attr_name = f"Heavy Trash Service Date"
        self._attr_unique_id = f"{entry.entry_id}-service-date"
        self._attr_icon = "mdi:calendar"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        if date := self._coordinator.data["service_date"]:
            return datetime.fromtimestamp(date/1000).strftime('%Y-%m-%d')
        return "Unknown"

class HoustonHeavyTrashTomorrowServiceDateSensor(HoustonHeavyTrashBaseSensor):
    """Tomorrow Service Date sensor for Houston Heavy Trash."""

    def __init__(self, coordinator, entry):
        """Initialize the tomorrow service date sensor."""
        super().__init__(coordinator, entry)
        self._attr_name = f"Heavy Trash Tomorrow Service Date"
        self._attr_unique_id = f"{entry.entry_id}-tomorrow-service-date"
        self._attr_icon = "mdi:calendar-arrow-right"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        if date := self._coordinator.data["tomorrow_service_date"]:
            return datetime.fromtimestamp(date/1000).strftime('%Y-%m-%d')
        return "Unknown"

class HoustonHeavyTrashServiceCompletedSensor(HoustonHeavyTrashBaseSensor):
    """Service Completed sensor for Houston Heavy Trash."""

    def __init__(self, coordinator, entry):
        """Initialize the service completed sensor."""
        super().__init__(coordinator, entry)
        self._attr_name = f"Heavy Trash Service Completed"
        self._attr_unique_id = f"{entry.entry_id}-service-completed"
        self._attr_icon = "mdi:check-circle"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return self._coordinator.data["service_completed"]

class HoustonHeavyTrashCompletedDateSensor(HoustonHeavyTrashBaseSensor):
    """Completed Date sensor for Houston Heavy Trash."""

    def __init__(self, coordinator, entry):
        """Initialize the completed date sensor."""
        super().__init__(coordinator, entry)
        self._attr_name = f"Heavy Trash Completed Date"
        self._attr_unique_id = f"{entry.entry_id}-completed-date"
        self._attr_icon = "mdi:calendar-check"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        if date := self._coordinator.data["completed_date"]:
            return datetime.fromtimestamp(date/1000).strftime('%Y-%m-%d')
        return "Unknown" 