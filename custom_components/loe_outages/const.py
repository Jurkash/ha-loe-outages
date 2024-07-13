"""Constants for the LOE Outages integration."""

from typing import Final

DOMAIN: Final = "loe_outages"
NAME: Final = "LOE Outages"

# Configuration option
CONF_GROUP: Final = "group"

# Defaults
DEFAULT_GROUP: Final = "1.1"

# Consts
UPDATE_INTERVAL: Final = 60

# Values
STATE_ON: Final = "PowerOn"
STATE_OFF: Final = "PowerOff"
# Endpoint paths
SCHEDULE_PATH = "https://lps.yuriishunkin.com/api/schedule/latest/{group}"
API_BASE_URL = "https://lps.yuriishunkin.com/api"


# Keys
TRANSLATION_KEY_EVENT_OFF: Final = f"component.{DOMAIN}.common.electricity_off"
