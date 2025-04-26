import logging
import requests
from bs4 import BeautifulSoup

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntity
from homeassistant.const import CONF_NAME
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

DOMAIN = "houston_incidents"
DEFAULT_NAME = "Houston Active Incidents"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
})

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Houston Incidents from a config entry."""
    name = config_entry.data.get(CONF_NAME, DEFAULT_NAME)
    async_add_entities([HoustonActiveIncidentsSensor(name)], True)

async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the sensor platform (legacy)."""
    name = config.get(CONF_NAME, DEFAULT_NAME)
    async_add_entities([HoustonActiveIncidentsSensor(name)], True)

class HoustonActiveIncidentsSensor(SensorEntity):
    """Sensor that scrapes the Houston Active Incidents page."""

    def __init__(self, name):
        """Initialize the sensor."""
        self._name = name
        self._state = None
        self._attributes = {}
        self._incidents = []

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def icon(self):
        """Return an appropriate icon."""
        return "mdi:fire-truck"

    @property
    def state(self):
        """Return the state (total incidents)."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return the sensor attributes."""
        return self._attributes

    async def async_update(self):
        """Fetch and parse the data from the Houston Active Incidents page."""
        url = "https://cohweb.houstontx.gov/ActiveIncidents/Combined.aspx"

        try:
            response = await self.hass.async_add_executor_job(
                requests.get, url, {"timeout": 30}
            )
            if response.status_code != 200:
                _LOGGER.warning("Got non-200 status code: %s", response.status_code)
                return

            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.find("table", {"id": "GridView2"})
            if not table:
                _LOGGER.error("Could not find incidents table in HTML.")
                return

            rows = table.find_all("tr")
            data_rows = rows[1:]  # skip header row

            incidents = []
            fd_count = 0
            pd_count = 0

            for row in data_rows:
                cols = row.find_all("td")
                if len(cols) < 7:
                    continue

                agency = cols[0].get_text(strip=True)
                address = cols[1].get_text(strip=True)
                cross_street = cols[2].get_text(strip=True)
                key_map = cols[3].get_text(strip=True)
                call_time_opened = cols[4].get_text(strip=True)
                incident_type = cols[5].get_text(strip=True)
                combined_response = cols[6].get_text(strip=True)

                if agency.upper() == "FD":
                    fd_count += 1
                elif agency.upper() == "PD":
                    pd_count += 1

                incident = {
                    "agency": agency,
                    "address": address,
                    "cross_street": cross_street,
                    "key_map": key_map,
                    "call_time_opened": call_time_opened,
                    "incident_type": incident_type,
                    "combined_response": combined_response,
                }
                incidents.append(incident)

            total_incidents = len(incidents)
            self._state = total_incidents
            self._attributes = {
                "fd_incidents": fd_count,
                "pd_incidents": pd_count,
                "incidents": incidents,
            }

        except Exception as e:
            _LOGGER.error("Error updating Houston Active Incidents: %s", e)
