import logging
from typing import Any, Optional

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from . import DOMAIN
from .coordinator import HoustonTrashDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
):
    """Set up the Houston Trash sensors via YAML discovery."""
    if discovery_info is None:
        return
    coordinator: HoustonTrashDataUpdateCoordinator = hass.data[DOMAIN]["coordinator"]

    sensors = [
        HoustonTrashNextPickupSensor(coordinator),
        HoustonRecyclingNextPickupSensor(coordinator),
    ]
    add_entities(sensors, True)


def find_earliest_event(events, flag_name: str):
    """
    Return the earliest event whose flags contain { name: flag_name }.
    Sort by event['day'] ascending. If none found, return None.
    """
    # Filter only events that have day != None
    valid_events = [e for e in events if e.get("day")]
    # Sort by day
    valid_events.sort(key=lambda e: e["day"])
    for evt in valid_events:
        for f in evt.get("flags", []):
            if f.get("name") == flag_name:
                return evt
    return None


class BasePickupSensor(SensorEntity):
    """Base class for a 'next pickup' sensor for a certain flag_name (e.g. 'waste', 'recycle')."""

    _flag_name = ""
    _attr_icon = "mdi:delete-circle"

    def __init__(self, coordinator: HoustonTrashDataUpdateCoordinator):
        self._coordinator = coordinator

    @property
    def native_value(self) -> Optional[str]:
        """Earliest date for an event matching our _flag_name (e.g. 'waste')."""
        data = self._coordinator.data
        if not data:
            return None
        all_events = data.get("events", [])
        match = find_earliest_event(all_events, self._flag_name)
        if not match:
            return None
        return match["day"]

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """
        Return details: 'delayed', 'message', 'zone_name', etc. from the matched flag/event.
        If multiple flags in the same event match, we just pick the first found.
        """
        data = self._coordinator.data
        if not data:
            return {}
        match = find_earliest_event(data.get("events", []), self._flag_name)
        if not match:
            return {}

        # Find the first flag that matches
        for f in match["flags"]:
            if f.get("name") == self._flag_name:
                return {
                    "delayed": f["delayed"],
                    "message": f["message"],
                    "zone_name": match.get("zone_name"),
                    "zone_title": match.get("zone_title"),
                }
        return {}

    async def async_update(self):
        """Request data update from coordinator if needed."""
        await self._coordinator.async_request_refresh()

    async def async_added_to_hass(self):
        """Listen for coordinator updates."""
        self.async_on_remove(
            self._coordinator.async_add_listener(self.async_write_ha_state)
        )


class HoustonTrashNextPickupSensor(BasePickupSensor):
    _attr_name = "Houston Trash Next Pickup"
    _attr_icon = "mdi:delete-circle"
    _flag_name = "waste"

    @property
    def unique_id(self):
        return "houston_trash_next_pickup"


class HoustonRecyclingNextPickupSensor(BasePickupSensor):
    _attr_name = "Houston Recycling Next Pickup"
    _attr_icon = "mdi:recycle"
    _flag_name = "recycle"

    @property
    def unique_id(self):
        return "houston_recycling_next_pickup"
