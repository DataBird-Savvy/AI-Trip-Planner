import yaml
import os
from logger import logger
import sys
from pathlib import Path
from exception import AITripPlannerException
def load_config() -> dict: 
    try:
        project_root = Path(__file__).resolve().parent.parent
        config_path = project_root / "config" / "config.yaml"
        logger.info(f"Checking config file: {config_path}")
        if not os.path.exists(config_path):
            logger.error(f"Config file not found: {config_path}")
            raise FileNotFoundError("Config file not found")
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)
            logger.info("Configuration loaded successfully.")
        return config
    except Exception as e:
        logger.error(f"Error occurred while loading config: {e}")
        raise AITripPlannerException(error_message=e, error_detail=sys.exc_info())
   