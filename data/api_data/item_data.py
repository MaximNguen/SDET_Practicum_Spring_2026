class ItemData:
    valid_data = {
        "addition": {
            "additional_info": "Дополнительные сведения",
            "additional_number": 123
        },
        "important_numbers": [
            42,
            87,
            15
        ],
        "title": "Заголовок сущности",
        "verified": True
        }
    expected_fields = ["addition", "important_numbers", "title", "verified"]