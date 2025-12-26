from datetime import datetime
from enum import Enum
from typing import Any, ClassVar, Dict, List, Literal, Optional, Tuple

from pydantic import BaseModel, ConfigDict, Field


class EventDirection(str, Enum):
    """Direction of an event"""

    DOWNSTREAM = "downstream"
    UPSTREAM = "upstream"


class TypedModel(BaseModel):
    _subtypes_: ClassVar[List[Tuple[Any, Any]]] = []

    def __init_subclass__(cls, type=None):  # type: ignore
        cls._subtypes_.append((type, cls))

    @classmethod
    def get_cls(_cls, type):
        for t, cls in _cls._subtypes_:
            if t == type:
                return cls
        raise ValueError(f"Unknown type {type}")

    @classmethod
    def get_type(_cls, cls_name):
        for t, cls in _cls._subtypes_:
            if cls.__name__ == cls_name:
                return t
        raise ValueError(f"Unknown class {cls_name}")

    @classmethod
    def parse_obj(cls, obj):
        data_type = obj.get("type")
        if data_type is None:
            raise ValueError(f"type is required for {cls.__name__}")

        sub = cls.get_cls(data_type)
        if sub is None:
            raise ValueError(f"Unknown type {data_type}")
        return sub(**obj)

    @property
    def type(self):
        return self.get_type(self.__class__.__name__)


class ConversationType(str, Enum):
    TELEPHONY_INBOUND = "telephonyInbound"
    TELEPHONY_OUTBOUND = "telephonyOutbound"
    CHAT = "chat"
    WEBCALL = "webcall"
    SUPERVISOR_AGENT = "supervisor_agent"


class SessionContext(BaseModel):
    initial_variables: Dict[str, Any]
    conversation_type: ConversationType


class OutputAgentSettings(BaseModel):
    interruptible: bool = True

    model_config = ConfigDict(extra="allow")


class EventType(str, Enum):
    """SDKEvent type enumeration"""

    BASE = "base"

    # system events
    SYSTEM_BASE = "system.base"
    SYSTEM_INIT = "system.init"
    SYSTEM_LLM_REQUEST = "system.llm.request"
    SYSTEM_USER_STARTED_SPEAKING = "system.user.started_speaking"
    SYSTEM_USER_STOPPED_SPEAKING = "system.user.stopped_speaking"
    SYSTEM_CONTROL_INTERRUPT = "system.control.interrupt"
    SYSTEM_UPDATE_OUTPUT_AGENT_SETTINGS = "system.output_agent.update_settings"
    SYSTEM_USER_JOINED = "system.user.joined"

    # agent events
    AGENT_BASE = "agent.base"
    AGENT_READY = "agent.ready"
    AGENT_ERROR = "agent.error"
    AGENT_LLM_RESPONSE_START = "agent.llm.response.start"
    AGENT_LLM_RESPONSE_CHUNK = "agent.llm.response.chunk"
    AGENT_LLM_RESPONSE_END = "agent.llm.response.end"
    AGENT_CONTROL_INTERRUPT = "agent.control.interrupt"
    AGENT_CONTROL_MUTE_USER = "agent.control.mute_user"
    AGENT_CONTROL_UNMUTE_USER = "agent.control.unmute_user"
    AGENT_TRANSCRIPT_UPDATE = "agent.transcript.update"
    AGENT_SPEAK = "agent.speak"

    AGENT_END_CALL = "agent.end_call"
    AGENT_TRANSFER_CONVERSATION = "agent.transfer_call"


class SDKEvent(TypedModel, type=EventType.BASE.value):
    timestamp: datetime = Field(default_factory=datetime.now)


class SDKSystemEvent(SDKEvent, type=EventType.SYSTEM_BASE.value):
    pass


class SDKAgentEvent(SDKEvent, type=EventType.AGENT_BASE.value):
    pass


class SDKAgentTranscriptUpdateEvent(
    SDKAgentEvent, type=EventType.AGENT_TRANSCRIPT_UPDATE.value
):
    role: Literal["user", "assistant"]
    content: str


class SDKAgentEndCallEvent(SDKAgentEvent, type=EventType.AGENT_END_CALL.value):
    pass


class TransferOptionType(str, Enum):
    COLD_TRANSFER = "cold_transfer"
    WARM_TRANSFER = "warm_transfer"


class WarmTransferHandoffOptionType(str, Enum):
    PROMPT = "prompt"
    STATIC = "static"


class WarmTransferPrivateHandoffOption(BaseModel):
    """A model for the warm transfer private handoff option."""

    type: WarmTransferHandoffOptionType
    prompt: str


class WarmTransferPublicHandoffOption(BaseModel):
    """A model for the warm transfer public handoff option."""

    type: WarmTransferHandoffOptionType
    prompt: str


class TransferOption(BaseModel):
    """A model for the transfer option."""

    model_config = ConfigDict(populate_by_name=True)

    type: TransferOptionType = Field(default=TransferOptionType.COLD_TRANSFER)
    private_handoff_option: Optional[WarmTransferPrivateHandoffOption] = Field(
        default=None, alias="privateHandoffOption"
    )
    public_handoff_option: Optional[WarmTransferPublicHandoffOption] = Field(
        default=None, alias="publicHandoffOption"
    )


class SDKAgentTransferConversationEvent(
    SDKAgentEvent, type=EventType.AGENT_TRANSFER_CONVERSATION.value
):
    transfer_call_number: str
    transfer_options: TransferOption
    on_hold_music: Optional[
        Literal["ringtone", "relaxing_sound", "uplifting_beats", "none"]
    ]


class SDKSystemInitEvent(SDKSystemEvent, type=EventType.SYSTEM_INIT.value):
    version: str
    session_context: SessionContext
    output_agent_settings: Optional[OutputAgentSettings] = None


class SDKSystemUpdateOutputAgentSettingsEvent(
    SDKSystemEvent, type=EventType.SYSTEM_UPDATE_OUTPUT_AGENT_SETTINGS.value
):
    settings: Dict[str, Any]


class SDKSystemUserJoinedEvent(SDKSystemEvent, type=EventType.SYSTEM_USER_JOINED.value):
    pass


class SDKSystemUserStartedSpeakingEvent(
    SDKSystemEvent, type=EventType.SYSTEM_USER_STARTED_SPEAKING.value
):
    pass


class SDKSystemUserStoppedSpeakingEvent(
    SDKSystemEvent, type=EventType.SYSTEM_USER_STOPPED_SPEAKING.value
):
    pass


class SDKSystemLLMRequestEvent(SDKSystemEvent, type=EventType.SYSTEM_LLM_REQUEST.value):
    """Request to LLM for completion."""

    extra_params: Dict[str, Any] = Field(default_factory=dict)


class SDKSystemControlInterruptEvent(
    SDKSystemEvent, type=EventType.SYSTEM_CONTROL_INTERRUPT.value
):
    pass


class SDKAgentReadyEvent(SDKAgentEvent, type=EventType.AGENT_READY.value):
    pass


class SDKAgentErrorEvent(SDKAgentEvent, type=EventType.AGENT_ERROR.value):
    message: str


class SDKAgentLLMResponseStartEvent(
    SDKAgentEvent, type=EventType.AGENT_LLM_RESPONSE_START.value
):
    """Streaming response started."""

    request_id: Optional[str] = None


class SDKAgentLLMResponseChunkEvent(
    SDKAgentEvent, type=EventType.AGENT_LLM_RESPONSE_CHUNK.value
):
    text: str


class SDKAgentLLMResponseEndEvent(
    SDKAgentEvent, type=EventType.AGENT_LLM_RESPONSE_END.value
):
    pass


class SDKAgentControlInterruptEvent(
    SDKAgentEvent, type=EventType.AGENT_CONTROL_INTERRUPT.value
):
    pass


class SDKAgentControlMuteUserEvent(
    SDKAgentEvent, type=EventType.AGENT_CONTROL_MUTE_USER.value
):
    pass


class SDKAgentControlUnmuteUserEvent(
    SDKAgentEvent, type=EventType.AGENT_CONTROL_UNMUTE_USER.value
):
    pass


class SDKAgentSpeakEvent(SDKAgentEvent, type=EventType.AGENT_SPEAK.value):
    text: str
