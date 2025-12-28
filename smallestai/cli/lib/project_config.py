from pathlib import Path
from typing import Optional

import tomli
import tomli_w


class ProjectConfig:
    """Manages project-level configuration in .smallest/config.toml"""

    def __init__(self, project_dir: Optional[Path] = None):
        self.project_dir = project_dir or Path.cwd()
        self.config_dir = self.project_dir / ".smallestai"
        self.config_file = self.config_dir / "config.toml"

    def get_agent_id(self) -> Optional[str]:
        """Get agent_id from config, or None if not set."""
        config = self._load_config()
        return config.get("agent_id")

    def set_agent_id(self, agent_id: str) -> None:
        """Set agent_id in config."""
        config = self._load_config()
        config["agent_id"] = agent_id
        self._save_config(config)

    def _load_config(self) -> dict:
        if not self.config_file.exists():
            return {}
        try:
            with open(self.config_file, "rb") as f:
                return tomli.load(f)
        except Exception:
            return {}

    def _save_config(self, config: dict) -> None:
        self.config_dir.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, "wb") as f:
            tomli_w.dump(config, f)
