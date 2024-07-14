"""Constants for the Loe Outages integration."""

from typing import Final

DOMAIN: Final = "loe_outages"
NAME: Final = "Loe Outages"

# Configuration option
CONF_GROUP: Final = "group"

# Defaults
DEFAULT_GROUP: Final = "1.1"

# Consts
UPDATE_INTERVAL: Final = 60

# Values
STATE_ON: Final = "poweron"
STATE_OFF: Final = "poweroff"

# Keys
TRANSLATION_KEY_EVENT_OFF: Final = f"component.{DOMAIN}.common.electricity_off"
TRANSLATION_KEY_EVENT_ON: Final = f"component.{DOMAIN}.common.electricity_on"
