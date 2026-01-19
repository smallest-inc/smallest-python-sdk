from typing import Dict, List, Optional, Tuple, Union, Any
from typing_extensions import Annotated
from pydantic import StrictFloat, StrictStr, StrictInt, StrictBytes, Field, validate_call

from smallestai.atoms.configuration import Configuration
from smallestai.atoms.api.agents_api import AgentsApi
from smallestai.atoms.api.knowledge_base_api import KnowledgeBaseApi
from smallestai.atoms.api.calls_api import CallsApi
from smallestai.atoms.models.create_agent_request import CreateAgentRequest
from smallestai.atoms.models.agent_id_patch_request import AgentIdPatchRequest
from smallestai.atoms.models.knowledgebase_post_request import KnowledgebasePostRequest
from smallestai.atoms.models.knowledgebase_id_items_upload_text_post_request import KnowledgebaseIdItemsUploadTextPostRequest
from smallestai.atoms.models.conversation_outbound_post_request import ConversationOutboundPostRequest
from smallestai.atoms.api_client import ApiClient
from smallestai.atoms.api.user_api import UserApi
from smallestai.atoms.api.organization_api import OrganizationApi
from smallestai.atoms.models.user_get200_response import UserGet200Response
from smallestai.atoms.models.organization_get200_response import OrganizationGet200Response
from smallestai.atoms.api.campaigns_api import CampaignsApi
from smallestai.atoms.models.campaign_post_request import CampaignPostRequest
from smallestai.atoms.models.campaign_get_request import CampaignGetRequest
from smallestai.atoms.api.agent_templates_api import AgentTemplatesApi
from smallestai.atoms.api.logs_api import LogsApi
from smallestai.atoms.models.create_agent_from_template_request import CreateAgentFromTemplateRequest
from smallestai.atoms.models.conversation_id_get200_response import ConversationIdGet200Response
# New modular managers (flat structure)
from smallestai.atoms.call import Call
from smallestai.atoms.audience import Audience
from smallestai.atoms.campaign import Campaign
from smallestai.atoms.kb import KB

class AtomsClient:
    def __init__(self, configuration=None) -> None:
        if configuration is None:
            configuration = Configuration.get_default()
        
        self.api_client = ApiClient(configuration)
        self.agents_api = AgentsApi(self.api_client)
        self.knowledge_base_api = KnowledgeBaseApi(self.api_client)
        self.calls_api = CallsApi(self.api_client)
        self.user_api = UserApi(self.api_client)
        self.organization_api = OrganizationApi(self.api_client)
        self.campaigns_api = CampaignsApi(self.api_client)
        self.agent_templates_api = AgentTemplatesApi(self.api_client)
        self.logs_api = LogsApi(self.api_client)
        
        # Initialize modular managers
        base_url = self.api_client.configuration.host
        self._call = Call(base_url)
        self._audience = Audience(base_url)
        self._campaign = Campaign(base_url)
        self._kb = KB(base_url)

    # ================================================================
    # Module Properties (Flat API)
    # ================================================================

    @property
    def call(self):
        """Call management and analytics."""
        return self._call
    
    @property
    def audience(self):
        """Audience management."""
        return self._audience

    @property
    def campaign(self):
        """Campaign management."""
        return self._campaign
        
    @property
    def kb(self):
        """Knowledge Base management."""
        return self._kb

    # Agent Methods
    @validate_call
    def create_agent(
        self,
        create_agent_request: CreateAgentRequest,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ):
        return self.agents_api.agent_post(
            create_agent_request=create_agent_request,
            _request_timeout=_request_timeout,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

    def delete_agent(
        self,
        id: str,
        **kwargs
    ):
        """
        Delete (archive) an agent by ID.
        
        Note: Backend uses /agent/{id}/archive endpoint.
        """
        import requests
        url = f"{self._get_base_url()}/agent/{id}/archive"
        headers = self._get_auth_headers()
        
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_agent_by_id(
        self,
        id: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Get agent by ID with full details.
        
        Returns:
            Dict with agent details including globalKnowledgeBaseId
        """
        import requests
        url = f"{self._get_base_url()}/agent/{id}"
        headers = self._get_auth_headers()
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    @validate_call
    def get_agents(
        self,
        page: Optional[StrictInt] = None,
        offset: Optional[StrictInt] = None,
        search: Optional[StrictStr] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ):
        return self.agents_api.agent_get(
            page=page,
            offset=offset,
            search=search,
            _request_timeout=_request_timeout,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

    @validate_call
    def update_agent(
        self,
        id: StrictStr,
        agent_id_patch_request: AgentIdPatchRequest,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ):
        return self.agents_api.agent_id_patch(
            id=id,
            agent_id_patch_request=agent_id_patch_request,
            _request_timeout=_request_timeout,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

    @validate_call
    def get_agent_workflow(
        self,
        id: StrictStr,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ):
        return self.agents_api.agent_id_workflow_get(
            id=id,
            _request_timeout=_request_timeout,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

    # Knowledge Base Methods
    @validate_call
    def create_knowledge_base(
        self,
        knowledgebase_post_request: KnowledgebasePostRequest,
        _request_timeout: Union[None, Annotated[StrictFloat, Field(gt=0)], Tuple[Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]]] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ):
        return self.knowledge_base_api.knowledgebase_post(
            knowledgebase_post_request=knowledgebase_post_request,
            _request_timeout=_request_timeout,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

    @validate_call
    def delete_knowledge_base(
        self,
        id: StrictStr,
        _request_timeout: Union[None, Annotated[StrictFloat, Field(gt=0)], Tuple[Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]]] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ):
        return self.knowledge_base_api.knowledgebase_id_delete(
            id=id,
            _request_timeout=_request_timeout,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

    @validate_call
    def get_knowledge_base_by_id(
        self,
        id: StrictStr,
        _request_timeout: Union[None, Annotated[StrictFloat, Field(gt=0)], Tuple[Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]]] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ):
        return self.knowledge_base_api.knowledgebase_id_get(
            id=id,
            _request_timeout=_request_timeout,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

    @validate_call
    def get_knowledge_bases(
        self,
        _request_timeout: Union[None, Annotated[StrictFloat, Field(gt=0)], Tuple[Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]]] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ):
        return self.knowledge_base_api.knowledgebase_get(
            _request_timeout=_request_timeout,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

    @validate_call
    def upload_text_to_knowledge_base(
        self,
        id: StrictStr,
        knowledgebase_id_items_upload_text_post_request: KnowledgebaseIdItemsUploadTextPostRequest,
        _request_timeout: Union[None, Annotated[StrictFloat, Field(gt=0)], Tuple[Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]]] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ):
        return self.knowledge_base_api.knowledgebase_id_items_upload_text_post(
            id=id,
            knowledgebase_id_items_upload_text_post_request=knowledgebase_id_items_upload_text_post_request,
            _request_timeout=_request_timeout,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

    @validate_call
    def upload_media_to_knowledge_base(
        self,
        id: StrictStr,
        media: Union[StrictBytes, StrictStr, Tuple[StrictStr, StrictBytes]],
        _request_timeout: Union[None, Annotated[StrictFloat, Field(gt=0)], Tuple[Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]]] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ):
        return self.knowledge_base_api.knowledgebase_id_items_upload_media_post(
            id=id,
            media=media,
            _request_timeout=_request_timeout,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

    @validate_call
    def get_knowledge_base_items(
        self,
        id: StrictStr,
        _request_timeout: Union[None, Annotated[StrictFloat, Field(gt=0)], Tuple[Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]]] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ):
        return self.knowledge_base_api.knowledgebase_id_items_get(
            id=id,
            _request_timeout=_request_timeout,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

    @validate_call
    def delete_knowledge_base_item(
        self,
        knowledge_base_id: StrictStr,
        knowledge_base_item_id: StrictStr,
        _request_timeout: Union[None, Annotated[StrictFloat, Field(gt=0)], Tuple[Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]]] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ):
        return self.knowledge_base_api.knowledgebase_knowledge_base_id_items_knowledge_base_item_id_delete(
            knowledge_base_id=knowledge_base_id,
            knowledge_base_item_id=knowledge_base_item_id,
            _request_timeout=_request_timeout,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

    # Calls Methods
    @validate_call
    def start_outbound_call(
        self,
        conversation_outbound_post_request: ConversationOutboundPostRequest,
        _request_timeout: Union[None, Annotated[StrictFloat, Field(gt=0)], Tuple[Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]]] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ):
        return self.calls_api.conversation_outbound_post(
            conversation_outbound_post_request=conversation_outbound_post_request,
            _request_timeout=_request_timeout,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

    # User Methods
    @validate_call
    def get_current_user(
        self,
        _request_timeout: Union[None, Annotated[StrictFloat, Field(gt=0)], Tuple[Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]]] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> UserGet200Response:
        return self.user_api.user_get(
            _request_timeout=_request_timeout,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

    # Organization Methods
    @validate_call
    def get_organization(
        self,
        _request_timeout: Union[None, Annotated[StrictFloat, Field(gt=0)], Tuple[Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]]] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> OrganizationGet200Response:
        return self.organization_api.organization_get(
            _request_timeout=_request_timeout,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

    # Campaign Methods
    @validate_call
    def create_campaign(
        self,
        campaign_post_request: CampaignPostRequest,
        _request_timeout: Union[None, Annotated[StrictFloat, Field(gt=0)], Tuple[Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]]] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ):
        return self.campaigns_api.campaign_post(
            campaign_post_request=campaign_post_request,
            _request_timeout=_request_timeout,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

    @validate_call
    def delete_campaign(
        self,
        id: StrictStr,
        _request_timeout: Union[None, Annotated[StrictFloat, Field(gt=0)], Tuple[Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]]] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ):
        return self.campaigns_api.campaign_id_delete(
            id=id,
            _request_timeout=_request_timeout,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

    def get_campaign_by_id(
        self,
        id: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Get campaign by ID with full status and metrics.
        
        Returns:
            Dict with campaign details, status, and metrics
        """
        import requests
        url = f"{self._get_base_url()}/campaign/{id}"
        headers = self._get_auth_headers()
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    @validate_call
    def get_campaigns(
        self,
        campaign_get_request: CampaignGetRequest,
        _request_timeout: Union[None, Annotated[StrictFloat, Field(gt=0)], Tuple[Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]]] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ):
        return self.campaigns_api.campaign_get(
            campaign_get_request=campaign_get_request,
            _request_timeout=_request_timeout,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

    def start_campaign(
        self,
        id: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Start a campaign by ID.
        
        Returns:
            Dict with message, taskId, and campaignId
        """
        import requests
        url = f"{self._get_base_url()}/campaign/{id}/start"
        headers = self._get_auth_headers()
        
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        return response.json()

    @validate_call
    def pause_campaign(
        self,
        id: StrictStr,
        _request_timeout: Union[None, Annotated[StrictFloat, Field(gt=0)], Tuple[Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]]] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ):
        return self.campaigns_api.campaign_id_pause_post(
            id=id,
            _request_timeout=_request_timeout,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

    # Agent Template Methods
    @validate_call
    def get_agent_templates(
        self,
        _request_timeout: Union[None, Annotated[StrictFloat, Field(gt=0)], Tuple[Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]]] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ):
        return self.agent_templates_api.agent_template_get(
            _request_timeout=_request_timeout,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

    @validate_call
    def create_agent_from_template(
        self,
        create_agent_from_template_request: CreateAgentFromTemplateRequest,
        _request_timeout: Union[None, Annotated[StrictFloat, Field(gt=0)], Tuple[Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]]] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ):
        return self.agent_templates_api.agent_from_template_post(
            create_agent_from_template_request=create_agent_from_template_request,
            _request_timeout=_request_timeout,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

    # Logs Methods
    @validate_call
    def get_conversation_logs(
        self,
        id: StrictStr,
        _request_timeout: Union[None, Annotated[StrictFloat, Field(gt=0)], Tuple[Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]]] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> ConversationIdGet200Response:
        return self.logs_api.conversation_id_get(
            id=id,
            _request_timeout=_request_timeout,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

    # ================================================================
    # Call Analytics Methods (using direct HTTP calls for JSON response)
    # ================================================================
    
    def get_call(self, call_id: str) -> Dict[str, Any]:
        """
        Get details for a single call by call ID.
        
        Args:
            call_id: The call ID (e.g., "CALL-1768155029217-0bae45")
        
        Returns:
            Dict with status and data containing call details including:
            - callId, duration, status, type
            - transcript, recordingUrl, recordingDualUrl
            - from, to, events, callCost
        """
        import requests
        import os
        api_key = os.environ.get("SMALLEST_API_KEY", "")
        url = f"{self.api_client.configuration.host}/conversation/{call_id}"
        
        response = requests.get(url, headers={"Authorization": f"Bearer {api_key}"})
        response.raise_for_status()
        return response.json()
    
    def get_calls(
        self,
        agent_id: Optional[str] = None,
        campaign_id: Optional[str] = None,
        page: int = 1,
        limit: int = 10,
        status: Optional[str] = None,
        call_type: Optional[str] = None,
        search: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get paginated list of calls with optional filters.
        
        Args:
            agent_id: Filter by agent ID
            campaign_id: Filter by campaign ID
            page: Page number (default: 1)
            limit: Results per page (default: 10)
            status: Filter by status (completed, failed, in_progress, etc.)
            call_type: Filter by type (telephony_inbound, telephony_outbound, chat)
            search: Search by callId, fromNumber, or toNumber
        
        Returns:
            Dict with status and data containing paginated call logs
        """
        import requests
        import os
        api_key = os.environ.get("SMALLEST_API_KEY", "")
        url = f"{self.api_client.configuration.host}/conversation"
        
        params = {"page": page, "limit": limit}
        if agent_id:
            params["agentIds"] = agent_id
        if campaign_id:
            params["campaignIds"] = campaign_id
        if status:
            params["statusFilter"] = status
        if call_type:
            params["callTypes"] = call_type
        if search:
            params["search"] = search
        
        response = requests.get(url, headers={"Authorization": f"Bearer {api_key}"}, params=params)
        response.raise_for_status()
        return response.json()
    
    def search_calls(self, call_ids: List[str]) -> Dict[str, Any]:
        """
        Search for multiple calls by their call IDs.
        
        Args:
            call_ids: List of call IDs to fetch (max 100)
        
        Returns:
            Dict with status and data containing matching call logs
        """
        import requests
        import os
        api_key = os.environ.get("SMALLEST_API_KEY", "")
        url = f"{self.api_client.configuration.host}/conversation/search"
        
        response = requests.post(
            url,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={"callIds": call_ids}
        )
        response.raise_for_status()
        return response.json()

    # ================================================================
    # Post-Call Analytics Methods
    # ================================================================
    
    def get_post_call_config(self, agent_id: str) -> Dict[str, Any]:
        """
        Get post-call analytics configuration for an agent.
        
        Args:
            agent_id: The agent ID
        
        Returns:
            Dict with status and data containing:
            - summaryPrompt: Custom prompt for generating call summaries
            - dispositionMetrics: List of configured disposition metrics
        """
        import requests
        import os
        api_key = os.environ.get("SMALLEST_API_KEY", "")
        url = f"{self.api_client.configuration.host}/agent/{agent_id}/post-call-analytics"
        
        response = requests.get(url, headers={"Authorization": f"Bearer {api_key}"})
        response.raise_for_status()
        return response.json()
    
    def set_post_call_config(
        self,
        agent_id: str,
        summary_prompt: str = None,
        disposition_metrics: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Set post-call analytics configuration for an agent.
        
        Args:
            agent_id: The agent ID
            summary_prompt: Custom prompt for generating call summaries
            disposition_metrics: List of disposition metrics to track. Each metric should have:
                - identifier: Unique ID (e.g., "customer_status")
                - dispositionMetricPrompt: Question to extract this data
                - dispositionValues: Dict with "type" key (STRING, BOOLEAN, INTEGER, ENUM, DATETIME)
                - choices: List of options (required only for ENUM type)
        
        Returns:
            Dict with status and updated configuration
        
        Example:
            client.set_post_call_config(
                agent_id="123",
                summary_prompt="Summarize the key outcomes of this call.",
                disposition_metrics=[
                    {
                        "identifier": "customer_status",
                        "dispositionMetricPrompt": "What is the customer's interest level?",
                        "dispositionValues": {"type": "ENUM"},
                        "choices": ["Interested", "Not Interested", "Callback"]
                    },
                    {
                        "identifier": "customer_name",
                        "dispositionMetricPrompt": "What is the customer's name?",
                        "dispositionValues": {"type": "STRING"}
                    }
                ]
            )
        """
        import requests
        import os
        api_key = os.environ.get("SMALLEST_API_KEY", "")
        url = f"{self.api_client.configuration.host}/agent/{agent_id}/post-call-analytics"
        
        payload = {}
        if summary_prompt is not None:
            payload["summaryPrompt"] = summary_prompt
        if disposition_metrics is not None:
            payload["dispositionMetrics"] = disposition_metrics
        
        response = requests.post(
            url,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json=payload
        )
        response.raise_for_status()
        return response.json()

    # ================================================================
    # Audience Methods (using direct HTTP calls)
    # ================================================================
    
    def _get_auth_headers(self) -> Dict[str, str]:
        """Get authorization headers for direct API calls."""
        import os
        api_key = os.environ.get("SMALLEST_API_KEY", "")
        return {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def _get_base_url(self) -> str:
        """Get base API URL."""
        return self.api_client.configuration.host
    
    def get_audiences(self) -> Dict[str, Any]:
        """
        Get all audiences for the organization.
        
        Returns:
            Dict with status and data containing list of audiences
        """
        import requests
        url = f"{self._get_base_url()}/audience"
        headers = self._get_auth_headers()
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def get_audience_by_id(self, audience_id: str) -> Dict[str, Any]:
        """
        Get audience by ID.
        
        Args:
            audience_id: The audience ID
            
        Returns:
            Dict with status and audience data
        """
        import requests
        url = f"{self._get_base_url()}/audience/{audience_id}"
        headers = self._get_auth_headers()
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def create_audience(
        self,
        name: str,
        phone_numbers: List[str],
        phone_number_column_name: str = "phoneNumber",
        description: str = "",
        names: Optional[List[Tuple[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Create a new audience with phone numbers.
        
        Args:
            name: Name of the audience
            phone_numbers: List of phone numbers to add (e.g., ["+916366821717", "+919353662554"])
            phone_number_column_name: Column name for phone numbers in CSV (default: "phoneNumber")
            description: Optional description
            names: Optional list of (firstName, lastName) tuples matching phone_numbers
            
        Returns:
            Dict with status and created audience data including _id
            
        Example:
            audience = client.create_audience(
                name="My Audience",
                phone_numbers=["+916366821717", "+919353662554"],
                names=[("John", "Doe"), ("Jane", "Smith")]
            )
            audience_id = audience["data"]["_id"]
        """
        import requests
        import io
        
        url = f"{self._get_base_url()}/audience"
        headers = {"Authorization": self._get_auth_headers()["Authorization"]}
        
        # Build CSV content
        csv_lines = ["firstName,lastName,phoneNumber"]
        for i, phone in enumerate(phone_numbers):
            if names and i < len(names):
                first_name, last_name = names[i]
            else:
                first_name, last_name = "User", str(i + 1)
            csv_lines.append(f"{first_name},{last_name},{phone}")
        
        csv_content = "\n".join(csv_lines)
        
        files = {'file': ('contacts.csv', csv_content.encode('utf-8'), 'text/csv')}
        data = {
            'name': name,
            'phoneNumberColumnName': phone_number_column_name,
            'description': description
        }
        
        response = requests.post(url, headers=headers, files=files, data=data)
        response.raise_for_status()
        return response.json()
    
    def delete_audience(self, audience_id: str) -> Dict[str, Any]:
        """
        Delete an audience by ID.
        
        Args:
            audience_id: The audience ID to delete
            
        Returns:
            Dict with status
        """
        import requests
        url = f"{self._get_base_url()}/audience/{audience_id}"
        headers = self._get_auth_headers()
        
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def get_audience_members(
        self,
        audience_id: str,
        page: int = 1,
        offset: int = 10
    ) -> Dict[str, Any]:
        """
        Get members of an audience.
        
        Args:
            audience_id: The audience ID
            page: Page number (default: 1)
            offset: Items per page (default: 10)
            
        Returns:
            Dict with status and members data
        """
        import requests
        url = f"{self._get_base_url()}/audience/{audience_id}/members"
        headers = self._get_auth_headers()
        params = {"page": str(page), "offset": str(offset)}
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def add_audience_members(
        self,
        audience_id: str,
        members: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Add members to an existing audience.
        
        Args:
            audience_id: The audience ID
            members: List of member dicts with phoneNumber and optional firstName, lastName
            
        Returns:
            Dict with status and count of added/skipped members
            
        Example:
            result = client.add_audience_members(
                audience_id="123abc",
                members=[
                    {"phoneNumber": "+919353662554", "firstName": "New", "lastName": "User"}
                ]
            )
        """
        import requests
        url = f"{self._get_base_url()}/audience/{audience_id}/members"
        headers = self._get_auth_headers()
        
        response = requests.post(url, headers=headers, json={"members": members})
        response.raise_for_status()
        return response.json()
    
    # ================================================================
    # Phone Number Methods
    # ================================================================
    
    def get_phone_numbers(self) -> Dict[str, Any]:
        """
        Get all acquired phone numbers for the organization.
        
        Returns:
            Dict with status and list of phone number products.
            Each product has:
            - _id: Phone number ID (use this in campaigns)
            - attributes.phoneNumber: The actual phone number
            - attributes.provider: Telephony provider
            - agentId: Assigned agent ID (if any)
            
        Example:
            numbers = client.get_phone_numbers()
            for num in numbers["data"]:
                print(f"ID: {num['_id']}, Phone: {num['attributes']['phoneNumber']}")
        """
        import requests
        url = f"{self._get_base_url()}/product/phone-numbers"
        headers = self._get_auth_headers()
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    # ================================================================
    # Simplified Wrapper Methods (cleaner API)
    # ================================================================
    
    def new_agent(
        self,
        name: str,
        prompt: str = None,
        description: str = "",
        kb_id: str = None,
        background_sound: str = ""
    ) -> Dict[str, Any]:
        """
        Create a new agent with simple parameters.
        
        Args:
            name: Agent name
            prompt: Global prompt for the agent
            description: Agent description
            kb_id: Knowledge base ID to link
            background_sound: '', 'office', 'cafe', 'call_center', or 'static'
        
        Returns:
            Dict with status and agent ID
        """
        from smallestai.atoms.models import CreateAgentRequest
        
        request = CreateAgentRequest(
            name=name,
            description=description,
            global_prompt=prompt,
            global_knowledge_base_id=kb_id,
            background_sound=background_sound
        )
        return self.create_agent(create_agent_request=request)
    
    def new_campaign(
        self,
        name: str,
        agent_id: str,
        audience_id: str,
        phone_ids: list,
        description: str = "",
        max_retries: int = 3,
        retry_delay: int = 15
    ) -> Dict[str, Any]:
        """
        Create a new campaign with simple parameters.
        
        Args:
            name: Campaign name
            agent_id: ID of the agent to use
            audience_id: ID of the audience to call
            phone_ids: List of outbound phone number IDs
            description: Campaign description
            max_retries: Max retry attempts (0-10)
            retry_delay: Minutes between retries (1-1440)
        
        Returns:
            Dict with campaign details
        """
        from smallestai.atoms.models import CampaignPostRequest
        
        request = CampaignPostRequest(
            name=name,
            description=description,
            agent_id=agent_id,
            audience_id=audience_id,
            phone_number_ids=phone_ids,
            max_retries=max_retries,
            retry_delay=retry_delay
        )
        return self.create_campaign(campaign_post_request=request)
    
    def new_kb(
        self,
        name: str,
        description: str = ""
    ) -> Dict[str, Any]:
        """
        Create a new knowledge base with simple parameters.
        
        Args:
            name: Knowledge base name
            description: Knowledge base description
        
        Returns:
            Dict with status and KB ID
        """
        from smallestai.atoms.models import KnowledgebasePostRequest
        
        request = KnowledgebasePostRequest(
            name=name,
            description=description
        )
        return self.create_knowledge_base(knowledgebase_post_request=request)
