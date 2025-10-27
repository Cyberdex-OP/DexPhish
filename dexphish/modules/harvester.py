"""Data harvester placeholder.

Contains a harmless stub for harvesting data (no network/file writes by default).
"""

def harvest(source: str) -> dict:
    """Return a fake harvest result structure for testing."""
    print(f"[harvester] harvest called with source={source!r}")
    return {"source": source, "items": []}
