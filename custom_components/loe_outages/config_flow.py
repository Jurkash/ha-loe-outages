"""Config flow for Loe Outages integration."""

import logging
from typing import Any

import voluptuous as vol
from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
)
from homeassistant.core import callback
from homeassistant.helpers.selector import selector

from .const import CONF_GROUP, DEFAULT_GROUP, DOMAIN

_LOGGER = logging.getLogger(__name__)


def get_config_value(
    entry: ConfigEntry | None,
    key: str,
    default: Any = None,
) -> any:
    """Get a value from the config entry or default."""
    if entry is not None:
        return entry.options.get(key, entry.data.get(key, default))
    return default


def build_schema(config_entry: ConfigEntry) -> vol.Schema:
    """Build the schema for the config flow."""
    return vol.Schema(
        {
            vol.Required(
                CONF_GROUP,
                default=get_config_value(config_entry, CONF_GROUP, DEFAULT_GROUP),
            ): selector(
                {
                    "select": {
                        "options": [
                            {"value": f"{i}.{j}", "label": f"Group {i}.{j}"}
                            for i in range(1, 7)  # 1-6
                            for j in range(1, 3)  # 1-2
                        ],
                    },
                },
            ),
        },
    )


class LoeOutagesOptionsFlow(OptionsFlow):
    """Handle options flow for Loe Outages."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input: dict | None = None) -> ConfigFlowResult:
        """Manage the options."""
        if user_input is not None:
            _LOGGER.debug("Updating options: %s", user_input)
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=build_schema(config_entry=self.config_entry),
        )


class LoeOutagesConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Loe Outages."""

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> LoeOutagesOptionsFlow:
        """Get the options flow for this handler."""
        return LoeOutagesOptionsFlow(config_entry)

    async def async_step_user(self, user_input: dict | None = None) -> ConfigFlowResult:
        """Handle the initial step."""
        if user_input is not None:
            _LOGGER.debug("User input: %s", user_input)
            return self.async_create_entry(title="Loe Outages", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=build_schema(config_entry=None),
        )
