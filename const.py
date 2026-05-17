"""Constants for the goe_charger_gold integration."""

from typing import Final

# Integration Information
DOMAIN: Final = "goe_charger_gold"
MANUFACTURER: Final = "go-e"
DEFAULT_NAME: Final = "go-e Charger"

# API Configuration
API_TIMEOUT: Final = 10  # Sekunden
DEFAULT_SCAN_INTERVAL: Final = 30  # Sekunden zwischen Updates
COOLDOWN_SECONDS: Final = 60  # Mindestzeit zwischen Änderungen

# API Endpoints
API_STATUS_ENDPOINT: Final = "/api/status"
API_SET_ENDPOINT: Final = "/api/set"

# PV Steuerung Thresholds
PV_START_THRESHOLD: Final = 1600  # Watt - Start Laden bei diesem Überschuss
PV_STOP_THRESHOLD: Final = 200  # Watt - Stoppen bei weniger als diesem Überschuss
TARGET_VOLTAGE: Final = 230  # Volt - Nominalspannung für Berechnungen

# Amperage Stufen für PV-Überschussladen
AMP_STEPS: Final = [6, 8, 10, 12, 14, 16]
MAX_AMPERE: Final = 16
MIN_AMPERE: Final = 6

# FRC Optionen (Force Control)
FRC_NEUTRAL: Final = "0"  # Laden erlauben (Auto-Logik)
FRC_OFF: Final = "1"  # Laden erzwingt stoppen
FRC_ON: Final = "2"  # Laden erzwingt starten (selten genutzt)

# ACS Optionen (Access Control)
ACS_OPEN: Final = "0"  # RFID-Sperre deaktiviert
ACS_WAIT: Final = "1"  # RFID-Sperre aktiv (warten auf Karte)

# Charger Status Codes (Bitmasken)
STATUS_OFFLINE: Final = 0
STATUS_READY: Final = 1
STATUS_CHARGING: Final = 2
STATUS_ERROR: Final = 4

# Car Status Codes
CAR_UNKNOWN: Final = 0
CAR_IDLE: Final = 1
CAR_CHARGING: Final = 2
CAR_WAIT: Final = 3
CAR_COMPLETE: Final = 4
CAR_ERROR: Final = 5

# Entity Keys (API Parameter)
KEY_AMP: Final = "amp"
KEY_AMA: Final = "ama"
KEY_MCA: Final = "mca"
KEY_FRC: Final = "frc"
KEY_ACS: Final = "acs"
KEY_FUP: Final = "fup"
KEY_FZF: Final = "fzf"
KEY_MOD: Final = "mod"
KEY_SPL3: Final = "spl3"
KEY_CAR: Final = "car"
KEY_STA: Final = "sta"
KEY_NRG: Final = "nrg"
KEY_WH: Final = "wh"
KEY_ETO: Final = "eto"
KEY_TMA: Final = "tma"
KEY_FWV: Final = "fwv"
KEY_RSSI: Final = "rssi"
KEY_FNA: Final = "fna"
KEY_SSE: Final = "sse"
KEY_TYP: Final = "typ"
KEY_OEM: Final = "oem"
KEY_ERR: Final = "err"
KEY_CBL: Final = "cbl"
KEY_ACU: Final = "acu"
KEY_FHZ: Final = "fhz"
KEY_CLW: Final = "cll"
KEY_CCW: Final = "ccw"

# Entity Categories
ENTITY_CATEGORY_CONFIG: Final = "config"
ENTITY_CATEGORY_DIAGNOSTIC: Final = "diagnostic"
