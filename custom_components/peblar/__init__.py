"""The Peblar integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ACCESS_TOKEN, CONF_IP_ADDRESS, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed

from .const import DOMAIN, UPDATE_INTERVAL
from .coordinator import InvalidAuth, PeblarCoordinator, async_validate_input
from .peblar import Peblar

PLATFORMS = [Platform.NUMBER, Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Peblar from a config entry."""
    peblar = Peblar(
        entry.data[CONF_ACCESS_TOKEN],
        entry.data[CONF_IP_ADDRESS],
    )
    try:
        await async_validate_input(hass, peblar)
    except InvalidAuth as ex:
        raise ConfigEntryAuthFailed from ex

    peblar_coordinator = PeblarCoordinator(
        peblar,
        hass,
    )
    await peblar_coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = peblar_coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
