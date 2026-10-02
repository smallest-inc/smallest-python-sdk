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

    def login(self, auth_token: str, base_url: Optional[str] = None) -> bool:
        """
        Authenticate user and store credentials.

        ``base_url`` optionally pins the regional API host (e.g.
        ``https://api.india.smallest.ai``) so it is reused on every command
        without setting ``SMALLEST_BASE_URL`` each time.
        """
        credentials: Dict = {"access_token": auth_token}
        if base_url:
            credentials["base_url"] = base_url.rstrip("/")

        self._store_credentials(credentials)

        return True

    def get_base_url(self) -> Optional[str]:
        """The regional API host pinned at login, if any."""
        creds = self.get_credentials()
        return (creds or {}).get("base_url")

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
