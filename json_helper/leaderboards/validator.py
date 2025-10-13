import json, jsonschema, jsonschema.exceptions

from json_helper.leaderboards.schema import schema_v1

def ValidateLeaderboards(leaderboards_path) -> list:
    """Validates and returns Leaderboards JSON. Returns empty list if JSON is invalid."""

    print(f"Trying to access file `{leaderboards_path}`")
    try:
        with open(leaderboards_path, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []

    try:
        jsonschema.validate(data, schema_v1)
    except jsonschema.exceptions.ValidationError:
        print("Error validating leaderboards.json. Resetting the leaderboards.")
        return []

    return data