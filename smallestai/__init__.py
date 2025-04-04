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
    CreateAgentFromTemplate200Response,
    CreateAgentFromTemplateRequest,
    CreateAgentRequest,
    CreateAgentRequestLanguage,
    CreateAgentRequestLanguageSynthesizer,
    CreateAgentRequestLanguageSynthesizerVoiceConfig,
    CreateCampaign201Response,
    CreateCampaign201ResponseData,
    CreateCampaignRequest,
    CreateKnowledgeBase201Response,
    CreateKnowledgeBaseRequest,
    DeleteAgent200Response,
    GetAgentById200Response,
    GetAgentTemplates200Response,
    GetAgentTemplates200ResponseDataInner,
    GetAgents200Response,
    GetAgents200ResponseData,
    GetCampaignById200Response,
    GetCampaignById200ResponseData,
    GetCampaigns200Response,
    GetCampaigns200ResponseDataInner,
    GetCampaigns200ResponseDataInnerAgent,
    GetCampaigns200ResponseDataInnerAudience,
    GetCampaignsRequest,
    GetConversationLogs200Response,
    GetConversationLogs200ResponseData,
    GetCurrentUser200Response,
    GetCurrentUser200ResponseData,
    GetKnowledgeBaseById200Response,
    GetKnowledgeBaseItems200Response,
    GetKnowledgeBases200Response,
    GetOrganization200Response,
    GetOrganization200ResponseData,
    GetOrganization200ResponseDataMembersInner,
    GetOrganization200ResponseDataSubscription,
    InternalServerErrorResponse,
    KnowledgeBaseDTO,
    KnowledgeBaseItemDTO,
    StartOutboundCall200Response,
    StartOutboundCall200ResponseData,
    StartOutboundCallRequest,
    UnauthorizedErrorReponse,
    UpdateAgent200Response,
    UpdateAgentRequest,
    UpdateAgentRequestLanguage,
    UpdateAgentRequestSynthesizer,
    UpdateAgentRequestSynthesizerVoiceConfig,
    UpdateAgentRequestSynthesizerVoiceConfigOneOf,
    UpdateAgentRequestSynthesizerVoiceConfigOneOf1,
    UploadTextToKnowledgeBaseRequest,
    AtomsClient
)

from smallestai.waves import (
    WavesClient,
    AsyncWavesClient,
    TextToAudioStream
)

from smallestai.atoms import __all__ as atoms_all
from smallestai.waves import __all__ as waves_all

__all__ = atoms_all + waves_all

__version__ = "3.0.0"