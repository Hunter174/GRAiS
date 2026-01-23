from pathlib import Path
import yaml

class GoogleConfig:
    def __init__(self, filename: str):
        base_dir = Path(__file__).resolve().parent
        config_path = base_dir / filename

        with open(config_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)["google"]

        self.application_name = data["application_name"]

        self.credentials_file = (base_dir / data["credentials_file"]).resolve()
        self.token_file = Path(data["token_file"]).expanduser().resolve()

        self.scopes = data["scopes"]
