"""Config flow for Peblar integration."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import SOURCE_REAUTH, ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_ACCESS_TOKEN, CONF_IP_ADDRESS
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import InvalidAuth, async_validate_input
from .peblar import Peblar

COMPONENT_DOMAIN = DOMAIN

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_IP_ADDRESS): str,
        vol.Required(CONF_ACCESS_TOKEN): str,
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, str]:
    """Validate the user input allows to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    peblar = Peblar(data["access_token"], data["ip_address"])

    await async_validate_input(hass, peblar)

    # Return info that you want to store in the config entry.
    return {"title": "peblar"}


class peblarConfigFlow(ConfigFlow, domain=COMPONENT_DOMAIN):
    """Handle a config flow for peblar."""

    async def async_step_reauth(
        self, entry_data: Mapping[str, Any]
    ) -> ConfigFlowResult:
        """Perform reauth upon an API authentication error."""
        return await self.async_step_user()

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=STEP_USER_DATA_SCHEMA,
            )

        errors = {}

        try:
            await self.async_set_unique_id(user_input["ip_address"])
            if self.source != SOURCE_REAUTH:
                self._abort_if_unique_id_configured()
                info = await validate_input(self.hass, user_input)
                return self.async_create_entry(title=info["title"], data=user_input)
            reauth_entry = self._get_reauth_entry()
            if user_input["ip_address"] == reauth_entry.data["ip_address"]:
                return self.async_update_reload_and_abort(reauth_entry, data=user_input)
            errors["base"] = "reauth_invalid"
        except ConnectionError:
            errors["base"] = "cannot_connect"
        except InvalidAuth:
            errors["base"] = "invalid_auth"

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )
