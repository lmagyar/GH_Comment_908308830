
for regulator_search_pattern_ in [
            ["climate", "climate.set_temperature"],
            ["humidifier", "humidifier.set_humidity"],
        ] :
    domain = regulator_search_pattern_[0]
    service = regulator_search_pattern_[1]
    for regulator_ in hass.states.all(domain) :
        hass.services.call("group", "set", {
            "object_id": regulator_.object_id + "_schedules",
            "name": "[" + regulator_.name + " Schedules]",
            "entities": [
                switch_.entity_id for switch_ in hass.states.all("switch")
                    if (switch_.entity_id.startswith("switch.schedule_")
                        and 0 < len([switch_action_ for switch_action_ in switch_.attributes.get("actions", [])
                            if (switch_action_["service"] == service
                                and switch_action_["entity_id"] == regulator_.entity_id)]))
            ]
        })
