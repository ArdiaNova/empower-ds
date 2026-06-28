from mcp.server.fastmcp import FastMCP
import json
import os

mcp = FastMCP("progress-analyst")

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


@mcp.tool()
def get_ds_benchmarks(milestone_key: str) -> str:
    """Retrieves DS-adjusted developmental benchmarks for a given milestone key.

    Args:
        milestone_key: The milestone to look up, e.g. "walking" or "first_word".

    Returns:
        The benchmark age range as a string, or an error/not-found message.
    """
    path = os.path.join(DATA_DIR, "ds_benchmarks.json")
    try:
        with open(path, "r") as f:
            data = json.load(f)
        return str(data.get(milestone_key, "Benchmark not found"))
    except FileNotFoundError:
        return f"Error: {path} not found."


@mcp.tool()
def save_milestone(achievement: str, date: str) -> str:
    """Logs a new milestone achievement with its date to the local milestone database.

    Args:
        achievement: Description of the milestone achieved, e.g. "Walking".
        date: The date the milestone was achieved, e.g. "2026-06-20".

    Returns:
        A confirmation message, or an error message if the save failed.
    """
    path = os.path.join(DATA_DIR, "user_milestones.json")
    try:
        with open(path, "r") as f:
            db = json.load(f)
        db["milestones"].append({"achievement": achievement, "date": date})
        with open(path, "w") as f:
            json.dump(db, f, indent=2)
        return "Milestone saved locally."
    except FileNotFoundError:
        return f"Error: {path} not found."


@mcp.tool()
def get_milestones() -> str:
    """Retrieves all saved milestone achievements from the local milestone database.

    Returns:
        A summary of all logged milestones, or a message if none are saved yet.
    """
    path = os.path.join(DATA_DIR, "user_milestones.json")
    try:
        with open(path, "r") as f:
            db = json.load(f)
        milestones = db.get("milestones", [])
        if not milestones:
            return "No milestones have been saved yet."
        lines = [f"- {m['achievement']} (achieved on {m['date']})" for m in milestones]
        return "Saved milestones:\n" + "\n".join(lines)
    except FileNotFoundError:
        return f"Error: {path} not found."


if __name__ == "__main__":
    mcp.run()