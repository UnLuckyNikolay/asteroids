schema_v1 = {
    "type": "object",
    "required": [
        "version",
        "player_stats_save"
    ],
    "properties": {
        "version": {
            "type": "number"
        },
        "player_stats_save": {
            "type": "object",
            "required": [
                "version",
                "name",
                "ship_model",
                "found_cheats",
                "cheat_godmode",
                "cheat_hitbox",
                "cheat_stonks"
            ],
            "properties": {
                "version": {
                    "type": "number"
                },
                "name": {
                    "type": "string",
                    "default": "Player"
                },
                "ship_model": {
                    "type": "number"
                },
                "found_cheats": {
                    "type": "boolean"
                },
                "cheat_godmode": {
                    "type": "boolean"
                },
                "cheat_hitbox": {
                    "type": "boolean"
                },
                "cheat_stonks": {
                    "type": "boolean"
                }
            }
        }
    }
}