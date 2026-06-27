def format_routine_item(task_name, icon):
    """Deterministic formatting for A2UI components."""
    return {
        "component": "Card",
        "children": [
            {"component": "Icon", "name": icon},
            {"component": "Text", "text": task_name}
        ]
    }

if __name__ == "__main__":
    # Local test run
    print(format_routine_item("Brush Teeth", "toothbrush"))
