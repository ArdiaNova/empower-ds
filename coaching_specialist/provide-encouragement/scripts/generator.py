def generate_coaching_card(headline, message, icon="star"):
    """Deterministic generator for celebratory A2UI cards."""
    return {
        "component": "Card",
        "children": [
            {"component": "Icon", "name": icon},
            {"component": "Text", "text": headline, "variant": "h2"},
            {"component": "Divider"},
            {"component": "Text", "text": message}
        ]
    }

if __name__ == "__main__":
    # Verify locally
    import json
    print(json.dumps(generate_coaching_card("Great Job!", "You walked today!"), indent=2))