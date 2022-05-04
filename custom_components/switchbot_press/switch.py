"""Support for Switchbot_press."""
import logging
from typing import Any, Dict
from datetime import datetime

# pylint: disable=import-error, no-member
import switchbot
import voluptuous as vol

try:
    from homeassistant.components.switch import SwitchEntity
except ImportError:
    from homeassistant.components.switch import SwitchDevice as SwitchEntity
from homeassistant.components.switch import PLATFORM_SCHEMA
from homeassistant.const import CONF_MAC, CONF_NAME, CONF_PASSWORD
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.util import dt as dt_util

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "Switchbot_press"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_MAC): cv.string,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_PASSWORD): cv.string,
    }
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Perform the setup for Switchbot_press devices."""
    name = config.get(CONF_NAME)
    mac_addr = config[CONF_MAC]
    password = config.get(CONF_PASSWORD)
    add_entities([SwitchBot_press(mac_addr, name, password)])


class SwitchBot_press(SwitchEntity, RestoreEntity):
    """Representation of a Switchbot."""

    def __init__(self, mac, name, password) -> None:
        """Initialize the Switchbot_press."""

        self._state = None
        self._last_run_success = None
        self._last_pressed: datetime | None = None
        self._name = name
        self._mac = mac
        self._device = switchbot.Switchbot(mac=mac, password=password)

    async def async_added_to_hass(self):
        """Run when entity about to be added."""
        await super().async_added_to_hass()
        state = await self.async_get_last_state()
        if not state:
            return
        self._state = state.state == "on"

    def turn_on(self, **kwargs) -> None:
        """Turn device on."""
        if self._device.press():
            self._state = False
            self._last_pressed = dt_util.utcnow()
            self._last_run_success = True
        else:
            self._last_run_success = False

    def turn_off(self, **kwargs) -> None:
        self._last_run_success = True

    @property
    def assumed_state(self) -> bool:
        """Return true if unable to access real state of entity."""
        return False

    @property
    def is_on(self) -> bool:
        """Return true if device is on."""
        return False

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return self._mac.replace(":", "")

    @property
    def name(self) -> str:
        """Return the name of the switch."""
        return self._name

    def last_pressed(self) -> str:
        if self._last_pressed is None:
            return ''
        return self._last_pressed.isoformat()

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return the state attributes."""
        return {"last_run_success": self._last_run_success, "last_pressed": self.last_pressed()}
