import sys, json, os

def get_ds_benchmarks(milestone_key):
    """Retrieves DS-adjusted benchmarks from local JSON."""
    try:
        with open("data/ds_benchmarks.json", "r") as f:
            data = json.load(f)
        return data.get(milestone_key, "Benchmark not found")
    except FileNotFoundError:
        return "Error: data/ds_benchmarks.json not found."

def save_milestone(achievement, date):
    """Logs a new milestone to the local database."""
    file_path = "data/user_milestones.json"
    try:
        with open(file_path, "r") as f:
            db = json.load(f)
        db["milestones"].append({"achievement": achievement, "date": date})
        with open(file_path, "w") as f:
            json.dump(db, f, indent=2)
        return "Milestone saved locally."
    except FileNotFoundError:
        return "Error: data/user_milestones.json not found."

if __name__ == "__main__":
    # Robust Python Dispatcher for Local MCP Testing
    if len(sys.argv) < 2: # This will be updated to < 3 or < 4 depending on command.
        print("Usage: python3 mcp_server.py [get <milestone_key> | save <achievement> <date>]")
        sys.exit(1)

    # Correcting the index mapping:
    # sys.argv[0] is script name
    # sys.argv[1] is the command (get/save)
    command = sys.argv[1]

    if command == "get":
        if len(sys.argv) == 3:
            # Expected: python3 mcp_server.py get walking
            print(get_ds_benchmarks(sys.argv[2]))
        else:
            print("Usage for 'get': python3 mcp_server.py get <milestone_key>")
            sys.exit(1)
    
    elif command == "save":
        if len(sys.argv) == 4:
            # Expected: python3 mcp_server.py save "Walking" "2026-06-20"
            print(save_milestone(sys.argv[2], sys.argv[3]))
        else:
            print("Usage for 'save': python3 mcp_server.py save <achievement> <date>")
            sys.exit(1)

    
    else:
        print(f"Invalid command or wrong number of arguments for: {command}")