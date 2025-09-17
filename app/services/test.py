def extract_station_ids(data: dict) -> list:
    """
    Recursively extracts all 'code' values that represent a station ID
    from a nested dictionary structure.
    
    Args:
        data: The dictionary to search.
        
    Returns:
        A list of all found station IDs (codes).
    """
    station_ids = []
    
    # Check the current dictionary for a station ID
    if data.get("type") == "Department" and data.get("code"):
        station_ids.append(data.get("code"))
    
    # Check for a 'children' key and iterate if it exists
    children_list = data.get("children", [])
    if isinstance(children_list, list):
        for child in children_list:
            # Recursively call the function for each child
            station_ids.extend(extract_station_ids(child))
            
    # Also check the top-level 'data' key for children
    top_level_data = data.get("data", {})
    if isinstance(top_level_data, dict):
        station_ids.extend(extract_station_ids(top_level_data))
        
    return station_ids