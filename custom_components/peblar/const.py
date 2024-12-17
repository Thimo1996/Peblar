"""Constants for the Eneco peblar integration."""

from enum import StrEnum

DOMAIN = "peblar"
UPDATE_INTERVAL = 30


CHARGER_CURRENT_VERSION_KEY = "FirmwareVersion"
CHARGER_PART_NUMBER_KEY = "ProductPn"
CHARGER_SERIAL_NUMBER_KEY = "ProductSn"
CHARGER_SOFTWARE_KEY = "FirmwareVersion"
CHARGER_MAX_CHARGING_CURRENT_KEY = "ChargeCurrentLimit"
CHARGER_CHARGING_CURRENT_ACTUAL_KEY = "ChargeCurrentLimitActual"
CHARGER_TOTAL_ENERGY_KEY = "EnergyTotal"
CHARGER_CURRENT_PHASE1_KEY = "CurrentPhase1"
CHARGER_SESSION_ENERGY_KEY = "EnergySession"
CHARGER_VOLTAGE_PHASE1_KEY = "VoltagePhase1"
CHARGER_POWER_PHASE1_KEY = "PowerPhase1"
CHARGER_CURRENT_PHASE2_KEY = "CurrentPhase2"
CHARGER_VOLTAGE_PHASE2_KEY = "VoltagePhase2"
CHARGER_POWER_PHASE2_KEY = "PowerPhase2"
CHARGER_CURRENT_PHASE3_KEY = "CurrentPhase3"
CHARGER_VOLTAGE_PHASE3_KEY = "VoltagePhase3"
CHARGER_POWER_PHASE3_KEY = "PowerPhase3"
CHARGER_CHARGE_POWER_KEY = "PowerTotal"
CHARGER_CP_STATE_KEY = "CpState"
CHARGER_CP_STATE_DESCRIPTION_KEY = "ChargeStateDescription"
CHARGER_LIMIT_SOURCE_DESCRIPTION_KEY = "ChargeCurrentLimitSource"


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
