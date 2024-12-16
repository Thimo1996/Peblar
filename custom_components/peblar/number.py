"""Home Assistant component for accessing the Peblar Portal API.

The number component allows control of charging current.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import cast

from homeassistant.components.number import NumberEntity, NumberEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import PlatformNotReady
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import CHARGER_MAX_CHARGING_CURRENT_KEY, CHARGER_SERIAL_NUMBER_KEY, DOMAIN
from .coordinator import InvalidAuth, PeblarCoordinator
from .entity import PeblarEntity


@dataclass(frozen=True, kw_only=True)
class PeblarNumberEntityDescription(NumberEntityDescription):
    """Describes Peblar number entity."""

    max_value_fn: Callable[[PeblarCoordinator], float]
    min_value_fn: Callable[[PeblarCoordinator], float]
    set_value_fn: Callable[[PeblarCoordinator], Callable[[float], Awaitable[None]]]


NUMBER_TYPES: dict[str, PeblarNumberEntityDescription] = {
    CHARGER_MAX_CHARGING_CURRENT_KEY: PeblarNumberEntityDescription(
        key=CHARGER_MAX_CHARGING_CURRENT_KEY,
        translation_key=CHARGER_MAX_CHARGING_CURRENT_KEY,
        max_value_fn=lambda _: 20000.0,
        min_value_fn=lambda _: 0.0,
        set_value_fn=lambda coordinator: coordinator.async_set_charging_current,
        native_step=1,
    ),
}


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Create Peblar number entities in HASS."""
    coordinator: PeblarCoordinator = hass.data[DOMAIN][entry.entry_id]
    # Check if the user has sufficient rights to change values, if so, add number component:
    try:
        await coordinator.async_set_charging_current(
            coordinator.data[CHARGER_MAX_CHARGING_CURRENT_KEY]
        )
    except InvalidAuth:
        return
    except ConnectionError as exc:
        raise PlatformNotReady from exc

    async_add_entities(
        PeblarNumber(coordinator, entry, description)
        for ent in coordinator.data
        if (description := NUMBER_TYPES.get(ent))
    )


class PeblarNumber(PeblarEntity, NumberEntity):
    """Representation of the Peblar."""

    entity_description: PeblarNumberEntityDescription

    def __init__(
        self,
        coordinator: PeblarCoordinator,
        entry: ConfigEntry,
        description: PeblarNumberEntityDescription,
    ) -> None:
        """Initialize a Peblar number entity."""
        super().__init__(coordinator)
        self.entity_description = description
        self._coordinator = coordinator
        self._attr_unique_id = (
            f"{description.key}-{coordinator.data[CHARGER_SERIAL_NUMBER_KEY]}"
        )

    @property
    def native_max_value(self) -> float:
        """Return the maximum available value."""
        return self.entity_description.max_value_fn(self.coordinator)

    @property
    def native_min_value(self) -> float:
        """Return the minimum available value."""
        return self.entity_description.min_value_fn(self.coordinator)

    @property
    def native_value(self) -> float | None:
        """Return the value of the entity."""
        return cast(float | None, self._coordinator.data[self.entity_description.key])

    async def async_set_native_value(self, value: float) -> None:
        """Set the value of the entity."""
        await self.entity_description.set_value_fn(self.coordinator)(value)
