"""DataUpdateCoordinator for the peblar integration."""

from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

import requests

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import (
    CHARGER_CP_STATE_DESCRIPTION_KEY,
    CHARGER_CP_STATE_KEY,
    DOMAIN,
    UPDATE_INTERVAL,
    ChargerStatus,
)

from .peblar import Peblar

_LOGGER = logging.getLogger(__name__)

CHARGER_STATUS: dict[str, ChargerStatus] = {
    "State A": "No EV connected",
    "State B": "EV connected but suspended",
    "State C": "EV connected and charging",
    "State D": "Same as C but ventilation requested",
    "State E": "Error, short to PE or powered off",
    "State F": "Fault",
    "State I": "Invalid CP level measured",
    "State U": "Unknown",
}


def _validate(peblar: Peblar) -> None:
    """Authenticate using Peblar API."""
    try:
        peblar.authenticate()
    except requests.exceptions.HTTPError as peblar_connection_error:
        if peblar_connection_error.response.status_code == 401:
            raise InvalidAuth from peblar_connection_error
        raise ConnectionError from peblar_connection_error


async def async_validate_input(hass: HomeAssistant, peblar: Peblar) -> None:
    """Get new sensor data for Peblar component."""
    await hass.async_add_executor_job(_validate, peblar)


class PeblarCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Peblar Coordinator class."""

    def __init__(self, peblar: Peblar, hass: HomeAssistant) -> None:
        """Initialize."""
        self._peblar = peblar

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )

    def authenticate(self) -> None:
        """Authenticate using Peblar API."""
        self._peblar.authenticate()

    def _get_data(self) -> dict[str, Any]:
        """Get new sensor data for Peblar component."""
        data: dict[str, Any] = self._peblar.getChargerData()
        data[CHARGER_CP_STATE_DESCRIPTION_KEY] = CHARGER_STATUS.get(
            data[CHARGER_CP_STATE_KEY], ChargerStatus.UNKNOWN
        )
        return data

    async def _async_update_data(self) -> dict[str, Any]:
        """Get new sensor data for Peblar component."""
        return await self.hass.async_add_executor_job(self._get_data)

    def _set_charging_current(self, charging_current: float) -> None:
        """Set maximum charging current for Peblar."""
        try:
            self._peblar.setMaxChargingCurrent(charging_current)
        except requests.exceptions.HTTPError as peblar_connection_error:
            if peblar_connection_error.response.status_code == 403:
                raise InvalidAuth from peblar_connection_error
            raise

    async def async_set_charging_current(self, charging_current: float) -> None:
        """Set maximum charging current for Peblar."""
        await self.hass.async_add_executor_job(
            self._set_charging_current, charging_current
        )
        await self.async_request_refresh()


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
