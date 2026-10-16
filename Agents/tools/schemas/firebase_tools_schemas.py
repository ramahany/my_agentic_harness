tools = [
    {
        "type": "function",
        "name": "get_product_details",
        "description": "Get details for a specific product.",
        "parameters": {
            "type": "object",
            "properties": {
                "product_name": {
                    "type": "string",
                    "description": "The name of the product to fetch details for",
                },
            },
            "required": ["product_name"],
            "additionalProperties": False
        },
    },
]