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
                "version"
            ],
            "properties": {
                "version": {
                    "type": "number"
                }
            }
        }
    }
}