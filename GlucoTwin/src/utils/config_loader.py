"""
Config loader utility for GlucoTwin.
"""
from pathlib import Path
import yaml
from typing import Dict, Any

def get_project_root() -> Path:
    """Finds the root directory of the GlucoTwin project."""
    # Look for config/config.yaml upwards from current file location
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / "config" / "config.yaml").exists():
            return current
        if (current / "GlucoTwin" / "config" / "config.yaml").exists():
            return current / "GlucoTwin"
        current = current.parent
    # Fallback to relative path
    return Path(__file__).resolve().parents[2]

def load_config(config_path: str = None) -> Dict[str, Any]:
    """Loads configuration YAML dictionary."""
    root = get_project_root()
    if config_path is None:
        target_path = root / "config" / "config.yaml"
    else:
        target_path = Path(config_path)
        if not target_path.is_absolute():
            target_path = root / target_path
            
    if not target_path.exists():
        raise FileNotFoundError(f"Configuration file not found at: {target_path}")
        
    with open(target_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    # Resolve relative paths in config relative to project root
    if "paths" in config:
        for k, v in config["paths"].items():
            config["paths"][k] = str((root / v).resolve())
            
    return config
