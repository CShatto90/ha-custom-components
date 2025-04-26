"""Config flow for Houston Trash."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN, CONF_ROUTES, CONF_NAME, CONF_ROUTE_ID, DASHBOARD_URL

CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ROUTES): [
            {
                vol.Required(CONF_NAME): str,
                vol.Required(CONF_ROUTE_ID): str,
            }
        ]
    }
)

async def validate_config(hass: HomeAssistant, data: dict) -> None:
    """Validate the configuration."""
    if not isinstance(data.get(CONF_ROUTES), list):
        raise ValueError("Routes must be a list")
    
    for route in data[CONF_ROUTES]:
        if not isinstance(route.get(CONF_NAME), str) or not route[CONF_NAME].strip():
            raise ValueError("Route name is required")
        if not isinstance(route.get(CONF_ROUTE_ID), str) or not route[CONF_ROUTE_ID].strip():
            raise ValueError("Route ID is required")

class HoustonTrashConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Houston Trash."""

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

        return self.async_create_entry(title="Houston Trash", data=user_input)

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Create the options flow."""
        return HoustonTrashOptionsFlow(config_entry)

class HoustonTrashOptionsFlow(config_entries.OptionsFlow):
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
                        CONF_ROUTES,
                        default=[route for route in self.config_entry.data.get(CONF_ROUTES, [])],
                    ): [
                        {
                            vol.Required(CONF_NAME): str,
                            vol.Required(CONF_ROUTE_ID): str,
                        }
                    ],
                }
            ),
            description_placeholders={
                "dashboard_url": DASHBOARD_URL,
            },
        ) 