
forced = data.get("forced")
entity_id = data.get("entity_id")

if not isinstance(forced, bool) :
    forced = False

if isinstance(entity_id, str) :
    entity_id_list = [e.strip() for e in entity_id.split(',')]
else :
    entity_id_list = entity_id

for entity_id_ in entity_id_list :
    entity_state = hass.states.get(entity_id_)
    dependent_entity_id = entity_state.attributes.get("dependent")
    dependent_by_parameter = entity_state.attributes.get("dependent_by_parameter", False)
    condition = entity_state.attributes.get("condition", True)
    if not isinstance(condition, bool) :
        condition = hass.states.get(condition).state == "on"
    dependent_state = hass.states.get(dependent_entity_id) if dependent_entity_id is not None else None
    if dependent_state is not None :
        if dependent_state.domain == "script" :
            if condition :
                hass.services.call("script", dependent_state.object_id, {
                    "leader": entity_id_,
                    "leader_state": entity_state.state
                })
        elif (dependent_by_parameter
                or entity_state.state == dependent_state.state and forced) :
            if condition :
                hass.states.set(dependent_entity_id, dependent_state.state, dependent_state.attributes.copy(), force_update=True)
        elif entity_state.state != dependent_state.state and condition :
            if dependent_state.domain == "input_select" :
                hass.services.call("input_select", "select_option", {
                    "entity_id": dependent_entity_id,
                    "option": entity_state.state
                })
            else : # anything boolean: input_boolean, switch
                hass.services.call("homeassistant", "turn_on" if entity_state.state == "on" else "turn_off", {
                    "entity_id": dependent_entity_id
                })
