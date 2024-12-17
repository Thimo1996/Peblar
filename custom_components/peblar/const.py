"""Constants for the Eneco peblar integration."""

from enum import StrEnum

DOMAIN = "peblar"
UPDATE_INTERVAL = 30


CHARGER_CURRENT_VERSION_KEY = "firmwareversion"
CHARGER_PART_NUMBER_KEY = "productpn"
CHARGER_SERIAL_NUMBER_KEY = "productsn"
CHARGER_SOFTWARE_KEY = "firmwareversion"
CHARGER_MAX_CHARGING_CURRENT_KEY = "chargecurrentlimit"
CHARGER_CHARGING_CURRENT_ACTUAL_KEY = "chargecurrentlimitactual"
CHARGER_TOTAL_ENERGY_KEY = "energytotal"
CHARGER_CURRENT_PHASE1_KEY = "currentphase1"
CHARGER_SESSION_ENERGY_KEY = "energysession"
CHARGER_VOLTAGE_PHASE1_KEY = "voltagephase1"
CHARGER_POWER_PHASE1_KEY = "powerphase1"
CHARGER_CURRENT_PHASE2_KEY = "currentphase2"
CHARGER_VOLTAGE_PHASE2_KEY = "voltagephase2"
CHARGER_POWER_PHASE2_KEY = "powerphase2"
CHARGER_CURRENT_PHASE3_KEY = "currentphase3"
CHARGER_VOLTAGE_PHASE3_KEY = "voltagephase3"
CHARGER_POWER_PHASE3_KEY = "powerphase3"
CHARGER_CHARGE_POWER_KEY = "powertotal"
CHARGER_CP_STATE_KEY = "cpstate"
CHARGER_CP_STATE_DESCRIPTION_KEY = "chargestatedescription"
CHARGER_LIMIT_SOURCE_DESCRIPTION_KEY = "chargecurrentlimitsource"


class ChargerStatus(StrEnum):
    """Charger Status Description."""

    DISCONNECTED = "No EV connected"
    SUSPENED = "EV connected but suspended"
    CHARGING = "EV connected and charging"
    CHARGING_VENTILATION = "Same as C but ventilation requested"
    ERROR = "Error, short to PE or powered off"
    FAULT = "Fault"
    INVALID = "Invalid CP level measured"
    UNKNOWN = "Unknown"
