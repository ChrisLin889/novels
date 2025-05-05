import os
import json

# Default settings
DEFAULT_SETTINGS = {
    "enable_content_audit": True,  # Enable/disable content audit
    "cache_ttl": 3600,            # Cache time-to-live in seconds
    "max_search_results": 100     # Maximum search results to return
}

# Path to settings file
SETTINGS_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
    'config', 
    'settings.json'
)

# Cached settings
_cached_settings = None

def get_settings():
    """
    Load settings from file or return cached settings
    
    Returns:
        dict: Application settings
    """
    global _cached_settings
    
    # Return cached settings if available
    if _cached_settings is not None:
        return _cached_settings
    
    # Create settings directory if it doesn't exist
    os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
    
    # Load settings from file or create new file with defaults
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as f:
                settings = json.load(f)
                
            # Update with any missing default settings
            updated = False
            for key, value in DEFAULT_SETTINGS.items():
                if key not in settings:
                    settings[key] = value
                    updated = True
            
            # Save updated settings
            if updated:
                with open(SETTINGS_FILE, 'w') as f:
                    json.dump(settings, f, indent=2)
        else:
            # Create new settings file with defaults
            settings = DEFAULT_SETTINGS.copy()
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(settings, f, indent=2)
    except Exception as e:
        print(f"Error loading settings: {e}")
        settings = DEFAULT_SETTINGS.copy()
    
    # Cache settings
    _cached_settings = settings
    return settings

def update_setting(key, value):
    """
    Update a setting and save to file
    
    Args:
        key (str): Setting key
        value (any): Setting value
        
    Returns:
        bool: Success status
    """
    global _cached_settings
    
    try:
        # Get current settings
        settings = get_settings()
        
        # Update setting
        settings[key] = value
        
        # Save settings
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=2)
        
        # Update cache
        _cached_settings = settings
        return True
    except Exception as e:
        print(f"Error updating setting: {e}")
        return False 