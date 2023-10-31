from __future__ import annotations
from homeassistant import config_entries


def get_value(config_entry: config_entries.ConfigEntry | None, param: str, default=None):
    if config_entry is not None:
        return config_entry.options.get(param, config_entry)
    else:
        return default
