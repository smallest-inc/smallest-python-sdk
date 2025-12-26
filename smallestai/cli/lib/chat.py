import asyncio
import json
from datetime import datetime
from enum import Enum
from typing import Any, ClassVar, Dict, List, Literal, Optional, Tuple

from pydantic import BaseModel, ConfigDict, Field
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from websockets.asyncio.client import connect as websocket_connect

console = Console()


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


class SDKSystemUserJoinedEvent(SDKSystemEvent, type=EventType.SYSTEM_USER_JOINED.value):
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


class SDKCodec:
    """
    Codec for encoding/decoding SDK Events.

    Handles bi-directional conversion:
    - Event → JSON bytes (for sending to SDK)
    - JSON bytes → Event (for receiving from SDK)
    """

    def encode(self, data: SDKEvent) -> bytes:
        """
        Encode SDK Event to JSON bytes for sending over WebSocket.

        Args:
            data: SDK Event to encode

        Returns:
            JSON bytes
        """
        return json.dumps(
            {
                "type": data.type,
                **data.model_dump(mode="json"),
            }
        ).encode()

    def decode(self, data: bytes) -> SDKEvent:
        """
        Decode JSON bytes to SDK Event.

        Args:
            data: JSON bytes from WebSocket

        Returns:
            SDK Event instance
        """
        if isinstance(data, str):
            data = data.encode()
        return SDKEvent.parse_obj(json.loads(data))


class ChatClient:
    """WebSocket client for chatting with Atoms SDK agents."""

    def __init__(self, ws_url: str):
        self.ws_url = ws_url
        self._websocket = None
        self._connected = False
        self.codec = SDKCodec()

    async def _connect(self) -> bool:
        """
        Connect to WebSocket server.

        Pattern: Modern websockets.asyncio.client.connect
        """
        try:
            self._websocket = await websocket_connect(
                self.ws_url,
            )

            await self._websocket.send(
                self.codec.encode(
                    SDKSystemInitEvent(
                        session_context=SessionContext(
                            initial_variables={},
                            conversation_type=ConversationType.CHAT,
                        ),
                        version="1.0.0",
                    )
                )
            )

            received_event = await asyncio.wait_for(
                self._websocket.recv(), timeout=10.0
            )
            if isinstance(received_event, str):
                received_event = received_event.encode()
            received_event = self.codec.decode(received_event)

            if not isinstance(received_event, SDKAgentReadyEvent):
                if isinstance(received_event, SDKAgentErrorEvent):
                    console.print(f"[red]Error: {received_event.message}[/red]")
                    return False
                else:
                    console.print(
                        f"[yellow]Unexpected event: {received_event.type}[/yellow]"
                    )
                    return False

            self._connected = True
            console.print("[green]✓ Connected and ready![/green]\n")
            return True

        except asyncio.TimeoutError:
            console.print("[red]Init timed out[/red]")
            return False

        except Exception as e:
            console.print(f"[red]Failed to connect to WebSocket: {e}[/red]")
            return False

    async def _disconnect(self):
        """Disconnect from WebSocket server."""
        if self._websocket:
            await self._websocket.close()
            self._connected = False

    async def send_event(self, event: SDKEvent):
        if not self._connected or not self._websocket:
            console.print("[red]Not connected[/red]")
            return False

        try:
            await self._websocket.send(self.codec.encode(event))
            return True
        except Exception as e:
            console.print(f"[red]Failed to send event: {e}[/red]")
            return False

    async def send_message(self, user_message: str) -> Optional[str]:
        """Send a user message and receive the agent's response."""
        if not self._connected or not self._websocket:
            console.print("[red]Not connected[/red]")
            return None

        try:
            await self._websocket.send(
                self.codec.encode(
                    SDKAgentTranscriptUpdateEvent(role="user", content=user_message)
                )
            )

            await self._websocket.send(self.codec.encode(SDKSystemLLMRequestEvent()))

            full_response = ""
            response_text = Text()

            with Live(
                Panel(
                    response_text,
                    title="[bold blue]Assistant[/bold blue]",
                    border_style="blue",
                ),
                console=console,
                refresh_per_second=10,
                transient=True,
            ) as live:
                while True:
                    try:
                        message = await asyncio.wait_for(
                            self._websocket.recv(), timeout=60.0
                        )
                        if isinstance(message, str):
                            message = message.encode()
                        event = self.codec.decode(message)

                        if isinstance(event, SDKAgentLLMResponseStartEvent):
                            pass

                        elif isinstance(event, SDKAgentLLMResponseChunkEvent):
                            chunk_text = event.text
                            full_response += chunk_text
                            response_text.append(chunk_text)
                            live.update(
                                Panel(
                                    response_text,
                                    title="[bold blue]Assistant[/bold blue]",
                                    border_style="blue",
                                )
                            )

                        elif isinstance(event, SDKAgentLLMResponseEndEvent):
                            break

                        elif isinstance(event, SDKAgentErrorEvent):
                            console.print(f"[red]Error: {event.message}[/red]")
                            return None

                        elif isinstance(event, SDKAgentSpeakEvent):
                            speak_text = event.text
                            full_response += speak_text
                            response_text.append(speak_text)
                            live.update(
                                Panel(
                                    response_text,
                                    title="[bold blue]Assistant[/bold blue]",
                                    border_style="blue",
                                )
                            )

                    except asyncio.TimeoutError:
                        console.print("[yellow]Response timeout[/yellow]")
                        break

            if full_response:
                console.print(
                    Panel(
                        Markdown(full_response),
                        title="[bold blue]Assistant[/bold blue]",
                        border_style="blue",
                    )
                )

                await self._websocket.send(
                    self.codec.encode(
                        SDKAgentTranscriptUpdateEvent(
                            role="assistant", content=full_response
                        )
                    )
                )

            return full_response

        except Exception as e:
            console.print(f"[red]Error sending message: {e}[/red]")
            return None

    async def receive_initial_message(self) -> Optional[str]:
        """Receive any initial message from the agent (like a greeting)."""
        if not self._connected or not self._websocket:
            return None

        try:
            full_response = ""
            response_text = Text()

            try:
                message = await asyncio.wait_for(self._websocket.recv(), timeout=2.0)

                if isinstance(message, str):
                    message = message.encode()

                event = self.codec.decode(message)

                if isinstance(event, SDKAgentSpeakEvent):
                    full_response = event.text

                elif isinstance(event, SDKAgentLLMResponseStartEvent):
                    with Live(
                        Panel(
                            response_text,
                            title="[bold blue]Assistant[/bold blue]",
                            border_style="blue",
                        ),
                        console=console,
                        refresh_per_second=10,
                        transient=True,
                    ) as live:
                        while True:
                            try:
                                msg = await asyncio.wait_for(
                                    self._websocket.recv(), timeout=30.0
                                )
                                if isinstance(msg, str):
                                    msg = msg.encode()
                                evt = self.codec.decode(msg)

                                if isinstance(evt, SDKAgentLLMResponseChunkEvent):
                                    chunk = evt.text
                                    full_response += chunk
                                    response_text.append(chunk)
                                    live.update(
                                        Panel(
                                            response_text,
                                            title="[bold blue]Assistant[/bold blue]",
                                            border_style="blue",
                                        )
                                    )
                                elif isinstance(evt, SDKAgentLLMResponseEndEvent):
                                    break
                            except asyncio.TimeoutError:
                                break

            except asyncio.TimeoutError:
                pass

            if full_response:
                console.print(
                    Panel(
                        Markdown(full_response),
                        title="[bold blue]Assistant[/bold blue]",
                        border_style="blue",
                    )
                )

                await self._websocket.send(
                    self.codec.encode(
                        SDKAgentTranscriptUpdateEvent(
                            role="assistant", content=full_response
                        )
                    )
                )

            return full_response if full_response else None

        except Exception:
            return None


async def chat_loop(client: ChatClient):
    """Main chat loop."""
    await client.send_event(SDKSystemUserJoinedEvent())
    await client.receive_initial_message()

    console.print(
        "[dim]Type your message and press Enter. Type 'exit' or 'quit' to leave.[/dim]\n"
    )

    while True:
        try:
            user_input = Prompt.ask("[bold green]You[/bold green]")

            if user_input.lower() in ["exit", "quit", "q"]:
                console.print("[dim]Goodbye![/dim]")
                break

            if not user_input.strip():
                continue

            await client.send_message(user_input)
            console.print()

        except KeyboardInterrupt:
            console.print("\n[dim]Interrupted. Goodbye![/dim]")
            break
        except EOFError:
            console.print("\n[dim]Goodbye![/dim]")
