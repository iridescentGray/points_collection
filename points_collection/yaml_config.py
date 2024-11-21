import yaml


class ConfigManager:
    def __init__(self):
        self.config = self.load_config()

    def load_config(self):
        file_path = "./user_data/config.yaml"
        with open(file_path, "r") as f:
            self.config = yaml.safe_load(f)
        return self.config


config_manager = ConfigManager()
