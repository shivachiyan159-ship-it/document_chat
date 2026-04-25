import os
from pathlib import Path

import yaml

def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]

def load_config(config_path:str):
    
    env_path = os.getenv("config_path")
    
    if config_path is None:
        config_path=env_path
    
    path=Path(config_path)
    
    if not path.is_absolute():
        path = _project_root()/path
    
    if not path.exists():
        raise FileNotFoundError("config file not found")
    
    with open(path,"r") as f:
        return yaml.safeload(f) or {}