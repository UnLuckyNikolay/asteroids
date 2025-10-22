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
                "found_cheats",
                "cheat_godmode",
                "cheat_hitbox",
                "cheat_stonks",
                "ship_model"
            ],
            "properties": {
                "version": {
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
                },
                "ship_model": {
                    "type": "number"
                }
            }
        }
    }
}