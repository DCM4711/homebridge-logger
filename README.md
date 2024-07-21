# homebridge-logger
Log Homebridge events/property-changes to a MySQL database


********************************************************************************
*                             HOMEBRIDGE-LOGGER                                *
********************************************************************************

This python script aims to solve the problem that there is no built in way to store/log events/property-changes in Homebridge. It is specifically built for my own Homebridge infrastructure but can be easilly extended and modified. Maybe it is of use for someone else too ;)

The script parses the homebridge logfile and extracts events from different types of devices and writes them into a mysql database.
The database can then be the source for tools such as Grafana to visualize these
values. In order for the script to work, 'Hombridge Debug Mode' must be enabled from within the settings menu in Hombridge UI.

Currently supported device types (homebridge plugins):
- HS100
- Shelly
- zigbee2mqtt
- homebridge-webos-tv
