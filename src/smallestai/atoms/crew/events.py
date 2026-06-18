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
    AGENT_LOG = "agent.log"


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


class SDKAgentLogEvent(SDKAgentEvent, type=EventType.AGENT_LOG.value):
    """Customer-defined event for the call's Events timeline.

    Any crew node — background or output — emits these to publish arbitrary
    state to the orchestrator. The platform stores each one in ClickHouse
    via the relay (RabbitMQ → ClickHouse) pipeline and surfaces it in the
    Events tab of the call detail page, alongside transcripts, tool calls,
    and lifecycle markers.

    Common use cases:

    - Sentiment classifications, intent labels, lead scores
    - Escalation triggers, disposition tags, slot-fill completion
    - Custom UI markers — "verification passed", "form submitted",
      "voicemail detected", "consent recorded"
    - Observability cross-references — Langfuse / Datadog / NewRelic trace
      URLs that operators can jump to from the call view

    Example (background node)::

        from smallestai.atoms.crew.events import SDKAgentLogEvent
        from smallestai.atoms.crew.nodes import BackgroundCrewNode

        class SentimentAnalyzer(BackgroundCrewNode):
            async def process_event(self, event):
                ...  # classify
                await self.send_event(SDKAgentLogEvent(
                    name="sentiment",
                    payload={"sentiment": "frustrated", "frustration_count": 3},
                ))

    Example (output node — flagging an escalation)::

        await self.send_event(SDKAgentLogEvent(
            name="escalation.triggered",
            payload={"reason": "frustration_threshold_exceeded"},
        ))
    """

    name: str
    payload: Dict[str, Any] = Field(default_factory=dict)


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
    """An error from inside the deployed crew.

    Emitted automatically by the SDK whenever user code in
    `process_event()` / `generate_response()` raises, so the orchestrator
    can record it on the call. Customers can also emit these manually
    from inside their nodes for app-level errors (validation failures,
    upstream API errors, etc.).

    The `severity` field controls whether the call is failed:

    - `"warning"` (default for BackgroundCrewNode) — recorded on the
      call's `errors[]` but the call continues. Use for non-critical
      side-channels (sentiment, audit, observability) where the failure
      doesn't break the conversation.
    - `"fatal"` (default for OutputCrewNode) — recorded on the call's
      `errors[]`, the call is marked as failed, and `failureReason` is
      populated. Use for the agent itself failing — no point continuing
      if the user-facing brain isn't responding.

    Auto-populated payload keys when the SDK emits on your behalf:

    - `node_name` — which CrewNode raised
    - `traceback` — full Python traceback string
    - `error_class` — exception class name (e.g. `"OpenAIError"`)

    When emitting manually, you can add any other keys (`customer_id`,
    `request_id`, etc.) — the relay stores `payload` as JSON.
    """

    message: str
    severity: Literal["warning", "fatal"] = "warning"
    payload: Dict[str, Any] = Field(default_factory=dict)


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
