"""Platform for fan integration."""
import usb.core
import usb.util
import homeassistant.helpers.config_validation as cv
import logging

from homeassistant.const import (
    ATTR_ENTITY_ID,
    STATE_UNKNOWN,
    STATE_OFF,
    STATE_ON,
    ATTR_MODE,
    ATTR_STATE,
    ATTR_ICON,
    CONF_HOST
)

from homeassistant.components.fan import (
    FanEntity,
    SUPPORT_SET_SPEED,
    SUPPORT_PRESET_MODE,
    ATTR_PRESET_MODE,
    ATTR_PRESET_MODES,
    ATTR_PERCENTAGE,
    ATTR_PERCENTAGE_STEP
)

from .const import (
    DOMAIN,
    FAN_DEVICES,
    STATES_MANAGER,
    MODE_AUTO,
    MODE_MANUALLY,
    MODE_TIMING,
    DEVICE_INFO,
    SPEED_OFF,
    SPEED_LOW,
    SPEED_MEDIUM,
    SPEED_HIGH,
    ATTR_SPEED
)

async def async_setup_entry(hass, config_entry, async_add_entities):
    states_manager = hass.data[config_entry.entry_id][STATES_MANAGER]
    hass.data[config_entry.entry_id][FAN_DEVICES] = []
    dev = USBLight(states_manager, config_entry.data[CONF_HOST])
    hass.data[config_entry.entry_id][FAN_DEVICES].append(dev)

    async_add_entities(hass.data[config_entry.entry_id][FAN_DEVICES])

class USBLight(FanEntity):
    def __init__(self, states_manager, host):
        self._dev = states_manager
        self._unique_id = f"{DOMAIN}.{host}"
        self.entity_id = self._unique_id
        self._states_manager = states_manager
        self._state = STATE_OFF
        self._mode = MODE_AUTO
        self._speed = 0
        self._icon = "mdi:fan"
        self._device_info = DEVICE_INFO
        self._device_info["identifiers"] = {(DOMAIN, host)}
        self._attr_preset_modes = [MODE_AUTO]
        self._attr_supported_features = SUPPORT_SET_SPEED | SUPPORT_PRESET_MODE
        self._states_manager.set_fan_update(self.update_status)

    def set_percentage(self, percentage) -> None:
        self._speed = percentage

    async def async_set_percentage(self, percentage: int) -> None:
        await self.hass.async_add_executor_job(self.set_percentage, percentage)

    @property
    def speed_count(self) -> int:
        return 10

    @property
    def percentage_step(self) -> float:
        return 1

    @property
    def state(self):
        return self._state

    @property
    def is_on(self):
        return self._state == STATE_ON

    @property
    def percentage(self):
        if self._speed == SPEED_OFF:
            _percentage = 0
        else:
            _percentage = self._speed
        return _percentage

    @property
    def device_info(self):
        return self._device_info

    #set name
    @property
    def name(self):
        return "ACINFINITY Sensor"

    @property
    def icon(self):
        return self._icon

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def preset_mode(self):
        return self._mode

    @property
    def capability_attributes(self):
        attrs = {}
        attrs[ATTR_PRESET_MODES] = self.preset_modes
        return attrs

    #update
    @property
    def state_attributes(self) -> dict:
        data: dict[int, int | str | None] = {}
        data[ATTR_PERCENTAGE] = self.percentage
        data[ATTR_PERCENTAGE_STEP] = self.percentage_step
        #data[ATTR_PRESET_MODE] = self.preset_mode
        data[ATTR_PRESET_MODE] = "ACinfinity use"
        return data

    @property
    def should_poll(self):
        return False
    
    def update_status2(self, data: dict):
        
        self._state = STATE_ON
     
        try:
            self.schedule_update_ha_state()
        except Exception:
            pass

    def update_status(self, data: dict):
        if ATTR_SPEED in data:
            self._speed = data[ATTR_SPEED]
        if ATTR_MODE in data:
            self._mode = data[ATTR_MODE]
        if ATTR_STATE in data:
            self._state = data[ATTR_STATE]
        if ATTR_ICON in data:
            self._icon = data[ATTR_ICON]
        try:
            self.schedule_update_ha_state()
            
        except Exception:
            pass
    
    def get_requet(self):
        #触发我的设备函数
        myres = ""
        return myres
    def brilight(self):
        self._state = STATE_ON
        return self._state == STATE_ON
    
    def turn_on(
            self,
            percentage: int | None = None,
            preset_mode: str | None = None,
            **kwargs,
    ):
        percentage = self.percentage
        self._state = STATE_ON    
        try:
            self.schedule_update_ha_state()
        except Exception:
            pass
    def turn_off(self, **kwargs):
        self._state = STATE_OFF  
        try:
            self.schedule_update_ha_state()
        except Exception:
            pass

    def set_speed(self, speed: str):
        if speed != self._speed:
            self._states_manager.set_speed(speed)

    def set_preset_mode(self, preset_mode: str):
        if preset_mode != self._mode:
            self._states_manager.set_mode(preset_mode)
    
    def update(self):
        self._state = STATE_ON
        self._states_manager.set_fan_update(self.update_status)


