
DEFAULT_PRESET = "[default]"

preset = data.get("preset")
entity_id = data.get("entity_id")

if not isinstance(preset, str) :
    preset = str(preset)
preset = ("[" + preset.lower() + "]") if 0 < len(preset) else DEFAULT_PRESET

if isinstance(entity_id, str) :
    entity_id_list = [e.strip() for e in entity_id.split(',')]
else :
    entity_id_list = entity_id

for entity_id_ in entity_id_list :
    entity_state = hass.states.get(entity_id_)
    dependent_entity_id = entity_state.attributes.get("dependent")
    dependent_state = hass.states.get(dependent_entity_id) if dependent_entity_id is not None else None
    if dependent_state is not None :
        if not dependent_entity_id.startswith("group.") :
            if entity_state.state != dependent_state.state :
                hass.services.call("homeassistant", "turn_on" if entity_state.state == "on" else "turn_off" , {
                    "entity_id": dependent_entity_id
                })
        else :
            if entity_state.state == "on" :
                schedule_entity_ids_to_turn_on = set()
                schedule_entity_ids_to_turn_off = set()
                schedule_entity_id_default = None
                for schedule_entity_id_ in dependent_state.attributes.get("entity_id", []) :
                    if schedule_entity_id_.startswith("switch.schedule_") :
                        schedule_entity_id_name = hass.states.get(schedule_entity_id_).name.lower()
                        if preset in schedule_entity_id_name :
                            schedule_entity_ids_to_turn_on.add(schedule_entity_id_)
                        else :
                            schedule_entity_ids_to_turn_off.add(schedule_entity_id_)
                        if DEFAULT_PRESET in schedule_entity_id_name :
                            schedule_entity_id_default = schedule_entity_id_
                if (0 == len(schedule_entity_ids_to_turn_on)
                        and schedule_entity_id_default is not None) :
                    schedule_entity_ids_to_turn_off.discard(schedule_entity_id_default)
                    schedule_entity_ids_to_turn_on.add(schedule_entity_id_default)
                if 0 < len(schedule_entity_ids_to_turn_off) :
                    hass.services.call("homeassistant", "turn_off", {
                        "entity_id": list(schedule_entity_ids_to_turn_off)
                    })
                if 0 < len(schedule_entity_ids_to_turn_on) :
                    hass.services.call("homeassistant", "turn_on", {
                        "entity_id": list(schedule_entity_ids_to_turn_on)
                    })
            else :
                if 0 < len(dependent_state.attributes.get("entity_id", [])) :
                    hass.services.call("homeassistant", "turn_off", {
                        "entity_id": dependent_entity_id
                    })
