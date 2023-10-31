"""Integration for ACInfinity"""
import asyncio

import logging
import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_NAME
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import async_generate_entity_id

from .const import DOMAIN, CONF_VALUE, DEFAULT_VALUE, DEVICES, STATES_MANAGER
from .statemanager import StateManager

from homeassistant.const import CONF_HOST, CONF_PORT

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    """Set up from a config entry."""
    config = config_entry.data
    host = config[CONF_HOST]
    port = config[CONF_PORT]

    state_manager = StateManager(host, port)

    hass.data[DOMAIN][DEVICES] = []
    hass.data[DOMAIN][DEVICES].append(host)
    hass.data[config_entry.entry_id] = {}
    hass.data[config_entry.entry_id][STATES_MANAGER] = state_manager
    state_manager.open()

    for platform in {"fan"}:
        hass.async_create_task(hass.config_entries.async_forward_entry_setup(
            config_entry, platform))
    return True

async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    await hass.config_entries.async_forward_entry_unload(config_entry, "sensor")
    state_manager = hass.data[config_entry.entry_id][STATES_MANAGER]
    state_manager.close()

    hass.data[DOMAIN][DEVICES].pop(config_entry.data[CONF_HOST])
    if len(hass.data[DOMAIN][DEVICES]) == 0:
        hass.data.pop(DOMAIN)
    hass.data.pop(config_entry.entry_id)
    return True
