"""Sensor platform for Houston Heavy Trash."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    CONF_NAME,
    CONF_ROUTE_ID,
    CONF_ROUTES,
    DEFAULT_NAME,
    DOMAIN,
    SENSOR_TYPES,
)
from .coordinator import HoustonHeavyTrashDataUpdateCoordinator

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Houston Heavy Trash sensors from a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []
    for route in entry.data[CONF_ROUTES]:
        for sensor_type in SENSOR_TYPES:
            entities.append(
                HoustonHeavyTrashSensor(
                    coordinator,
                    route[CONF_NAME],
                    route[CONF_ROUTE_ID],
                    sensor_type,
                )
            )

    async_add_entities(entities)

class HoustonHeavyTrashSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Houston Heavy Trash sensor."""

    def __init__(
        self,
        coordinator: HoustonHeavyTrashDataUpdateCoordinator,
        name: str,
        route_id: str,
        sensor_type: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._name = name
        self._route_id = route_id
        self._sensor_type = sensor_type
        self._attr_name = f"{name} {SENSOR_TYPES[sensor_type]['name']}"
        self._attr_unique_id = f"{route_id}_{sensor_type}"
        self._attr_icon = SENSOR_TYPES[sensor_type]["icon"]
        self._attr_device_class = None
        self._attr_native_unit_of_measurement = SENSOR_TYPES[sensor_type]["unit_of_measurement"]

    @property
    def native_value(self) -> Any:
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None

        route_data = self.coordinator.data.get(self._route_id)
        if not route_data:
            return None

        if self._sensor_type == "status":
            return self._calculate_status(route_data)
        elif self._sensor_type == "next_pickup":
            return self._get_next_pickup(route_data)
        elif self._sensor_type == "service_type":
            return route_data.get("SERVICE_TY")
        elif self._sensor_type == "service_week":
            return route_data.get("Service_WK")
        elif self._sensor_type == "service_day":
            return route_data.get("Day")
        elif self._sensor_type == "quadrant":
            return route_data.get("QUAD")

        return None

    def _calculate_status(self, attrs: dict) -> str:
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

    def _get_next_pickup(self, attrs: dict) -> str:
        """Get the next pickup date."""
        if attrs.get("ServicedDate"):
            service_date = datetime.fromtimestamp(attrs.get("ServicedDate")/1000, timezone.utc)
            return service_date.strftime("%Y-%m-%d")
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        if not self.coordinator.data:
            return {}

        route_data = self.coordinator.data.get(self._route_id)
        if not route_data:
            return {}

        return {
            "route_id": self._route_id,
            "service_week": route_data.get("Service_WK"),
            "service_day": route_data.get("Day"),
            "quadrant": route_data.get("QUAD"),
            "service_type": route_data.get("SERVICE_TY"),
            "last_update": datetime.now().isoformat(),
        } 