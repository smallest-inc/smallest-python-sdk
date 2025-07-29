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
from smallestai.atoms.models.create_agent_from_template_request import CreateAgentFromTemplateRequest
from smallestai.atoms.api.logs_api import LogsApi
from smallestai.atoms.models.conversation_id_get200_response import ConversationIdGet200Response

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

    @validate_call
    def delete_agent(
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
        return self.agents_api.agent_id_delete(
            id=id,
            _request_timeout=_request_timeout,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

    @validate_call
    def get_agent_by_id(
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
        return self.agents_api.agent_id_get(
            id=id,
            _request_timeout=_request_timeout,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

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

    @validate_call
    def get_campaign_by_id(
        self,
        id: StrictStr,
        _request_timeout: Union[None, Annotated[StrictFloat, Field(gt=0)], Tuple[Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]]] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ):
        return self.campaigns_api.campaign_id_get(
            id=id,
            _request_timeout=_request_timeout,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

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

    @validate_call
    def start_campaign(
        self,
        id: StrictStr,
        _request_timeout: Union[None, Annotated[StrictFloat, Field(gt=0)], Tuple[Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]]] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ):
        return self.campaigns_api.campaign_id_start_post(
            id=id,
            _request_timeout=_request_timeout,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

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
