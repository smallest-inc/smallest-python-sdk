from typing import Dict, List, Optional, Tuple, Union, Any
from typing_extensions import Annotated
from pydantic import StrictFloat, StrictStr, StrictInt, StrictBytes, Field, validate_call

from smallestai.atoms.configuration import Configuration
from smallestai.atoms.api.agents_api import AgentsApi
from smallestai.atoms.api.knowledge_base_api import KnowledgeBaseApi
from smallestai.atoms.api.calls_api import CallsApi
from smallestai.atoms.models.create_agent_request import CreateAgentRequest
from smallestai.atoms.models.update_agent_request import UpdateAgentRequest
from smallestai.atoms.models.create_knowledge_base_request import CreateKnowledgeBaseRequest
from smallestai.atoms.models.upload_text_to_knowledge_base_request import UploadTextToKnowledgeBaseRequest
from smallestai.atoms.models.start_outbound_call_request import StartOutboundCallRequest
from smallestai.atoms.api_client import ApiClient
from smallestai.atoms.api.user_api import UserApi
from smallestai.atoms.api.organization_api import OrganizationApi
from smallestai.atoms.models.get_current_user200_response import GetCurrentUser200Response
from smallestai.atoms.models.get_organization200_response import GetOrganization200Response
from smallestai.atoms.api.campaigns_api import CampaignsApi
from smallestai.atoms.models.create_campaign_request import CreateCampaignRequest
from smallestai.atoms.models.get_campaigns_request import GetCampaignsRequest
from smallestai.atoms.api.agent_templates_api import AgentTemplatesApi
from smallestai.atoms.models.create_agent_from_template_request import CreateAgentFromTemplateRequest
from smallestai.atoms.api.logs_api import LogsApi
from smallestai.atoms.models.get_conversation_logs200_response import GetConversationLogs200Response

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
        return self.agents_api.create_agent(
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
        return self.agents_api.delete_agent(
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
        return self.agents_api.get_agent_by_id(
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
        return self.agents_api.get_agents(
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
        update_agent_request: UpdateAgentRequest,
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
        return self.agents_api.update_agent(
            id=id,
            update_agent_request=update_agent_request,
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
        create_knowledge_base_request: CreateKnowledgeBaseRequest,
        _request_timeout: Union[None, Annotated[StrictFloat, Field(gt=0)], Tuple[Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]]] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ):
        return self.knowledge_base_api.create_knowledge_base(
            create_knowledge_base_request=create_knowledge_base_request,
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
        return self.knowledge_base_api.delete_knowledge_base(
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
        return self.knowledge_base_api.get_knowledge_base_by_id(
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
        return self.knowledge_base_api.get_knowledge_bases(
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
        upload_text_to_knowledge_base_request: UploadTextToKnowledgeBaseRequest,
        _request_timeout: Union[None, Annotated[StrictFloat, Field(gt=0)], Tuple[Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]]] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ):
        return self.knowledge_base_api.upload_text_to_knowledge_base(
            id=id,
            upload_text_to_knowledge_base_request=upload_text_to_knowledge_base_request,
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
        return self.knowledge_base_api.upload_media_to_knowledge_base(
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
        return self.knowledge_base_api.get_knowledge_base_items(
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
        return self.knowledge_base_api.delete_knowledge_base_item(
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
        start_outbound_call_request: StartOutboundCallRequest,
        _request_timeout: Union[None, Annotated[StrictFloat, Field(gt=0)], Tuple[Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]]] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ):
        return self.calls_api.start_outbound_call(
            start_outbound_call_request=start_outbound_call_request,
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
    ) -> GetCurrentUser200Response:
        return self.user_api.get_current_user(
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
    ) -> GetOrganization200Response:
        return self.organization_api.get_organization(
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
        create_campaign_request: CreateCampaignRequest,
        _request_timeout: Union[None, Annotated[StrictFloat, Field(gt=0)], Tuple[Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]]] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ):
        return self.campaigns_api.create_campaign(
            create_campaign_request=create_campaign_request,
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
        return self.campaigns_api.delete_campaign(
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
        return self.campaigns_api.get_campaign_by_id(
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
        get_campaigns_request: GetCampaignsRequest,
        _request_timeout: Union[None, Annotated[StrictFloat, Field(gt=0)], Tuple[Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]]] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ):
        return self.campaigns_api.get_campaigns(
            get_campaigns_request=get_campaigns_request,
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
        return self.campaigns_api.start_campaign(
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
        return self.campaigns_api.pause_campaign(
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
        return self.agent_templates_api.get_agent_templates(
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
        return self.agent_templates_api.create_agent_from_template(
            create_agent_from_template_request=create_agent_from_template_request,
            _request_timeout=_request_timeout,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

    @validate_call
    def get_conversation_logs(
        self,
        id: StrictStr,
        _request_timeout: Union[None, Annotated[StrictFloat, Field(gt=0)], Tuple[Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]]] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> GetConversationLogs200Response:
        return self.logs_api.get_conversation_logs(
            id=id,
            _request_timeout=_request_timeout,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )
