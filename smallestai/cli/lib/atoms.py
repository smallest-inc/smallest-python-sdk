from enum import Enum
from typing import List, Optional

import httpx
from pydantic import BaseModel, Field
from rich.console import Console

console = Console()


class AgentBuildStatus(str, Enum):
    QUEUED = "QUEUED"
    BUILDING = "BUILDING"
    BUILD_FAILED = "BUILD_FAILED"
    DEPLOYING = "DEPLOYING"
    DEPLOY_FAILED = "DEPLOY_FAILED"
    SUCCEEDED = "SUCCEEDED"


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


class AgentBuild(BaseModel):
    build_id: str = Field(..., alias="buildId")
    message: str = Field(..., alias="message")


class CreateAgentBuildAPIResponse(BaseModel):
    status: bool
    data: Optional[AgentBuild] = Field(default=None)
    errors: Optional[List[str]] = Field(default=None)


class AgentBuildDetail(BaseModel):
    id: str
    agent_id: str = Field(..., alias="agentId")
    status: AgentBuildStatus
    image_uri: Optional[str] = Field(default=None, alias="imageUri")
    websocket_url: Optional[str] = Field(default=None, alias="websocketUrl")
    error_message: Optional[str] = Field(default=None, alias="errorMessage")
    build_logs: Optional[List[str]] = Field(default=None, alias="buildLogs")
    created_at: str = Field(..., alias="createdAt")
    updated_at: str = Field(..., alias="updatedAt")


class GetAgentBuildData(BaseModel):
    build: AgentBuildDetail


class GetAgentBuildAPIResponse(BaseModel):
    status: bool
    data: Optional[GetAgentBuildData] = Field(default=None)
    errors: Optional[List[str]] = Field(default=None)


class AgentBuildListItem(BaseModel):
    id: str
    agent_id: str = Field(..., alias="agentId")
    status: AgentBuildStatus
    image_uri: Optional[str] = Field(default=None, alias="imageUri")
    websocket_url: Optional[str] = Field(default=None, alias="websocketUrl")
    error_message: Optional[str] = Field(default=None, alias="errorMessage")
    is_live: Optional[bool] = Field(default=None, alias="isLive")
    created_at: str = Field(..., alias="createdAt")
    updated_at: str = Field(..., alias="updatedAt")


class Pagination(BaseModel):
    limit: int
    offset: int
    total: int


class ListAgentBuildsData(BaseModel):
    builds: List[AgentBuildListItem]
    pagination: Pagination


class ListAgentBuildsAPIResponse(BaseModel):
    status: bool
    data: Optional[ListAgentBuildsData] = Field(default=None)
    errors: Optional[List[str]] = Field(default=None)


class DeleteAgentDeploymentData(BaseModel):
    message: str
    agent_id: str = Field(..., alias="agentId")


class DeleteAgentDeploymentAPIResponse(BaseModel):
    status: bool
    data: Optional[DeleteAgentDeploymentData] = Field(default=None)
    errors: Optional[List[str]] = Field(default=None)


class UpdateAgentBuildData(BaseModel):
    message: str


class UpdateAgentBuildAPIResponse(BaseModel):
    status: bool
    data: Optional[UpdateAgentBuildData] = Field(default=None)
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
                f"{self.base_url}/api/v1/agent?page={page}&offset={offset}&sortField={sort_field}&sortOrder={sort_order}&type=single_prompt",
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

            account_details_response = AccountDetailsAPIResponse.model_validate(
                response.json()
            )

            if (
                account_details_response.status is False
                or account_details_response.data is None
            ):
                raise Exception(account_details_response.errors)

            return account_details_response.data

    async def create_agent_build(
        self,
        agent_id: str,
        entry_point_file_name: str,
        agent_code_zip: str,
        api_key: str,
    ):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/v1/sdk/agents/{agent_id}/builds",
                headers={
                    "Authorization": f"Bearer {api_key}",
                },
                json={
                    "entryPointFileName": entry_point_file_name,
                    "agentCodeZip": agent_code_zip,
                },
            )

            response.raise_for_status()

            create_agent_build_response = CreateAgentBuildAPIResponse.model_validate(
                response.json()
            )

            if (
                create_agent_build_response.status is False
                or create_agent_build_response.data is None
            ):
                raise Exception(create_agent_build_response.errors)

            return create_agent_build_response.data

    async def list_agent_builds(
        self,
        agent_id: str,
        api_key: str,
        limit: int = 50,
        offset: int = 0,
    ) -> ListAgentBuildsData:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/api/v1/sdk/agents/{agent_id}/builds",
                headers={
                    "Authorization": f"Bearer {api_key}",
                },
                params={
                    "limit": limit,
                    "offset": offset,
                },
            )

            response.raise_for_status()

            list_builds_response = ListAgentBuildsAPIResponse.model_validate(
                response.json()
            )

            if (
                list_builds_response.status is False
                or list_builds_response.data is None
            ):
                raise Exception(list_builds_response.errors)

            return list_builds_response.data

    async def get_agent_build(
        self,
        agent_id: str,
        build_id: str,
        api_key: str,
    ) -> AgentBuildDetail:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/api/v1/sdk/agents/{agent_id}/builds/{build_id}",
                headers={
                    "Authorization": f"Bearer {api_key}",
                },
            )

            response.raise_for_status()

            get_build_response = GetAgentBuildAPIResponse.model_validate(
                response.json()
            )

            if get_build_response.status is False or get_build_response.data is None:
                raise Exception(get_build_response.errors)

            return get_build_response.data.build

    async def update_agent_build(
        self,
        agent_id: str,
        build_id: str,
        api_key: str,
        is_live: bool,
    ) -> UpdateAgentBuildData:
        async with httpx.AsyncClient() as client:
            response = await client.patch(
                f"{self.base_url}/api/v1/sdk/agents/{agent_id}/builds/{build_id}",
                headers={
                    "Authorization": f"Bearer {api_key}",
                },
                json={
                    "isLive": is_live,
                },
            )

            response.raise_for_status()

            update_build_response = UpdateAgentBuildAPIResponse.model_validate(
                response.json()
            )

            if (
                update_build_response.status is False
                or update_build_response.data is None
            ):
                raise Exception(update_build_response.errors)

            return update_build_response.data

    # async def stream_agent_build(
    #     self,
    #     agent_id: str,
    #     build_id: str,
    #     api_key: str,
    # ):
    #     """
    #     Stream build logs using Server-Sent Events.
    #     Yields tuples of (event_type, data) where event_type is 'log', 'status', or 'error'.
    #     """
    #     async with httpx.AsyncClient(timeout=None) as client:
    #         async with client.stream(
    #             "GET",
    #             f"{self.base_url}/api/v1/sdk/agents/{agent_id}/builds/{build_id}/stream",
    #             headers={
    #                 "Authorization": f"Bearer {api_key}",
    #             },
    #         ) as response:
    #             response.raise_for_status()
    #             async for line in response.aiter_lines():
    #                 if line.startswith("data: "):
    #                     import json

    #                     data = json.loads(line[6:])
    #                     yield data
