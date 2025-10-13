schema_v1 = {
    "type": "array",
    "items": {
        "type": "object",
        "required": [
            "name",
            "score"
        ],
        "properties": {
            "name": {
                "type": "string"
            },
            "score": {
                "type": "number",
                "minimum": 1
            }
        }
    }
}