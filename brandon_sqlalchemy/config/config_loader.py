import os.path
from pathlib import Path
import yaml

class ConfigLoader():

    def __init__(self, filename):
        self.config_path = None
        self.config_filename = filename

        self._read_config()
        self.db_config = self._load_db_config()


    def _read_config(self):
        cur_file_path = os.path.abspath(__file__)
        parent_dir_path = Path(os.path.dirname(cur_file_path)).parent
        config_path = f"{parent_dir_path}/config/{self.config_filename}"
        self.config_path = config_path
        return config_path

    def _load_db_config(self):
        with open(self.config_path, "r") as file:
            data = yaml.safe_load(file)
        return data["db"]

