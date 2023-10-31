from homeassistant.const import Platform

DOMAIN = "ACINFINITY"
PLATFORMS = [Platform.SENSOR]
UPDATE_LISTENER = "update_listener"
CONF_POLL = "poll"
CONF_VALUE = "value"
DEFAULT_VALUE = "password"

DEFAULT_PORT = 9600
DEVICES = "devices"
FAN_DEVICES = "fan_devices"
STATES_MANAGER = "stateS_manager"

DEVICE_CLASS_PM25 = "pm2_5"
DEVICE_CLASS_VOC = "voc"
DEVICE_CLASS_FILTER = "filter"

MODE_AUTO = "cooltron use"
MODE_MANUALLY = "manually"
MODE_TIMING = "timing"

SPEED_OFF = "off"
SPEED_LOW = "low"
SPEED_MEDIUM = "medium"
SPEED_HIGH = "high"
ATTR_SPEED = "speed"

DEVICE_INFO = {
            "manufacturer": "BLAUBERG",
            "model": "Komfort ERV D 150P V3",
            "name": "Cooltron' Sensors"
}
