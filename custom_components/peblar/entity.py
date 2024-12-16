"""Base entity for the peblar integration."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CHARGER_PART_NUMBER_KEY, CHARGER_SERIAL_NUMBER_KEY, DOMAIN
from .coordinator import PeblarCoordinator


class PeblarEntity(CoordinatorEntity[PeblarCoordinator]):
    """Defines a base Peblar entity."""

    _attr_has_entity_name = True

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information about this Peblar device."""
        return DeviceInfo(
            identifiers={
                (
                    DOMAIN,
                    self.coordinator.data[CHARGER_SERIAL_NUMBER_KEY],
                )
            },
            name="Peblar",
            manufacturer="Peblar",
            model_id=self.coordinator.data[CHARGER_PART_NUMBER_KEY],
        )
