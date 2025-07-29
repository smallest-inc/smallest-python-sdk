"""
SmallestAI Python SDK

This package provides access to both the Atoms API (agent management)
and Waves API components.
"""

from smallestai.atoms import (
    AgentTemplatesApi,
    AgentsApi,
    CallsApi,
    CampaignsApi,
    KnowledgeBaseApi,
    LogsApi,
    OrganizationApi,
    UserApi,
    ApiResponse,
    ApiClient,
    Configuration,
    OpenApiException,
    ApiTypeError,
    ApiValueError,
    ApiKeyError,
    ApiAttributeError,
    ApiException,
    AgentDTO,
    AgentDTOLanguage,
    AgentDTOSynthesizer,
    AgentDTOSynthesizerVoiceConfig,
    BadRequestErrorResponse,
    AgentFromTemplatePost200Response,
    CreateAgentFromTemplateRequest,
    CreateAgentRequest,
    CreateAgentRequestLanguage,
    CreateAgentRequestLanguageSynthesizer,
    CreateAgentRequestLanguageSynthesizerVoiceConfig,
    CampaignPost201Response,
    CampaignPostRequest,
    CampaignGetRequest,
    AgentIdDelete200Response,
    AgentIdGet200Response,
    AgentTemplateGet200Response,
    AgentTemplateGet200ResponseDataInner,
    AgentGet200Response,
    CampaignIdGet200Response,
    CampaignGet200Response,
    ConversationIdGet200Response,
    ConversationIdGet200ResponseData,
    UserGet200Response,
    UserGet200ResponseData,
    KnowledgebaseIdGet200Response,
    KnowledgebasePost201Response,
    KnowledgebasePostRequest,
    KnowledgebaseIdItemsUploadTextPostRequest,
    OrganizationGet200Response,
    OrganizationGet200ResponseData,
    OrganizationGet200ResponseDataMembersInner,
    OrganizationGet200ResponseDataSubscription,
    InternalServerErrorResponse,
    ConversationOutboundPost200Response,
    ConversationOutboundPost200ResponseData,
    ConversationOutboundPostRequest,
    UnauthorizedErrorReponse,
    AgentIdPatch200Response,
    AgentIdPatchRequest,
    AgentIdPatchRequestLanguage,
    AgentIdPatchRequestSynthesizer,
    AgentIdPatchRequestSynthesizerVoiceConfig,
    AgentIdPatchRequestSynthesizerVoiceConfigOneOf,
    AgentIdPatchRequestSynthesizerVoiceConfigOneOf1,
    AtomsClient
)

from smallestai.waves import (
    WavesClient,
    AsyncWavesClient,
    WavesStreamingTTS
)

from smallestai.atoms import __all__ as atoms_all
from smallestai.waves import __all__ as waves_all

__all__ = atoms_all + waves_all

__version__ = "4.0.1"