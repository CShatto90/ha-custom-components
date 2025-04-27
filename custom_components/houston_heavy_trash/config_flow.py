"""Config flow for Houston Heavy Trash."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN, DASHBOARD_URL

CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required("routes"): [
            {
                vol.Required("name"): str,
                vol.Required("route_id"): str,
            }
        ]
    }
)

async def validate_config(hass: HomeAssistant, data: dict) -> None:
    """Validate the configuration."""
    if not isinstance(data.get("routes"), list):
        raise ValueError("Routes must be a list")
    
    for route in data["routes"]:
        if not isinstance(route.get("name"), str) or not route["name"].strip():
            raise ValueError("Route name is required")
        if not isinstance(route.get("route_id"), str) or not route["route_id"].strip():
            raise ValueError("Route ID is required")

class HoustonHeavyTrashConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Houston Heavy Trash."""

    VERSION = 1

    async def async_step_user(self, user_input: dict | None = None) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=CONFIG_SCHEMA,
                description_placeholders={
                    "dashboard_url": DASHBOARD_URL,
                },
            )

        try:
            await validate_config(self.hass, user_input)
        except ValueError as err:
            return self.async_show_form(
                step_id="user",
                data_schema=CONFIG_SCHEMA,
                errors={"base": str(err)},
                description_placeholders={
                    "dashboard_url": DASHBOARD_URL,
                },
            )

        return self.async_create_entry(title="Houston Heavy Trash", data=user_input)

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Create the options flow."""
        return HoustonHeavyTrashOptionsFlow(config_entry)

class HoustonHeavyTrashOptionsFlow(config_entries.OptionsFlow):
    """Handle options."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        "routes",
                        default=[route for route in self.config_entry.data.get("routes", [])],
                    ): [
                        {
                            vol.Required("name"): str,
                            vol.Required("route_id"): str,
                        }
                    ],
                }
            ),
            description_placeholders={
                "dashboard_url": DASHBOARD_URL,
            },
        ) 