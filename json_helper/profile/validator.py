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

    return data
