from typing import Dict, List, Optional, Tuple, Union, Any
from typing_extensions import Annotated
from pydantic import StrictFloat, StrictStr, StrictInt, Field, validate_call

from smallestai.atoms.api.agents_api import AgentsApi
from smallestai.atoms.api.knowledge_base_api import KnowledgeBaseApi
from smallestai.atoms.api.calls_api import CallsApi
from smallestai.atoms.models.create_agent_request import CreateAgentRequest
from smallestai.atoms.models.update_agent_request import UpdateAgentRequest
from smallestai.atoms.models.create_knowledge_base_request import CreateKnowledgeBaseRequest
from smallestai.atoms.models.upload_text_to_knowledge_base_request import UploadTextToKnowledgeBaseRequest
from smallestai.atoms.models.start_outbound_call_request import StartOutboundCallRequest
from smallestai.atoms.api_client import ApiClient

class AtomsClient:
    def __init__(self, api_client=None) -> None:
        if api_client is None:
            api_client = ApiClient.get_default()
        self.api_client = api_client
        self.agents_api = AgentsApi(api_client)
        self.knowledge_base_api = KnowledgeBaseApi(api_client)
        self.calls_api = CallsApi(api_client)

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
