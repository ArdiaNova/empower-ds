import sys
import os

sys.path.append('routine_specialist/visual-routine-prompting/scripts')
from formatter import format_routine_item

def test_routine_formatter():
    result = format_routine_item("Brush Teeth", "toothbrush")
    
    # 1. Verify the top-level component
    assert result["component"] == "Card"
    
    # 2. Verify the list structure exists
    assert isinstance(result["children"], list)
    
    # 3. Verify the Icon component (Position 0 in the list)
    assert result["children"][0]["component"] == "Icon"
    assert result["children"][0]["name"] == "toothbrush"
    
    # 4. Verify the Text component (Position 1 in the list)
    assert result["children"][1]["component"] == "Text"
    assert result["children"][1]["text"] == "Brush Teeth"
    
    print("Routine Formatter Test: PASS")

if __name__ == "__main__":
    try:
        test_routine_formatter()
    except AssertionError as e:
        print(f"Test FAILED: Data structure does not match expectations.")
    except Exception as e:
        print(f"An error occurred: {e}")
        