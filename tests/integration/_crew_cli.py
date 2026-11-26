"""Run the real crew commands without reading or writing a user's saved login."""

import os
from types import SimpleNamespace

from smallestai.cli.agent_crew import initialise_agent_crew_app
from smallestai.cli.lib.atoms import AtomsAPIClient
from smallestai.cli.lib.project_config import ProjectConfig


def main():
    key = os.environ["SMALLEST_API_KEY"]
    base = os.environ["SMALLEST_BASE_URL"]
    app = initialise_agent_crew_app(
        ProjectConfig(),
        SimpleNamespace(get_credentials=lambda: {"access_token": key}),
        AtomsAPIClient(base_url=base),
    )
    app()


if __name__ == "__main__":
    main()
