import json, jsonschema, jsonschema.exceptions

from json_helper.leaderboard.schema import schema_v1

def ValidateLeaderboard(leaderboard_path) -> list:
    """Validates and returns Leaderboard JSON. Returns empty list if JSON is invalid."""

    print(f"Trying to access file `{leaderboard_path}`")
    try:
        with open(leaderboard_path, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        return []

    try:
        jsonschema.validate(data, schema_v1)
    except jsonschema.exceptions.ValidationError:
        print(f"Error validating `{leaderboard_path}`. Resetting the leaderboard.")
        return []

    return data