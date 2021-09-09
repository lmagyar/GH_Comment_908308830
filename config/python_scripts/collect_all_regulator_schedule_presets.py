
preset_entity_id = data.get("entity_id")

if not isinstance(preset_entity_id, str) :
    preset_entity_id = str(preset_entity_id)

presets = []
for switch_ in hass.states.all("switch") :
    if (switch_.entity_id.startswith("switch.schedule_")
            and len([switch_action_ for switch_action_ in switch_.attributes.get("actions", [])
                if switch_action_["service"] in [
                    "climate.set_temperature",
                    "humidifier.set_humidity"]]) > 0) :
        switch_name = switch_.name
        switch_name_length = len (switch_name)
        start = 0
        end = 0
        while start < switch_name_length and (start := switch_name.find("[", start)) != -1 and (end := switch_name.find("]", start)) != -1 :
            new_preset = switch_name[start+1:end].capitalize()
            if new_preset not in presets :
                presets.append(new_preset)
            start = end + 1
if len(presets) == 0 :
    presets = ["Default"]
presets.sort()

current_selection = hass.states.get(preset_entity_id).state
hass.services.call("input_select", "set_options", {
    "entity_id": preset_entity_id,
    "options": presets
})
if current_selection in presets :
    hass.services.call("input_select", "select_option", {
        "entity_id": preset_entity_id,
        "option": current_selection
    })
