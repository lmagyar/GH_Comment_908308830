
# Sample repository

For: https://github.com/nielsfaber/scheduler-card/issues/219#issuecomment-908308830

## Notes

1. This is a copy-paste-delete-delete-delete-... version of my config. Theoretically it requires only a `sensor.living_room_temperature` and a `switch.heater` entity to be a valid config.
1. Entities are "connected" by my custom defined `dependant` attribute, that added by customization (in the yaml also).
1. Scripts copy the states, usually "on"/"off", along these `dependant` relations.
1. Scripts create groups for the schedules, that belong to a regulator (thermostat or dehumidifier in my case).
1. Scripts collect the "schedule presets" from the schedule names. You have to surround these user defineable "schedule presets" with [ and ] brackets. Eg. schedule name: "Big pool [winter] temperature schedule"
1. Sensors detect, whether a regulator is in auto mode, then automations turn on/off the schedules that belong to this regulator's group, though they turn on only those that belong to the selected "schedule preset", like winter, summer, normal, early, etc.
1. Independent from the above, my regulators are switching only virtual things, like an `input_boolean.virtual_heater`, then automations copy the state changes of these virtual switches to the real ones, like `switch.heater`, and (!) they also do it regularly, because the real switches have default `off` values, without repeating messages, they turn off. This way in case of network or HA or rPI failure, the actuator (eg. heater) won't run continuously.
1. It survives any kind of restart and recalculates it's state. Eg. if the virtual thermostat should switch on/off during a restart/reload, these automations will put them in the proper state after a restart.
1. __Important:__ automation state triggers can't be groups, all the members of the groups has to be enumerated in the trigger. See the `# group.xxx` comment lines.
1. Maybe start with schedules.yaml to understand the concept.
