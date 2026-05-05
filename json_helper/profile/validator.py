import json, jsonschema, jsonschema.exceptions

from json_helper.profile.schema import schema_v1

def ValidateProfile(player_save_path) -> dict | None:
    """Validates and returns Profile save. Returns None if profile is invalid or missing."""

    print(f"Trying to access file `{player_save_path}`")
    try:
        with open(player_save_path, "r") as file:
            data = json.load(file)
    except:
        return None

    try:
        jsonschema.validate(data, schema_v1)
    except jsonschema.exceptions.ValidationError as e:
        print(f"Error validating `{player_save_path}`.")
        return None
    
    if data["player_stats_save"]["version"] == 1:
        # New unlocked ship list
        old_list = data["player_stats_save"]["unlocked_ships"]
        new_list = []
        for ship_tuple in old_list:
            if ship_tuple[1]:
                new_list.append(ship_tuple[0])
        data["player_stats_save"]["unlocked_ships"] = new_list
        data["player_stats_save"]["version"] = 2

    return data
