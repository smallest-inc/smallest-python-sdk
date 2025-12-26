import json
import os
import stat
from pathlib import Path
from typing import Dict, Optional


class AuthClient:
    def __init__(self, app_name: str = "smallestai"):
        self.app_name = app_name
        self.config_dir = Path.home() / f".{app_name}"
        self.credentials_file = self.config_dir / "credentials.json"
        self.config_file = self.config_dir / "config.json"

        self.config_dir.mkdir(parents=True, exist_ok=True)

    def login(self, auth_token: str) -> bool:
        """
        Authenticate user and store credentials
        """
        self._store_credentials(
            {
                "access_token": auth_token,
            }
        )

        return True

    def _store_credentials(self, credentials: Dict) -> None:
        with open(self.credentials_file, "w") as f:
            json.dump(credentials, f, indent=2)

        os.chmod(self.credentials_file, stat.S_IRUSR | stat.S_IWUSR)

    def get_credentials(self) -> Optional[Dict]:
        if not self.credentials_file.exists():
            return None

        try:
            with open(self.credentials_file, "r") as f:
                return json.load(f)
        except Exception:
            return None

    def logout(self) -> None:
        """Remove stored credentials"""
        if self.credentials_file.exists():
            self.credentials_file.unlink()
