"""Home Assistant component for accessing the Peblar Portal API. The sensor component creates multiple sensors regarding peblar performance."""

from __future__ import annotations

from dataclasses import dataclass
import logging
from datetime import datetime
from typing import cast

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfElectricCurrent, UnitOfEnergy, UnitOfPower
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from .const import (
    CHARGER_CHARGE_POWER_KEY,
    CHARGER_MAX_CHARGING_CURRENT_KEY,
    CHARGER_SERIAL_NUMBER_KEY,
    CHARGER_SESSION_ENERGY_KEY,
    CHARGER_TOTAL_ENERGY_KEY,
    DOMAIN,
)
from .coordinator import PeblarCoordinator
from .entity import PeblarEntity

UPDATE_INTERVAL = 30

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class PeblarSensorEntityDescription(SensorEntityDescription):
    """Describes Peblar sensor entity."""

    precision: int | None = None
    last_reset: datetime | None = None


SENSOR_TYPES: dict[str, PeblarSensorEntityDescription] = {
    CHARGER_MAX_CHARGING_CURRENT_KEY: PeblarSensorEntityDescription(
        key=CHARGER_MAX_CHARGING_CURRENT_KEY,
        translation_key=CHARGER_MAX_CHARGING_CURRENT_KEY,
        native_unit_of_measurement=UnitOfElectricCurrent.MILLIAMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    last_reset=datetime(2023, 1, 1, 0, 0, 0),  # Example last reset time
    CHARGER_TOTAL_ENERGY_KEY: PeblarSensorEntityDescription(
        key=CHARGER_TOTAL_ENERGY_KEY,
        translation_key=CHARGER_TOTAL_ENERGY_KEY,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    CHARGER_SESSION_ENERGY_KEY: PeblarSensorEntityDescription(
        key=CHARGER_SESSION_ENERGY_KEY,
        translation_key=CHARGER_SESSION_ENERGY_KEY,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    CHARGER_CHARGE_POWER_KEY: PeblarSensorEntityDescription(
        key=CHARGER_CHARGE_POWER_KEY,
        translation_key=CHARGER_CHARGE_POWER_KEY,
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
}


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Create Peblar sensor entities in HASS."""
    coordinator: PeblarCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        PeblarSensor(coordinator, description)
        for ent in coordinator.data
        if (description := SENSOR_TYPES.get(ent))
    )


class PeblarSensor(PeblarEntity, SensorEntity):
    """Representation of the Peblar portal."""

    entity_description: PeblarSensorEntityDescription

    def __init__(
        self,
        coordinator: PeblarCoordinator,
        description: PeblarSensorEntityDescription,
    ) -> None:
        """Initialize a Peblar sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = (
            f"{description.key}-{coordinator.data[CHARGER_SERIAL_NUMBER_KEY]}"
        )

    @property
    def last_reset(self) -> datetime | None:
        """Return the last reset time of the sensor."""
        return self.entity_description.last_reset
    def native_value(self) -> StateType:
        """Return the state of the sensor. Round the value when it, and the precision property are not None."""
        if (
            sensor_round := self.entity_description.precision
        ) is not None and self.coordinator.data[
            self.entity_description.key
        ] is not None:
            return cast(
                StateType,
                round(self.coordinator.data[self.entity_description.key], sensor_round),
            )
        return cast(StateType, self.coordinator.data[self.entity_description.key])