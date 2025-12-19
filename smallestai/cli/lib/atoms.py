from typing import List, Optional

import httpx
from pydantic import BaseModel, Field
from rich.console import Console

console = Console()


class AccountDetailsData(BaseModel):
    firstName: str
    lastName: str
    userEmail: str


class Agent(BaseModel):
    id: str = Field(..., validation_alias="_id")
    name: str


class AgentData(BaseModel):
    agents: List[Agent]
    hasMore: bool
    totalCount: int
    totalPages: int


class AccountDetailsAPIResponse(BaseModel):
    status: bool
    data: Optional[AccountDetailsData] = Field(default=None)
    errors: Optional[List[str]] = Field(default=None)


class AgentsAPIResponse(BaseModel):
    status: bool
    data: Optional[AgentData] = Field(default=None)
    errors: Optional[List[str]] = Field(default=None)


class AtomsAPIClient:
    def __init__(self):
        self.base_url = "https://atoms-api.smallest.ai"

    async def get_agents(
        self,
        access_token: str,
        page: int = 1,
        # TODO: Replace the paginated api with the non paginated api
        # This is hack to get the all the agents
        offset: int = 100000000,
        sort_field: str = "updatedAt",
        sort_order: str = "desc",
    ):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/api/v1/agent?page={page}&offset={offset}&sortField={sort_field}&sortOrder={sort_order}",
                headers={
                    "Authorization": f"Bearer {access_token}",
                },
            )

            response.raise_for_status()

            agents_response = AgentsAPIResponse.model_validate(response.json())

            if agents_response.status is False or agents_response.data is None:
                raise Exception(agents_response.errors)

            return agents_response.data

    async def get_account_details(
        self,
        access_token: str,
    ) -> AccountDetailsData:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/api/v1/user",
                headers={
                    "Authorization": f"Bearer {access_token}",
                },
            )

            response.raise_for_status()

            account_details_response = AccountDetailsAPIResponse.model_validate(response.json())

            if account_details_response.status is False or account_details_response.data is None:
                raise Exception(account_details_response.errors)

            return account_details_response.data
