
for group_ in hass.states.all("group") :
    if group_.name.startswith("[") and group_.name.endswith("]") :
        hass.services.call("group", "remove", {
            "object_id": group_.object_id
        })
