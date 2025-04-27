import logging
from datetime import datetime, time, timedelta
from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.util import dt as dt_util

from . import DOMAIN
from .coordinator import HoustonTrashDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
):
    """Set up the Houston Trash & Recycling calendars."""
    if discovery_info is None:
        return
    coordinator: HoustonTrashDataUpdateCoordinator = hass.data[DOMAIN]["coordinator"]

    cals = [
        HoustonTrashCalendar(coordinator),
        HoustonRecyclingCalendar(coordinator),
    ]
    add_entities(cals, True)


class BaseHoustonCalendar(CalendarEntity):
    """
    A multi-event calendar that shows all events within ~6 months
    that have a certain flag_name (e.g. 'waste' or 'recycle').
    """

    _flag_name = ""
    _attr_name = "Base Calendar"

    def __init__(self, coordinator: HoustonTrashDataUpdateCoordinator):
        self._coordinator = coordinator

    async def async_update(self):
        """Request a fresh poll if needed."""
        await self._coordinator.async_request_refresh()

    async def async_added_to_hass(self):
        """Listen for coordinator updates."""
        self.async_on_remove(
            self._coordinator.async_add_listener(self.async_write_ha_state)
        )

    @property
    def event(self) -> CalendarEvent | None:
        """
        Return the *next* upcoming event that matches our _flag_name.
        Home Assistant uses this to show a single “current” or “next” event.
        """
        events = self._filter_events()
        if not events:
            return None
        # Next event is the first in sorted order
        next_evt = events[0]
        return self._build_calendar_event(next_evt)

    async def async_get_events(self, hass, start_date, end_date):
        """
        Return all events matching our _flag_name that fall within the requested date range.
        This is how the HA Calendar UI can show the schedule over days/weeks.
        """
        matched = []
        for evt in self._filter_events():
            c_evt = self._build_calendar_event(evt)
            if not c_evt:
                continue
            if c_evt.start < end_date and c_evt.end > start_date:
                matched.append(c_evt)
        return matched

    def _filter_events(self):
        """Return all events that have a flag 'name' == self._flag_name, sorted by day."""
        data = self._coordinator.data
        if not data:
            return []
        all_events = data.get("events", [])
        # Filter
        relevant = []
        for e in all_events:
            day_str = e.get("day")
            if not day_str:
                continue
            # if any flag has name == _flag_name, we consider this event
            for f in e.get("flags", []):
                if f.get("name") == self._flag_name:
                    relevant.append(e)
                    break
        # Sort by day ascending
        relevant.sort(key=lambda e: e["day"])
        return relevant

    def _build_calendar_event(self, evt) -> CalendarEvent | None:
        """Convert a single event dict to a CalendarEvent object with a 1-hour duration."""
        day_str = evt.get("day")
        if not day_str:
            return None

        # parse "YYYY-MM-DD" -> datetime
        day_date = dt_util.parse_date(day_str)
        if not day_date:
            return None

        local_tz = dt_util.get_time_zone(self._coordinator.hass.config.time_zone)
        start_dt = datetime.combine(day_date, time(0, 0), local_tz)
        end_dt = start_dt + timedelta(hours=1)

        # Build a summary from each matching flag's subject
        subjects = []
        for f in evt["flags"]:
            if f.get("name") == self._flag_name:
                subjects.append(f.get("subject", "Pickup"))
        summary = " & ".join(subjects) if subjects else "Pickup"

        return CalendarEvent(
            start=start_dt,
            end=end_dt,
            summary=summary,
        )


class HoustonTrashCalendar(BaseHoustonCalendar):
    _flag_name = "waste"
    _attr_name = "Houston Trash Pickup Calendar"


class HoustonRecyclingCalendar(BaseHoustonCalendar):
    _flag_name = "recycle"
    _attr_name = "Houston Recycling Pickup Calendar"
