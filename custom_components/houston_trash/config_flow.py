"""Config flow for Houston Trash."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN, CONF_BASE_URL

CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_BASE_URL): str,
    }
)

async def validate_config(hass: HomeAssistant, data: dict) -> None:
    """Validate the configuration."""
    if not isinstance(data.get(CONF_BASE_URL), str) or not data[CONF_BASE_URL].strip():
        raise ValueError("Base URL is required")
    
    # Basic URL validation
    if not data[CONF_BASE_URL].startswith(("http://", "https://")):
        raise ValueError("Base URL must start with http:// or https://")

class HoustonTrashConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Houston Trash."""

    VERSION = 1

    async def async_step_user(self, user_input: dict | None = None) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=CONFIG_SCHEMA,
            )

        try:
            await validate_config(self.hass, user_input)
        except ValueError as err:
            return self.async_show_form(
                step_id="user",
                data_schema=CONFIG_SCHEMA,
                errors={"base": str(err)},
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
                        CONF_BASE_URL,
                        default=self.config_entry.data.get(CONF_BASE_URL),
                    ): str,
                }
            ),
        ) 