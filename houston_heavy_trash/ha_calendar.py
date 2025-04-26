"""Calendar platform for the Houston Heavy Trash integration."""
from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone

from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN, CONF_ROUTE
from .coordinator import HoustonHeavyTrashCoordinator

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the calendar platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([HoustonHeavyTrashCalendar(coordinator, entry)])

class HoustonHeavyTrashCalendar(CalendarEntity):
    """Calendar entity for Houston Heavy Trash."""

    def __init__(
        self,
        coordinator: HoustonHeavyTrashCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the calendar."""
        self._coordinator = coordinator
        self._entry = entry
        self._route = entry.data[CONF_ROUTE]
        self._attr_name = f"Heavy Trash Pickup Schedule"
        self._attr_unique_id = f"{entry.entry_id}-calendar"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._route)},
            name=f"Route: {self._route}",
            manufacturer="City of Houston",
            model="Heavy Trash Route",
        )

    @property
    def event(self) -> CalendarEvent | None:
        """Return the next upcoming event."""
        if not self._coordinator.data:
            return None

        status = self._coordinator.data["status"]
        now = datetime.now(timezone.utc)

        if status == "Completed":
            return None

        if status == "In Progress":
            # If in progress, create event for today
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end = start + timedelta(days=1)
            return CalendarEvent(
                start=start,
                end=end,
                summary=f"Heavy Trash Pickup - {self._route}",
                description="Heavy trash pickup is in progress today",
            )

        if status.startswith("Scheduled in"):
            # If scheduled for tomorrow
            start = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
            end = start + timedelta(days=1)
            return CalendarEvent(
                start=start,
                end=end,
                summary=f"Heavy Trash Pickup - {self._route}",
                description="Heavy trash pickup is scheduled for tomorrow",
            )

        if status == "1-3 Days":
            # If 1-3 days away, create event for 3 days from now
            start = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=3)
            end = start + timedelta(days=1)
            return CalendarEvent(
                start=start,
                end=end,
                summary=f"Heavy Trash Pickup - {self._route}",
                description="Heavy trash pickup is scheduled in 1-3 days",
            )

        if status == "4-7 Days":
            # If 4-7 days away, create event spanning those days
            start = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=4)
            end = start + timedelta(days=4)  # 4-7 days span
            return CalendarEvent(
                start=start,
                end=end,
                summary=f"Heavy Trash Pickup - {self._route}",
                description="Heavy trash pickup is scheduled in 4-7 days",
            )

        return None

    async def async_get_events(
        self,
        hass: HomeAssistant,
        start_date: datetime,
        end_date: datetime,
    ) -> list[CalendarEvent]:
        """Return calendar events within a datetime range."""
        event = self.event
        if not event:
            return []

        # Only return the event if it falls within the requested range
        if event.start <= end_date and event.end >= start_date:
            return [event]
        return []

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