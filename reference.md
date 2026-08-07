# Reference
## Atoms User
<details><summary><code>client.atoms.user.<a href="src/smallestai/atoms/user/client.py">get_user_details</a>() -> GetUserResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.user.get_user_details()
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Atoms Organization
<details><summary><code>client.atoms.organization.<a href="src/smallestai/atoms/organization/client.py">get_organization_details</a>() -> GetOrganizationResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.organization.get_organization_details()
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Atoms AgentTemplates
<details><summary><code>client.atoms.agent_templates.<a href="src/smallestai/atoms/agent_templates/client.py">list_agent_templates</a>(...) -> ListAgentTemplatesAgentTemplatesResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.agent_templates.list_agent_templates()
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**region:** `typing.Optional[ListAgentTemplatesAgentTemplatesRequestRegion]` — Filter templates by region. Omit to return all templates.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.agent_templates.<a href="src/smallestai/atoms/agent_templates/client.py">create_agent_from_template</a>(...) -> PostAgentFromTemplateResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

We have created templates for some common use cases. You can use these templates to create an agent. For getting list of templates, you can use the /agent/template endpoint. It will give you the list of templates with their description and id. You can pass the id of the template in the request body to create an agent from the template.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.agent_templates.create_agent_from_template(
    agent_name="agentName",
    template_id="templateId",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**agent_name:** `str` — Name of the agent
    
</dd>
</dl>

<dl>
<dd>

**template_id:** `str` — ID of the template to use. You can get the list of templates with their description and id from the /agent/template endpoint.
    
</dd>
</dl>

<dl>
<dd>

**agent_description:** `typing.Optional[str]` — Description of the agent
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Agents
<details><summary><code>client.atoms.agents.<a href="src/smallestai/atoms/agents/client.py">list_agents</a>(...) -> ListAgentsAgentsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Agents are the main entities in the system. Agents are used to create conversations. You can create workflow for an agent and configure it for different use cases. You can also create custom workflows for an agent. This API will give you the list of agents created by organization you are a part of.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.agents.list_agents()
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**page:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**search:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**type:** `typing.Optional[ListAgentsAgentsRequestType]` — Filter agents by workflow type
    
</dd>
</dl>

<dl>
<dd>

**sort_field:** `typing.Optional[ListAgentsAgentsRequestSortField]` — Field to sort results by
    
</dd>
</dl>

<dl>
<dd>

**sort_order:** `typing.Optional[ListAgentsAgentsRequestSortOrder]` — Sort direction
    
</dd>
</dl>

<dl>
<dd>

**archived:** `typing.Optional[bool]` — When true, returns only archived agents. Omit or set to false to return active agents.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.agents.<a href="src/smallestai/atoms/agents/client.py">create_agent</a>(...) -> CreateAgentAgentsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Create a new agent by passing the agent name in the request body.

New agents have versioning enabled by default. To set the prompt,
`firstMessage`, tools, or any runtime config, fork a draft from the
auto-created initial version, edit it, publish, and activate — see
the [Versioning Lifecycle](/atoms/developer-guide/build/agents/versioning-lifecycle)
guide for the full flow.

The legacy `PATCH /workflow/{workflowId}` endpoint writes directly to
the underlying workflow document and bypasses the version lifecycle;
edits made that way are not captured as a version and may not
propagate to live calls. Use the drafts flow above.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.agents.create_agent(
    name="name",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**name:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**description:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**background_sound:** `typing.Optional[CreateAgentRequestBackgroundSound]` — Ambient background sound during calls. Options: '' (none), 'office', 'cafe', 'call_center', 'static'. Note: this value is currently overridden by the server default on creation; update via PATCH after creation.
    
</dd>
</dl>

<dl>
<dd>

**language:** `typing.Optional[CreateAgentRequestLanguage]` 

Language configuration for the agent.
Cross-field rule: `default` must be one of the values in `supported`.
Tamil (`ta`) cannot be combined with other languages in `supported`.
    
</dd>
</dl>

<dl>
<dd>

**synthesizer:** `typing.Optional[CreateAgentRequestSynthesizer]` 

Synthesizer (TTS) configuration for the agent. Model
`waves_lightning_v3_1` validates `voiceId` against the Waves
API. `gpt-realtime` and `gpt-realtime-mini` accept any voiceId.
Cloned voices are regular voiceIds. Use them with a compatible
Waves model.
    
</dd>
</dl>

<dl>
<dd>

**global_knowledge_base_id:** `typing.Optional[str]` — The global knowledge base ID of the agent. You can create a global knowledge base by using the /knowledgebase endpoint and assign it to the agent. The agent will use this knowledge base for its responses.
    
</dd>
</dl>

<dl>
<dd>

**slm_model:** `typing.Optional[CreateAgentRequestSlmModel]` 

The LLM model to use for the agent.
Note: `gpt-5.2`, `electron-kogta`, and `electron-kogta-v2` require org-level access and return 403 if not enabled.
`workflowType` must be `single_prompt` to use `gpt-realtime` or `gpt-realtime-mini`.
    
</dd>
</dl>

<dl>
<dd>

**default_variables:** `typing.Optional[typing.Dict[str, typing.Any]]` — The default variables to use for the agent. These variables will be used if no variables are provided when initiating a conversation with the agent.
    
</dd>
</dl>

<dl>
<dd>

**pre_call_api:** `typing.Optional[CreateAgentRequestPreCallApi]` — Configuration for an API call to be made before the call starts. The response variables can be injected into the agent's prompt.
    
</dd>
</dl>

<dl>
<dd>

**global_prompt:** `typing.Optional[str]` 

Set global instructions for your agent's personality, role, and behavior throughout conversations.
Note: Only used for workflow_graph agents. Maximum 4000 characters.
    
</dd>
</dl>

<dl>
<dd>

**telephony_product_id:** `typing.Optional[typing.List[str]]` — IDs of telephony products (phone numbers) to associate with the agent for inbound/outbound calls.
    
</dd>
</dl>

<dl>
<dd>

**workflow_type:** `typing.Optional[WorkflowType]` — The type of workflow to create for the agent. Defaults to `single_prompt` if not specified. Using `workflow_graph` requires conversational agent access (403 if not enabled).
    
</dd>
</dl>

<dl>
<dd>

**first_message:** `typing.Optional[str]` — The first message the agent sends when a conversation starts.
    
</dd>
</dl>

<dl>
<dd>

**mute_user_until_first_bot_response:** `typing.Optional[bool]` — When true, the user's audio is muted until the agent has finished its first response.
    
</dd>
</dl>

<dl>
<dd>

**allow_interruptions:** `typing.Optional[bool]` — Whether the user can interrupt the agent while it is speaking.
    
</dd>
</dl>

<dl>
<dd>

**wait_for_user_to_speak_first:** `typing.Optional[bool]` — When true, the agent waits for the user to speak before sending the first message.
    
</dd>
</dl>

<dl>
<dd>

**interruption_backoff_timer:** `typing.Optional[float]` — Seconds the agent waits after being interrupted before resuming speech.
    
</dd>
</dl>

<dl>
<dd>

**smart_turn_config:** `typing.Optional[CreateAgentRequestSmartTurnConfig]` — Smart turn-detection configuration. When enabled, the agent uses an additional model to decide whether the user has finished a turn.
    
</dd>
</dl>

<dl>
<dd>

**voice_detection_config:** `typing.Optional[CreateAgentRequestVoiceDetectionConfig]` — Voice activity detection (VAD) configuration. Controls how the agent decides when speech is present.
    
</dd>
</dl>

<dl>
<dd>

**voice_mail_detection_config:** `typing.Optional[CreateAgentRequestVoiceMailDetectionConfig]` — Voicemail-detection configuration. When the call hits a voicemail tone, the agent plays `endText` and ends the call.
    
</dd>
</dl>

<dl>
<dd>

**denoising_config:** `typing.Optional[CreateAgentRequestDenoisingConfig]` — Background-noise denoising configuration for the agent's input audio.
    
</dd>
</dl>

<dl>
<dd>

**redaction_config:** `typing.Optional[CreateAgentRequestRedactionConfig]` — PII redaction configuration. When enabled, personally identifiable information is redacted from transcripts before storage.
    
</dd>
</dl>

<dl>
<dd>

**pronunciation_dicts:** `typing.Optional[typing.List[CreateAgentRequestPronunciationDictsItem]]` — Pronunciation overrides — words the TTS engine should pronounce differently from its default.
    
</dd>
</dl>

<dl>
<dd>

**llm_idle_timeout_config:** `typing.Optional[CreateAgentRequestLlmIdleTimeoutConfig]` — Timeout configuration for the LLM stage of a conversation. Triggers a retry or call termination when the LLM does not respond within the configured window.
    
</dd>
</dl>

<dl>
<dd>

**session_timeout_config:** `typing.Optional[CreateAgentRequestSessionTimeoutConfig]` — Maximum duration of a conversation session. The call ends after this elapsed time even if active.
    
</dd>
</dl>

<dl>
<dd>

**timezone:** `typing.Optional[CreateAgentRequestTimezone]` — Timezone applied to scheduled actions and timestamps the agent reports to the user.
    
</dd>
</dl>

<dl>
<dd>

**call_disposition_config:** `typing.Optional[str]` — Configuration string for call disposition tracking.
    
</dd>
</dl>

<dl>
<dd>

**allow_inbound_call:** `typing.Optional[bool]` — Whether the agent accepts inbound calls.
    
</dd>
</dl>

<dl>
<dd>

**enable_style_guide:** `typing.Optional[bool]` — Whether style guide enforcement is applied to agent responses.
    
</dd>
</dl>

<dl>
<dd>

**speech_formatting:** `typing.Optional[bool]` — Whether speech formatting is applied to the agent's responses.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.agents.<a href="src/smallestai/atoms/agents/client.py">duplicate_agent</a>(...) -> DuplicateAgentAgentsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Duplicates a SINGLE_PROMPT agent's live active version into a target organization
(can also be the same organization). Copies all versioned configuration but strips
organization-specific resources: knowledge base tools are removed, default variable
values are blanked, and a new avatar is generated. The duplicate starts with a
published V1 as its active version.

**400 is returned when:**
- The source agent is archived (`"Cannot duplicate an archived agent"`)
- The agent has no `activeVersionId` (`"This agent has no active version and cannot be duplicated"`)
- The active version exists but is not published/active (`"This agent has no active published version and cannot be duplicated"`)
- The agent is not `SINGLE_PROMPT` workflow type
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.agents.duplicate_agent(
    id="id",
    target_organization_id="60d0fe4f5311236168a109ca",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The ID of the source agent to duplicate
    
</dd>
</dl>

<dl>
<dd>

**target_organization_id:** `str` 

MongoDB ObjectId of the target organization. Must be a 24-character hex string.
The authenticated user must be a member of this organization.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.agents.<a href="src/smallestai/atoms/agents/client.py">get_agent</a>(...) -> GetAgentAgentsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns the agent document merged with the resolved config of the active version
under `_resolvedConfig`. Non-versioned fields (name, telephonyProductId, allowInboundCall,
etc.) sit at the top level; versioned fields (prompt, tools, language, synthesizer,
post-call analytics, …) are resolved from the target version and exposed under `_resolvedConfig`.

**Previewing a draft or specific version**

Pass `?draftId=<id>` to resolve config from a specific draft instead of the active version.
Pass `?versionId=<id>` to resolve config from a specific published version.
When either param is used, the response includes `_configSource: "draft" | "version" | "active"`
indicating which config was resolved.

Notable resolved fields in `_resolvedConfig`:

- `prompt` — active version's single-prompt text
- `tools` — configured tools on the resolved version
- `postCallAnalyticsConfig` — disposition metrics + analytics model flags
- `modelName` — LLM model name on the resolved version
- `defaultLanguage`, `supportedLanguages` — active language config
- `firstMessage`, `globalPrompt` — active messaging config
- `workflowGraph` — full node graph for `workflow_graph` agents

To read prompt + tools alone, use `GET /agent/{id}/workflow` (deprecated for
new integrations but still live). To inspect a specific non-active version,
use `GET /agent/{id}/versions/{versionId}`.

**400 — also used for "not found":** if the agent ID does not exist in the
organization, the API returns 400 with `errors: ["No agent found"]` rather than 404.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.agents.get_agent(
    id="id",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**draft_id:** `typing.Optional[str]` — Resolve `_resolvedConfig` from this draft instead of the active version. Sets `_configSource` to `"draft"` in the response.
    
</dd>
</dl>

<dl>
<dd>

**version_id:** `typing.Optional[str]` — Resolve `_resolvedConfig` from this published version instead of the active version. Sets `_configSource` to `"version"` in the response.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.agents.<a href="src/smallestai/atoms/agents/client.py">update_agent</a>(...) -> UpdateAgentAgentsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Update agent fields. Behavior depends on whether the agent has versioning enabled:

**Versioned agents** (have an active published version): only metadata fields are accepted —
`name`, `description`, `avatarUrl`, `telephonyProductId`, `allowInboundCall`, `visibleToEveryone`.
Submitting any config-level field returns 400 with
`"Agent has versioning enabled. Config changes must be made through drafts."`.
Use `PATCH /agent/{id}/drafts/{draftId}/config` instead.

**Non-versioned agents** (no active version): all configuration fields are accepted,
the same full set as `POST /agent`.

**400 is also returned when a cross-field constraint is violated** (for example, `north_indic` language requires `transcriberType: pulse`).

**403** is returned when selecting a gated model (`gpt-5.2`, `electron-kogta`, `electron-kogta-v2`)
without org-level access.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.agents.update_agent(
    id="id",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` — Name of the agent.
    
</dd>
</dl>

<dl>
<dd>

**description:** `typing.Optional[str]` — Description of the agent.
    
</dd>
</dl>

<dl>
<dd>

**avatar_url:** `typing.Optional[str]` — URL of the agent's avatar image.
    
</dd>
</dl>

<dl>
<dd>

**telephony_product_id:** `typing.Optional[typing.List[str]]` — IDs of telephony products (phone numbers) to associate with the agent.
    
</dd>
</dl>

<dl>
<dd>

**allow_inbound_call:** `typing.Optional[bool]` — Whether the agent accepts inbound calls.
    
</dd>
</dl>

<dl>
<dd>

**visible_to_everyone:** `typing.Optional[bool]` — Whether the agent is visible to all members of the organization.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.agents.<a href="src/smallestai/atoms/agents/client.py">get_agent_widget_config</a>(...) -> GetAgentWidgetConfigResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns the current web widget configuration for the agent. Also includes `assistantId` (same as the agent ID) as a convenience field for the widget embed code.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.agents.get_agent_widget_config(
    id="id",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — Agent ObjectId
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.agents.<a href="src/smallestai/atoms/agents/client.py">update_agent_widget_config</a>(...) -> UpdateAgentWidgetConfigResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Updates the web widget configuration for the agent. Only provided fields are updated (partial update). When `avatarUrl` is changed, the old CDN avatar is automatically deleted from S3. The `avatarUrl` must be a URL from the platform's CDN domain — use `POST /agent/{id}/avatar/presigned-url` to upload first.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.agents.update_agent_widget_config(
    id="id",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — Agent ObjectId
    
</dd>
</dl>

<dl>
<dd>

**widget_config:** `typing.Optional[UpdateAgentWidgetConfigRequestWidgetConfig]` — All fields are optional — only provided fields are updated
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.agents.<a href="src/smallestai/atoms/agents/client.py">get_agent_avatar_presigned_url</a>(...) -> GetAgentAvatarPresignedUrlResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Generates a pre-signed S3 upload URL for the agent's widget avatar image. Upload the image directly to S3 using the returned `presignedUrl`, then save `cdnUrl` as the agent's avatar via `PATCH /agent/{id}/widget-config`.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.agents.get_agent_avatar_presigned_url(
    id="id",
    file_name="fileName",
    content_type="contentType",
    file_size=1.1,
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — Agent ObjectId
    
</dd>
</dl>

<dl>
<dd>

**file_name:** `str` — Original file name (used to construct the S3 key)
    
</dd>
</dl>

<dl>
<dd>

**content_type:** `str` — MIME type — must start with `image/`
    
</dd>
</dl>

<dl>
<dd>

**file_size:** `float` — File size in bytes — must be > 0 and ≤ 2 MB (2,097,152 bytes)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.agents.<a href="src/smallestai/atoms/agents/client.py">get_agent_call_logs</a>(...) -> GetAgentCallLogsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns paginated call logs for a specific agent.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.agents.get_agent_call_logs(
    id="id",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — Agent ObjectId
    
</dd>
</dl>

<dl>
<dd>

**page:** `typing.Optional[int]` — Page number (default 1)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Records per page (default 10)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.agents.<a href="src/smallestai/atoms/agents/client.py">archive_agent</a>(...) -> ArchiveAgentAgentsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Soft-archives the agent — it is excluded from listings and stops accepting calls,
but all data is preserved and the operation is fully reversible.

Pass `?on=false` to unarchive (restore) a previously archived agent.

**409 is returned when:**
- The agent is already in the requested state (`"Agent is already archived"` / `"Agent is already active"`)
- The agent is linked to an active campaign (`"Agent is associated with the [status] campaign "[name]". Complete or remove the campaign before archiving."`)
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.agents.archive_agent(
    id="id",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**on:** `typing.Optional[bool]` 

`true` (default) — archive the agent.
`false` — unarchive (restore) a previously archived agent.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Atoms Realtime
<details><summary><code>client.atoms.realtime.<a href="src/smallestai/atoms/realtime/client.py">register_call</a>(...) -> RegisterCallRealtimeResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Mint a **short-lived, single-use access token** for opening a realtime
[Agent WebSocket](/atoms/api-reference/realtime-agent/realtime-agent)
connection. This is the **recommended** way to start a session from a
browser or other client-side app: your API key stays server-side, and
the browser only ever sees the short-lived token. (Server-side or
trusted clients may instead connect to the WebSocket with a raw API key
directly.)

Flow:
1. Call this endpoint with your API key and the `agent_id` (plus optional
   `mode` and per-call `variables`). All session configuration is fixed
   here — it is baked into the returned token.
2. Open a WebSocket to `wss://api.smallest.ai/atoms/v1/agent/connect?token=<access_token>`.
   No `agent_id`, `mode`, or `variables` query params are needed on the
   WebSocket — they come from the token.

The token is valid for `expires_in` seconds (30) and can be used for a
single connection. Request a fresh token for each connection.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.realtime.register_call(
    agent_id="69da0b4c20c0e03cfa4ee258",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**agent_id:** `str` — The Atoms agent to connect to.
    
</dd>
</dl>

<dl>
<dd>

**mode:** `typing.Optional[RegisterCallRealtimeRequestMode]` 

Session mode. `webcall` = full voice pipeline (audio in +
audio out). `chat` = text-only pipeline. Defaults to `webcall`.
    
</dd>
</dl>

<dl>
<dd>

**variables:** `typing.Optional[typing.Dict[str, RegisterCallRealtimeRequestVariablesValue]]` 

Per-call prompt variables that override the agent's
`defaultVariables` for this session only. Values must be
`string`, `number`, or `boolean`. Reserved system-variable
keys (`call_id`, `conversation_type`, `agent_number`,
`user_number`, `current_date`, `current_time`, `current_day`,
`agent_gender`, `default_language`, `supported_languages`,
`timezone`) are populated by the server and stripped if
supplied.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Atoms Calls
<details><summary><code>client.atoms.calls.<a href="src/smallestai/atoms/calls/client.py">list</a>(...) -> ListCallsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieve paginated conversation logs with support for various filters. Returns call logs for agents belonging to the authenticated user's organization.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment
import datetime

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.calls.list(
    agent_ids="60d0fe4f5311236168a109ca,60d0fe4f5311236168a109cb",
    campaign_ids="60d0fe4f5311236168a109ca,60d0fe4f5311236168a109cb",
    search="+1234567890",
    status_filter="completed,failed",
    disconnect_reason_filter="user_hangup,agent_hangup",
    call_attempt_filter="initial",
    duration_filter="0-30,30-60",
    date_from=datetime.datetime.fromisoformat("2025-01-01T00:00:00+00:00"),
    date_to=datetime.datetime.fromisoformat("2025-01-31T23:59:59+00:00"),
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**page:** `typing.Optional[int]` — Page number for pagination
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Number of items per page. Server-side cap is 500 — values above 500 are silently clamped.
    
</dd>
</dl>

<dl>
<dd>

**agent_ids:** `typing.Optional[str]` — Comma-separated list of agent IDs to filter by
    
</dd>
</dl>

<dl>
<dd>

**campaign_ids:** `typing.Optional[str]` — Comma-separated list of campaign IDs to filter by
    
</dd>
</dl>

<dl>
<dd>

**call_types:** `typing.Optional[ListCallsRequestCallTypes]` — Comma-separated list of call types to filter by
    
</dd>
</dl>

<dl>
<dd>

**search:** `typing.Optional[str]` — Search query to filter by callId, fromNumber, or toNumber
    
</dd>
</dl>

<dl>
<dd>

**status_filter:** `typing.Optional[str]` 

Comma-separated list of call statuses to filter by.
Available statuses: pending, in_progress, in_queue, processing, active, completed, failed, no_answer, cancelled
    
</dd>
</dl>

<dl>
<dd>

**disconnect_reason_filter:** `typing.Optional[str]` 

Comma-separated list of disconnect reasons to filter by.
Available reasons: user_hangup, agent_hangup, connection_error, timeout, system_error, transfer_complete
    
</dd>
</dl>

<dl>
<dd>

**call_attempt_filter:** `typing.Optional[str]` 

Comma-separated list of call attempt types to filter by.
Available filters: initial (first attempt calls), retry (retry attempt calls), all (all calls)
    
</dd>
</dl>

<dl>
<dd>

**duration_filter:** `typing.Optional[str]` 

Comma-separated list of duration ranges to filter by.
Available ranges: 0-30 (0-30 seconds), 30-60 (30-60 seconds), 1-5 (1-5 minutes), 5+ (more than 5 minutes)
    
</dd>
</dl>

<dl>
<dd>

**sort_by:** `typing.Optional[ListCallsRequestSortBy]` — Field to sort results by
    
</dd>
</dl>

<dl>
<dd>

**sort_order:** `typing.Optional[ListCallsRequestSortOrder]` — Sort direction
    
</dd>
</dl>

<dl>
<dd>

**date_from:** `typing.Optional[datetime.datetime]` — ISO date — return calls created on or after this date
    
</dd>
</dl>

<dl>
<dd>

**date_to:** `typing.Optional[datetime.datetime]` — ISO date — return calls created on or before this date
    
</dd>
</dl>

<dl>
<dd>

**version_filter:** `typing.Optional[str]` — Comma-separated version IDs to filter calls by the agent version that handled them
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.calls.<a href="src/smallestai/atoms/calls/client.py">search</a>(...) -> SearchCallsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Fetch specific conversation logs by their callIds. This endpoint allows you to retrieve up to 100 specific calls at once.
Only returns calls that belong to agents in your organization (security check enforced).
Unlike the GET /conversation endpoint, this endpoint can also return retry calls (non-root calls).

**Differences from GET /conversation response:** each log item has the same base structure but
the following three fields are **not** included here:
- `dispositionMetrics` — not enriched
- `agentDispositionConfig` — not enriched
- `versionNumber` — not enriched
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.calls.search(
    call_ids=["CALL-1737000000000-abc123", "CALL-1737000000001-def456"],
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**call_ids:** `typing.List[str]` 

Array of callIds to fetch. Format: `CALL-{13-digit-timestamp}-{6-char-hex}`
(e.g. `CALL-1737000000000-abc123`). Minimum 1, maximum 100 per request.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.calls.<a href="src/smallestai/atoms/calls/client.py">get</a>(...) -> GetCallsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieve detailed information about a specific conversation including transcript, events, and latency metrics.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.calls.get(
    id="CALL-1737000000000-abc123",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The callId of the conversation (format `CALL-{13-digit-timestamp}-{6-char-hex}`). You can get the callId from the conversation logs endpoint.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.calls.<a href="src/smallestai/atoms/calls/client.py">start_outbound_call</a>(...) -> StartOutboundCallCallsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Initiates an outbound telephony call with a specified agent and phone number.

## Caller-ID resolution

When `fromProductId` is omitted **and** the agent has no telephony
product attached, the call dispatches from a Smallest-managed Plivo
trunk using a default caller-ID number (chosen by destination
country). The call still places and the response is still
`200 + conversationId`, but the recipient sees the default Smallest
number rather than your own. For production traffic, either:

- pass `fromProductId` explicitly (look up your owned numbers via
  `GET /product/phone-numbers`), or
- attach a phone-number product to the agent.

## Resolved-config check

The call uses the agent's currently-active version. If your most
recent prompt change went through `PATCH /workflow/{workflowId}` and
the agent has versioning enabled, that change may not have
propagated to the active version — and the call will play the
platform-default greeting instead of your prompt. Before placing a
production call, fetch `GET /agent/{agentId}` and confirm
`_resolvedConfig.firstMessage` (and related fields) match what you
intended. The
[Versioning Lifecycle](/atoms/developer-guide/build/agents/versioning-lifecycle)
guide covers the correct edit flow.

**400 is returned for:**
- Invalid `agentId` format (`"Invalid agent id"`)
- Invalid `phoneNumber` format (`"Invalid phone number"`)
- Invalid `fromProductId` format (`"Invalid product id"`)
- Agent not found or not in the caller's org (`"Agent not found"`)
- Agent is archived (`"Agent is archived and cannot initiate calls"`)
- `workflow_graph` agent has no workflow configured (`"Workflow not found"`)
- Workflow has validation errors (`"Invalid workflow, please fix the errors..."`)

**403** is returned for `workflow_graph` agents when the org lacks conversational agents access.

**Test calls:** set the `x-test-call: true` header to mark the resulting call log as a test call
(`isTest: true`). Test calls are subject to concurrent slot limits.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.calls.start_outbound_call(
    agent_id="60d0fe4f5311236168a109ca",
    phone_number="+1234567890",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**agent_id:** `str` — MongoDB ObjectId of the agent initiating the conversation
    
</dd>
</dl>

<dl>
<dd>

**phone_number:** `str` — The E.164 phone number to call
    
</dd>
</dl>

<dl>
<dd>

**test_call:** `typing.Optional[StartOutboundCallCallsRequestXTestCall]` — Set to "true" to mark this as a test call. The call log will have isTest=true and counts against concurrent test-call slot limits.
    
</dd>
</dl>

<dl>
<dd>

**variables:** `typing.Optional[typing.Dict[str, StartOutboundCallCallsRequestVariablesValue]]` 

Variables to inject into the agent's prompt at call time.
Values must be string, number, or boolean — nested objects are not supported.
    
</dd>
</dl>

<dl>
<dd>

**from_product_id:** `typing.Optional[str]` — ID of the telephony product (phone number) to call from. Get this from `GET /product/phone-numbers`.
    
</dd>
</dl>

<dl>
<dd>

**version_id:** `typing.Optional[str]` 

ID of a specific published agent version to use for this call.
Useful for test calls — attributes the call log to that version so you can track
which version was tested.
    
</dd>
</dl>

<dl>
<dd>

**operator_id:** `typing.Optional[str]` 

Integration operator identifier. Pass `"webengage"` to trigger the WebEngage
integration flow.
    
</dd>
</dl>

<dl>
<dd>

**operator_data:** `typing.Optional[typing.Dict[str, typing.Any]]` — Arbitrary data passed to the operator (e.g. `userId`, `journeyId` for WebEngage).
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Atoms Conversations
<details><summary><code>client.atoms.conversations.<a href="src/smallestai/atoms/conversations/client.py">get_a_time_limited_recording_download_url</a>(...) -> GetConversationCallIdRecordingDownloadUrlResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns a presigned S3 URL for the call's recording. Hand the URL straight to the customer or pull bytes server-side. The presigned URL is **time-limited** — typically usable for a few minutes — so don't cache it; request a fresh one each time you need the recording.

Returns `404` if the call has no recording (call hasn't started, was cancelled before audio captured, or was deleted by the platform's retention policy). Returns `400 Invalid call ID format` if you pass a Mongo `_id` instead of the `callId` string.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.conversations.get_a_time_limited_recording_download_url(
    call_id="CALL-1781127346211-e765f7",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**call_id:** `str` — The `callId` string for the conversation (e.g. `CALL-1778226705739-7e4c17`). This is the `callId` field returned by `GET /conversation`, **not** the Mongo `_id` — passing `_id` returns `400 Invalid call ID format`.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.conversations.<a href="src/smallestai/atoms/conversations/client.py">list_retry_attempts</a>(...) -> ListRetryAttemptsConversationsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns the **parent call** plus every retry attempt that branched from it, ordered by attempt index. Use this when a customer asks "did the platform retry this call?" — typically driven by an outbound agent's auto-retry configuration (`maxRetries`, `retryDelay`).

- If the `callId` you pass is the original (parent), the response contains that parent plus all child retries.
- If the `callId` you pass is itself a retry, the response still includes the parent and every sibling retry — the API resolves to the family root automatically.

Returns `404` if no call exists with that ID in your organization.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.conversations.list_retry_attempts(
    call_id="callId",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**call_id:** `str` — Any `callId` in the retry family (parent or any retry).
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.conversations.<a href="src/smallestai/atoms/conversations/client.py">cancel</a>(...) -> CancelConversationsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Cancels an outbound call that has been queued or is in progress. Use the body form to look the call up by `callId`; the path-param form (`POST /conversation/{callId}/cancel`) is the equivalent for REST conventions, but only handles `IN_QUEUE` calls.

Returns `404` if no call with that ID exists in your organization. Returns `400` if the call is already in a terminal state (completed / failed / cancelled).
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.conversations.cancel(
    call_id="CALL-1778226705739-7e4c17",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**call_id:** `str` — The `callId` returned by `POST /conversation/outbound` or visible in `GET /conversation`.
    
</dd>
</dl>

<dl>
<dd>

**reason:** `typing.Optional[str]` — Optional free-text reason for cancellation. Logged for support / audit.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.conversations.<a href="src/smallestai/atoms/conversations/client.py">cancel_queued</a>(...) -> CancelQueuedConversationsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

REST-conventional path-param variant of [`POST /conversation/cancel`](#operation/cancelCallByBody).

**Behavior differs from the body form.** This path-param endpoint only cancels calls that are still in the `IN_QUEUE` state — calls that have already started dialing or are in progress return `400 Bad Request` with `errors: ["Conversation with ID ... is not in queue and cannot be cancelled"]`. Use the body form (`POST /conversation/cancel`) if you need to cancel an in-progress call.

The path param is the `callId` string (e.g. `CALL-1778226705739-7e4c17`), **not** the Mongo `_id`. Passing `_id` returns `404 No conversation found`.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.conversations.cancel_queued(
    call_id="CALL-1781127346211-e765f7",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**call_id:** `str` — The `callId` string for the conversation to cancel.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Atoms LiveTranscripts
<details><summary><code>client.atoms.live_transcripts.<a href="src/smallestai/atoms/live_transcripts/client.py">subscribe_to_live_events</a>(...) -> typing.Iterator[bytes]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Real-time streaming of user speech (STT) and agent speech (TTS) events for an active call via Server-Sent Events.

The connection is real-time — events stream directly from the call runtime as they are produced. The SSE connection auto-closes when the call ends (`sse_close` event). Only active calls can be subscribed to; completed calls return a 400 error.

**Transcript event types:**

- `user_interim_transcription` — Partial, in-progress transcription as the user speaks. Use for live preview only; will be superseded by `user_transcription`.
- `user_transcription` — Final transcription for a completed user speech turn.
- `tts_completed` — Fired when the agent finishes speaking a TTS segment. Includes the spoken text and optionally TTS latency.

**Lifecycle events:**

- `sse_init` — Sent immediately when the SSE connection is established.
- `sse_close` — Sent when the call ends, right before the server closes the connection.

Other event types (e.g. `tool_call_start`, `pre_call_api`, `agent_log`, metrics) are also sent on this stream.

- `call_start`
- `call_end`
- `turn_latency`
- `metrics`
- `agent_node_state`
- `hopping`
- `knowledgebase`
- `variable_extraction`
- `pre_call_api`
- `post_call_api`
- `agent_error`
- `agent_log`
- `tool_call_start`
- `tool_call_end`
- `tool_call_error`
- `call_cancelled`
- `call_recording`
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.live_transcripts.subscribe_to_live_events(
    call_id="CALL-1758124225863-80752e",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**call_id:** `str` — The call ID to subscribe events for. Missing or invalid values return 400.
    
</dd>
</dl>

<dl>
<dd>

**organization_id:** `typing.Optional[str]` — Required when using session-cookie auth. API-token auth may infer the organization from the token.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Atoms Campaigns
<details><summary><code>client.atoms.campaigns.<a href="src/smallestai/atoms/campaigns/client.py">list</a>(...) -> ListCampaignsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Get all campaigns for the authenticated organization.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.campaigns.list()
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**page:** `typing.Optional[int]` — Page number for pagination
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Number of campaigns per page
    
</dd>
</dl>

<dl>
<dd>

**status:** `typing.Optional[ListCampaignsRequestStatus]` — Filter campaigns by status
    
</dd>
</dl>

<dl>
<dd>

**search:** `typing.Optional[str]` — Search campaigns by name
    
</dd>
</dl>

<dl>
<dd>

**sort_field:** `typing.Optional[ListCampaignsRequestSortField]` — Field to sort by
    
</dd>
</dl>

<dl>
<dd>

**sort_order:** `typing.Optional[ListCampaignsRequestSortOrder]` — Sort direction
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.campaigns.<a href="src/smallestai/atoms/campaigns/client.py">create</a>(...) -> CreateCampaignsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Create a campaign
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.campaigns.create(
    name="My Campaign",
    audience_id="60d0fe4f5311236168a109ca",
    agent_id="60d0fe4f5311236168a109ca",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**name:** `str` — The name of the campaign
    
</dd>
</dl>

<dl>
<dd>

**audience_id:** `str` — The ID of the audience
    
</dd>
</dl>

<dl>
<dd>

**agent_id:** `str` — The ID of the agent
    
</dd>
</dl>

<dl>
<dd>

**description:** `typing.Optional[str]` — The description of the campaign
    
</dd>
</dl>

<dl>
<dd>

**phone_number_ids:** `typing.Optional[typing.List[str]]` 

Optional list of caller-ID phone number IDs to rotate across
when placing outbound calls for this campaign. If omitted,
the agent's default phone number is used.
    
</dd>
</dl>

<dl>
<dd>

**scheduled_at:** `typing.Optional[datetime.datetime]` 

Optional ISO-8601 timestamp for when the campaign should
start dialing. Must be in the future. If provided, the
campaign is created in `scheduled` status; otherwise it
starts in `draft` status and must be started manually.
    
</dd>
</dl>

<dl>
<dd>

**max_retries:** `typing.Optional[int]` 

Maximum number of times a failed call is retried before the
participant is marked as failed. `0` disables retries.
    
</dd>
</dl>

<dl>
<dd>

**retry_delay:** `typing.Optional[int]` — Delay in minutes between retry attempts for a failed call.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.campaigns.<a href="src/smallestai/atoms/campaigns/client.py">get</a>(...) -> GetCampaignsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Get a campaign with detailed metrics
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.campaigns.get(
    id="id",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The ID of the campaign
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.campaigns.<a href="src/smallestai/atoms/campaigns/client.py">delete</a>(...) -> DeleteCampaignsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Delete a campaign
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.campaigns.delete(
    id="id",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The ID of the campaign
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.campaigns.<a href="src/smallestai/atoms/campaigns/client.py">start_or_resume</a>(...) -> StartOrResumeCampaignsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Queues the campaign for processing and returns immediately — the campaign is **not** yet
running when the 202 is returned. Poll `GET /campaign/{id}` and watch for `status: "running"`.

This endpoint also acts as a **resume** endpoint: if the campaign is currently paused,
calling this endpoint resumes it (`status` transitions from `paused` → `running`).
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.campaigns.start_or_resume(
    id="id",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The ID of the campaign
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.campaigns.<a href="src/smallestai/atoms/campaigns/client.py">pause</a>(...) -> PauseCampaignsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Queues a pause task and returns immediately — the campaign is **not** immediately paused.
Poll `GET /campaign/{id}` and watch for `status: "paused"`.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.campaigns.pause(
    id="id",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The ID of the campaign
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Atoms KnowledgeBase
<details><summary><code>client.atoms.knowledge_base.<a href="src/smallestai/atoms/knowledge_base/client.py">list</a>() -> ListKnowledgeBaseResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Get all knowledge bases
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.knowledge_base.list()
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.knowledge_base.<a href="src/smallestai/atoms/knowledge_base/client.py">create</a>(...) -> CreateKnowledgeBaseResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Create a knowledge base
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.knowledge_base.create(
    name="name",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**name:** `str` — Name of the knowledge base (1–40 characters, trimmed)
    
</dd>
</dl>

<dl>
<dd>

**description:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.knowledge_base.<a href="src/smallestai/atoms/knowledge_base/client.py">get</a>(...) -> GetKnowledgeBaseResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Get a knowledge base
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.knowledge_base.get(
    id="id",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The ID of the knowledge base
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.knowledge_base.<a href="src/smallestai/atoms/knowledge_base/client.py">update_a_knowledge_base_name_description</a>(...) -> PostKnowledgebaseIdResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Updates the metadata of a knowledge base. **Note**: the platform uses `POST` (not `PATCH`) on this path — preserved here as-is.

Only `name` and `description` are mutable through this endpoint. To add or remove content (files, URLs, text snippets), use the items endpoints.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.knowledge_base.update_a_knowledge_base_name_description(
    id="id",
    name="Q4 Pricing Updates",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — 24-char hex ObjectId of the knowledge base.
    
</dd>
</dl>

<dl>
<dd>

**name:** `str` — Display name. 1–40 characters; trimmed server-side.
    
</dd>
</dl>

<dl>
<dd>

**description:** `typing.Optional[str]` — Optional free-text description shown in the dashboard.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.knowledge_base.<a href="src/smallestai/atoms/knowledge_base/client.py">delete</a>(...) -> DeleteKnowledgeBaseResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Delete a knowledge base.

**400 is returned when the knowledge base is still linked to an agent:**
`"This knowledge base is connected to an agent. Please detach it from the agent before deleting."`
Detach the KB from all agents (via agent config) before attempting deletion.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.knowledge_base.delete(
    id="id",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The ID of the knowledge base
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.knowledge_base.<a href="src/smallestai/atoms/knowledge_base/client.py">get_all_knowledge_base_items</a>(...) -> GetKnowledgebaseIdItemsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Get all knowledge base items
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.knowledge_base.get_all_knowledge_base_items(
    id="id",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The ID of the knowledge base
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.knowledge_base.<a href="src/smallestai/atoms/knowledge_base/client.py">delete_a_knowledge_base_item</a>(...) -> DeleteKnowledgebaseKnowledgeBaseIdItemsKnowledgeBaseItemIdResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Delete a knowledge base item
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.knowledge_base.delete_a_knowledge_base_item(
    knowledge_base_id="knowledgeBaseId",
    knowledge_base_item_id="knowledgeBaseItemId",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**knowledge_base_id:** `str` — The ID of the knowledge base
    
</dd>
</dl>

<dl>
<dd>

**knowledge_base_item_id:** `str` — The ID of the knowledge base item
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.knowledge_base.<a href="src/smallestai/atoms/knowledge_base/client.py">upload_a_pdf_file_to_a_knowledge_base</a>(...) -> PostKnowledgebaseIdItemsUploadMediaResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Upload a PDF file to a knowledge base. Only PDF files are accepted (validated by MIME type and extension).

**400 is returned for billing/entitlement failures before the file is processed:**
- `"Insufficient credits for KB storage upload."` — account lacks upload credits
- `"KB storage access is not enabled for your account."` — plan doesn't include KB storage

No application-level file size limit is enforced — any proxy or infrastructure limits (e.g. nginx) apply instead.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.knowledge_base.upload_a_pdf_file_to_a_knowledge_base(
    id="id",
    media="example_media",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The ID of the knowledge base
    
</dd>
</dl>

<dl>
<dd>

**media:** `core.File` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.knowledge_base.<a href="src/smallestai/atoms/knowledge_base/client.py">get_a_presigned_s3url_for_direct_file_upload</a>(...) -> PostKnowledgebaseGetPresignedUrlResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Two-step file upload flow that bypasses Atoms' API for the file bytes themselves — useful when files exceed the multipart upload limit on `POST /knowledgebase/{id}/items/upload-media` or when you want to upload from the browser without round-tripping through your backend.

**Step 1**: Call this endpoint with file metadata. Atoms returns a presigned URL + a storage `key`.
**Step 2**: `PUT` the file bytes directly to the presigned URL (set `Content-Type` to the same value you sent here).
**Step 3**: Call [`POST /knowledgebase/compelete-file-upload`](#operation/completeKnowledgeBaseFileUpload) with the same `key` to commit the upload and start processing.

Same end result as `POST /knowledgebase/{id}/items/upload-media`, just without the multipart-through-our-API hop.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.knowledge_base.get_a_presigned_s3url_for_direct_file_upload(
    file_name="company-handbook.pdf",
    file_size=2457600,
    content_type="application/pdf",
    knowledge_base_id="6867ca76d0f8f2e0f4201281",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**file_name:** `str` — Original filename — used for display in the Atoms dashboard. Doesn't have to match the S3 key.
    
</dd>
</dl>

<dl>
<dd>

**file_size:** `int` — Size in bytes. Atoms uses this to enforce per-file limits before issuing the URL.
    
</dd>
</dl>

<dl>
<dd>

**content_type:** `str` — MIME type. You must send this EXACT value as `Content-Type` on the subsequent PUT to the presigned URL.
    
</dd>
</dl>

<dl>
<dd>

**knowledge_base_id:** `str` — 24-char hex ObjectId of the target knowledge base (from `GET /knowledgebase`).
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.knowledge_base.<a href="src/smallestai/atoms/knowledge_base/client.py">complete_a_presigned_url_upload_and_start_processing</a>(...) -> PostKnowledgebaseCompeleteFileUploadResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Step 3 of the presigned-URL upload flow. Commits a file that was uploaded directly to S3 via `POST /knowledgebase/get-presigned-url`, registers it as a knowledge-base item, and triggers async processing.

**Note**: The path includes `compelete` (sic) — that's the actual route name on the platform. Don't fix the spelling in your client; it's a stable URL.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.knowledge_base.complete_a_presigned_url_upload_and_start_processing(
    file_name="company-handbook.pdf",
    content_type="application/pdf",
    knowledge_base_id="6867ca76d0f8f2e0f4201281",
    key="key",
    file_size=1,
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**file_name:** `str` — Filename — pass the same value used in `get-presigned-url`.
    
</dd>
</dl>

<dl>
<dd>

**content_type:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**knowledge_base_id:** `str` — Target knowledge base ID.
    
</dd>
</dl>

<dl>
<dd>

**key:** `str` — S3 storage key returned by `get-presigned-url`.
    
</dd>
</dl>

<dl>
<dd>

**file_size:** `int` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.knowledge_base.<a href="src/smallestai/atoms/knowledge_base/client.py">extract_sitemap_urls</a>(...) -> ExtractSitemapUrlsKnowledgeBaseResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Fetches a website's `sitemap.xml`, parses it, and returns the list of URLs inside. Use this before calling `POST /knowledgebase/{id}/scrape-urls` to let the customer pick which URLs they actually want indexed.

Returns `422` if the URL doesn't return a fetchable sitemap or if the XML is malformed.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.knowledge_base.extract_sitemap_urls(
    site_url="https://example.com/sitemap.xml",
    knowledge_base_id="6867ca76d0f8f2e0f4201281",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**site_url:** `str` — URL of the sitemap.xml file (or a homepage that links to one).
    
</dd>
</dl>

<dl>
<dd>

**knowledge_base_id:** `str` — Target knowledge base ID — used for ownership validation only. The endpoint doesn't write any URLs at this stage.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.knowledge_base.<a href="src/smallestai/atoms/knowledge_base/client.py">scrape_urls</a>(...) -> ScrapeUrlsKnowledgeBaseResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Adds one or more URLs to a knowledge base by scraping each page's content, chunking it, and indexing for retrieval. Typical flow:

1. Discover candidate URLs (`POST /knowledgebase/get-sitemap-urls` or paste your own list).
2. Call this endpoint with the curated list — scraping runs async.
3. Poll `GET /knowledgebase/{id}/scraped-urls` for the per-URL status.

Returns `400` if your account's KB billing precheck fails (quota or plan limits). Returns `404` if the KB doesn't belong to your organization.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.knowledge_base.scrape_urls(
    id="id",
    urls=["https://example.com/pricing", "https://example.com/faq"],
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — 24-char hex ObjectId of the target knowledge base.
    
</dd>
</dl>

<dl>
<dd>

**urls:** `typing.List[str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.knowledge_base.<a href="src/smallestai/atoms/knowledge_base/client.py">list_scraped_ur_ls_in_a_knowledge_base_their_status</a>(...) -> GetKnowledgebaseIdScrapedUrlsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns every URL added to the knowledge base via `POST /knowledgebase/{id}/scrape-urls`, with its current scrape/index status. Poll this after kicking off a scrape job to track progress.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.knowledge_base.list_scraped_ur_ls_in_a_knowledge_base_their_status(
    id="id",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — 24-char hex ObjectId of the knowledge base.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.knowledge_base.<a href="src/smallestai/atoms/knowledge_base/client.py">delete_a_scraped_url_from_a_knowledge_base</a>(...) -> DeleteKnowledgebaseKnowledgeBaseIdScrapedUrlsKnowledgeBaseScrapedUrlsIdResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Removes a previously-scraped URL (and its indexed content) from the knowledge base. Permanent — there is no undo.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.knowledge_base.delete_a_scraped_url_from_a_knowledge_base(
    knowledge_base_id="knowledgeBaseId",
    knowledge_base_scraped_urls_id="knowledgeBaseScrapedUrlsId",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**knowledge_base_id:** `str` — 24-char hex ObjectId of the knowledge base.
    
</dd>
</dl>

<dl>
<dd>

**knowledge_base_scraped_urls_id:** `str` — 24-char hex ObjectId of the scraped-URL row to delete (from `GET /{id}/scraped-urls`).
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Atoms PhoneNumbers
<details><summary><code>client.atoms.phone_numbers.<a href="src/smallestai/atoms/phone_numbers/client.py">list</a>() -> ListPhoneNumbersResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieve all platform-purchased telephony numbers (Twilio/Plivo) for the organization.

**Note:** Imported SIP numbers added via `POST /product/import-phone-number` are **not** included
in this response — they are stored as a separate product type and returned by a different internal call.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.phone_numbers.list()
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.phone_numbers.<a href="src/smallestai/atoms/phone_numbers/client.py">list_all_phone_numbers_platform_sip</a>() -> GetProductAllNumbersResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns every phone number owned by the organization in one response:

- `telephonyProducts` — numbers rented via the Atoms platform (Plivo / Twilio).
- `customProducts` — numbers imported via [`POST /product/import-phone-number`](#operation/importSipPhoneNumber) with your own SIP trunks.

Use this when you need a single combined view (e.g. a "Pick a number" dropdown). To list only platform-rented numbers, use [`GET /product/phone-numbers`](#operation/getAcquiredPhoneNumbers).
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.phone_numbers.list_all_phone_numbers_platform_sip()
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.phone_numbers.<a href="src/smallestai/atoms/phone_numbers/client.py">search_rentable</a>(...) -> SearchRentablePhoneNumbersResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Searches the telephony provider's inventory for available numbers matching the requested country (and optional area code). Returns up to 5 candidates per call.

Use the returned `phoneNumber` value in [`POST /product/rent-number`](#operation/rentPhoneNumber) to actually rent it.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.phone_numbers.search_rentable(
    country_code="US",
    provider="plivo",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**country_code:** `str` — ISO 3166-1 alpha-2 country code (e.g. `US`, `IN`, `GB`).
    
</dd>
</dl>

<dl>
<dd>

**provider:** `SearchRentablePhoneNumbersRequestProvider` — Telephony provider to search.
    
</dd>
</dl>

<dl>
<dd>

**area_code:** `typing.Optional[str]` — Optional area-code / region filter — provider-dependent (US area codes for plivo/twilio, etc.).
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.phone_numbers.<a href="src/smallestai/atoms/phone_numbers/client.py">preview_prorated_rental_cost_for_renting_a_phone_number_today</a>() -> GetProductProrationAmountResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns the immediate prorated charge for renting one phone number from today through the end of the current billing cycle, plus the recurring monthly rate. Use this to show a "you'll be charged $X today" preview before calling [`POST /product/rent-number`](#operation/rentPhoneNumber).

Returns `400` if the organization doesn't have the phone-numbers feature configured (contact support) or if the org is currently locked (e.g. unpaid invoices — call [`GET /product/unpaid-invoices`](#operation/getUnpaidInvoices) first to check).
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.phone_numbers.preview_prorated_rental_cost_for_renting_a_phone_number_today()
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.phone_numbers.<a href="src/smallestai/atoms/phone_numbers/client.py">rent</a>(...) -> RentPhoneNumbersResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Rents an available number returned by [`GET /product/get-available-numbers`](#operation/searchAvailablePhoneNumbers). Charges the organization the prorated amount returned by [`GET /product/proration-amount`](#operation/getProrationAmount) immediately, then the monthly rate on each billing cycle.

Always call `GET /product/proration-amount` first to surface the immediate charge to your customer. The endpoint may return `200` with a body containing `requiresAction: true` when payment requires customer interaction (3-D Secure, etc.) — handle that branch in your client.

Released later via [`POST /product/release-number`](#operation/releasePhoneNumber).
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.phone_numbers.rent(
    phone_number="13183747513",
    provider="plivo",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**phone_number:** `str` — The number to rent — exactly as returned by `GET /product/get-available-numbers` (no leading `+`).
    
</dd>
</dl>

<dl>
<dd>

**provider:** `RentPhoneNumbersRequestProvider` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.phone_numbers.<a href="src/smallestai/atoms/phone_numbers/client.py">release</a>(...) -> ReleasePhoneNumbersResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Releases a phone number previously rented via `POST /product/rent-number`. The number goes back into provider inventory and recurring charges stop.

Returns `400` if the number is still assigned to an agent — detach it from the agent first (`PATCH /agent/{agentId}` with `productId: null`).
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.phone_numbers.release(
    product_id="6969109c84c74bed175f02a7",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**product_id:** `str` — 24-char hex MongoDB ObjectId of the phone-number product to release (the `_id` value returned by `GET /product/phone-numbers`).
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.phone_numbers.<a href="src/smallestai/atoms/phone_numbers/client.py">get_stripe_customer_portal_url</a>() -> GetProductManageSubscriptionResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns a time-limited Stripe Customer Portal URL the user can open to manage their subscription (update payment method, view invoices, etc.). Returns an empty object if the organization isn't on a Stripe-backed plan.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.phone_numbers.get_stripe_customer_portal_url()
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.phone_numbers.<a href="src/smallestai/atoms/phone_numbers/client.py">check_whether_the_organization_has_unpaid_invoices</a>() -> GetProductUnpaidInvoicesResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns whether the org has unpaid invoices that would block destructive actions (renting numbers, etc.). Call this before any billable mutation to surface the "Pay outstanding balance" flow.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.phone_numbers.check_whether_the_organization_has_unpaid_invoices()
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.phone_numbers.<a href="src/smallestai/atoms/phone_numbers/client.py">import_sip</a>(...) -> ImportSipPhoneNumbersResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Bring your own SIP trunk by importing an existing phone number with its SIP termination URL.
Atoms creates both inbound and outbound SIP trunks so your number works for making and receiving calls through the platform.

If `name` is omitted, a name is auto-generated from the phone number and user ID.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.phone_numbers.import_sip(
    phone_number="+14155551234",
    sip_termination_url="trunk.your-provider.com",
    name="Main Support Line",
    sip_username="",
    sip_password="",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**phone_number:** `str` — Your existing phone number. E.164 format is recommended but not enforced server-side — any non-empty string is accepted.
    
</dd>
</dl>

<dl>
<dd>

**sip_termination_url:** `str` — Your SIP provider's termination host — a hostname or IP address, optionally with a port (e.g. "sip.your-provider.com:5060"). Full SIP URIs ("sip:" / "sips:") are also accepted and automatically normalized to the bare host.
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` — A friendly display name for this number
    
</dd>
</dl>

<dl>
<dd>

**sip_username:** `typing.Optional[str]` — Username for SIP authentication (if your trunk requires it)
    
</dd>
</dl>

<dl>
<dd>

**sip_password:** `typing.Optional[str]` — Password for SIP authentication (if your trunk requires it)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Atoms Compliance
<details><summary><code>client.atoms.compliance.<a href="src/smallestai/atoms/compliance/client.py">get_compliance_status</a>(...) -> GetComplianceStatusResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns the current compliance status for a given country, number type, and user type.
This is the single endpoint the frontend uses to determine which step to render
(form, submitted, accepted, rejected, expired, or suspended).
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.compliance.get_compliance_status(
    country_iso="IN",
    number_type="local",
    user_type="individual",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**country_iso:** `str` — ISO 3166-1 alpha-2 country code. Must be exactly 2 characters (e.g. "IN", "US"). Sending 3+ characters returns 400.
    
</dd>
</dl>

<dl>
<dd>

**number_type:** `GetComplianceStatusRequestNumberType` — The type of phone number
    
</dd>
</dl>

<dl>
<dd>

**user_type:** `GetComplianceStatusRequestUserType` — The type of end user
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.compliance.<a href="src/smallestai/atoms/compliance/client.py">get_compliance_requirements</a>(...) -> GetComplianceRequirementsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Discover what documents are required for a given country, number type, and user type.
Results are cached for 1 hour. Returns an empty `documentTypes` array if no compliance
is needed for the given combination.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.compliance.get_compliance_requirements(
    country_iso="IN",
    number_type="local",
    user_type="individual",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**country_iso:** `str` — ISO 3166-1 alpha-2 country code. Must be exactly 2 characters (e.g. "IN", "US"). Sending 3+ characters returns 400.
    
</dd>
</dl>

<dl>
<dd>

**number_type:** `GetComplianceRequirementsRequestNumberType` — The type of phone number
    
</dd>
</dl>

<dl>
<dd>

**user_type:** `GetComplianceRequirementsRequestUserType` — The type of end user
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.compliance.<a href="src/smallestai/atoms/compliance/client.py">submit</a>(...) -> SubmitComplianceResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Submit a new compliance application with end-user details and supporting documents.
One application is allowed per organization per country per number type per user type.

The request uses `multipart/form-data` because documents are uploaded inline.
The `endUser` and `documents` fields are JSON strings embedded in the form data.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.compliance.submit(
    files=["example_files"],
    country_iso="countryIso",
    number_type="local",
    user_type="individual",
    end_user="endUser",
    documents="documents",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**country_iso:** `str` — ISO 3166-1 alpha-2 country code
    
</dd>
</dl>

<dl>
<dd>

**number_type:** `SubmitComplianceRequestNumberType` — The type of phone number
    
</dd>
</dl>

<dl>
<dd>

**user_type:** `SubmitComplianceRequestUserType` — The type of end user
    
</dd>
</dl>

<dl>
<dd>

**end_user:** `str` 

JSON-stringified end-user details. `name` is required; all other fields are optional
but may be required by Plivo depending on country/numberType. Accepted fields:

- `name` (required) — full name or business name
- `lastName` — last name
- `email` — email address
- `addressLine1` — street address line 1
- `addressLine2` — street address line 2
- `city` — city
- `state` — state or province
- `postalCode` — postal/ZIP code
- `country` — ISO country code; defaults to `countryIso` if omitted
- `registrationNumber` — business registration number (required for some business applications)
    
</dd>
</dl>

<dl>
<dd>

**documents:** `str` 

JSON string containing an array of document metadata. Each entry must have a
`documentTypeId` (from the requirements endpoint) and optional `dataFields`.
Example:
```json
[{"documentTypeId": "dt_123", "dataFields": {"business_name": "Acme Corp"}}]
```
    
</dd>
</dl>

<dl>
<dd>

**files:** `typing.List[core.File]` 

Document files in the same order as the `documents` metadata array.
Accepted formats: PDF, JPEG, PNG. Maximum 5 MB per file, up to 10 files.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.compliance.<a href="src/smallestai/atoms/compliance/client.py">resubmit</a>(...) -> ResubmitComplianceResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Resubmit a previously rejected compliance application with corrected documents.
Only applications in `rejected` status can be resubmitted. All documents must be
re-uploaded — partial updates are not supported.

File/document count must match exactly. Mismatch returns 400 with message `"Expected X files, got Y"`.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.compliance.resubmit(
    id="id",
    files=["example_files"],
    documents="documents",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The compliance application ID
    
</dd>
</dl>

<dl>
<dd>

**documents:** `str` 

JSON string containing an array of document metadata. Same format as
the create endpoint.
    
</dd>
</dl>

<dl>
<dd>

**files:** `typing.List[core.File]` 

Replacement document files. Must match the length of the `documents` array.
Accepted formats: PDF, JPEG, PNG. Maximum 5 MB per file.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.compliance.<a href="src/smallestai/atoms/compliance/client.py">refresh_compliance_application_status</a>(...) -> PostComplianceApplicationsIdRefreshResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Manually poll Plivo for the latest status of a compliance application.
Use this as a fallback when webhooks are delayed. The frontend enforces a
60-second cooldown between refreshes.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.compliance.refresh_compliance_application_status(
    id="id",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The compliance application ID
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Atoms Webhooks
<details><summary><code>client.atoms.webhooks.<a href="src/smallestai/atoms/webhooks/client.py">get_webhooks</a>(...) -> GetWebhookResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieve all webhooks for the organization or a specific webhook by ID
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.webhooks.get_webhooks()
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**webhook_id:** `typing.Optional[str]` — Optional MongoDB ObjectId (24-char hex) of a specific webhook to retrieve. If omitted, returns all webhooks for the organization.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.webhooks.<a href="src/smallestai/atoms/webhooks/client.py">create</a>(...) -> CreateWebhooksResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Create a new webhook with subscriptions for specific agents and events.

**400 is also returned when the endpoint URL is already registered:**
`"A webhook with this URL has already been registered"`
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment
from smallestai.atoms.webhooks import CreateWebhooksRequestEventsItem

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.webhooks.create(
    endpoint="https://example.com/webhook",
    description="Webhook for conversation events",
    events=[
        CreateWebhooksRequestEventsItem(
            agent_id="60d0fe4f5311236168a109ca",
            event_type="pre-conversation",
        )
    ],
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**endpoint:** `str` — The webhook endpoint URL
    
</dd>
</dl>

<dl>
<dd>

**description:** `str` — The description of the webhook
    
</dd>
</dl>

<dl>
<dd>

**events:** `typing.List[CreateWebhooksRequestEventsItem]` — Array of events to subscribe to
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.webhooks.<a href="src/smallestai/atoms/webhooks/client.py">delete</a>(...) -> DeleteWebhooksResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Delete a webhook by its ID.

**400 is returned when the webhook still has active agent subscriptions:**
`"Cannot delete webhook: It is currently assigned to one or more agents. Please remove all agent assignments first."`
Call `DELETE /agent/{agentId}/webhook-subscriptions` for each assigned agent before deleting.

**400 is also returned for an invalid webhook ID format:**
`"The provided Webhook ID is invalid."`
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.webhooks.delete(
    id="id",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The ID of the webhook to delete
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.webhooks.<a href="src/smallestai/atoms/webhooks/client.py">update</a>(...) -> UpdateWebhooksResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Update a webhook's endpoint URL, description, or custom headers. At
least one of the three fields must be present in the request body.

**Event subscriptions cannot be changed here.** To add or remove an
agent's subscription to this webhook, use `POST /agent/{agentId}/webhook-subscriptions`
and `DELETE /agent/{agentId}/webhook-subscriptions`.

**Custom `headers` behavior**
- Send a non-empty object to replace all custom headers on the webhook.
- Send an empty object (`{}`) to clear all custom headers.
- Omit the field to leave existing custom headers untouched.

Custom header limits: at most 10 headers per webhook, values up to
1024 characters, header names must match RFC 7230 token syntax. The
following names are reserved and rejected: `x-signature`, `host`,
`content-length`, `content-type`, `connection`, `transfer-encoding`.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.webhooks.update(
    id="id",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The ID of the webhook to update.
    
</dd>
</dl>

<dl>
<dd>

**endpoint:** `typing.Optional[str]` — New endpoint URL. Must be a valid URL.
    
</dd>
</dl>

<dl>
<dd>

**description:** `typing.Optional[str]` — New human-readable label.
    
</dd>
</dl>

<dl>
<dd>

**headers:** `typing.Optional[typing.Dict[str, str]]` 

Map of custom header names to values. Non-empty object replaces
all existing headers; empty object clears them.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.webhooks.<a href="src/smallestai/atoms/webhooks/client.py">get_webhook_subscriptions_for_an_agent</a>(...) -> GetAgentAgentIdWebhookSubscriptionsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieve webhook subscriptions for a given agent ID
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.webhooks.get_webhook_subscriptions_for_an_agent(
    agent_id="agentId",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**agent_id:** `str` — The ID of the agent
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.webhooks.<a href="src/smallestai/atoms/webhooks/client.py">replace_webhook_subscriptions_for_an_agent</a>(...) -> PostAgentAgentIdWebhookSubscriptionsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

**Replaces** all existing webhook subscriptions for the agent with the provided event types.
Any previously configured subscriptions for this agent are deleted before the new ones are created.
To add subscriptions without removing existing ones, retrieve current subscriptions first and include them in the request.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.webhooks.replace_webhook_subscriptions_for_an_agent(
    agent_id="agentId",
    event_types=["pre-conversation"],
    webhook_id="60d0fe4f5311236168a109ca",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**agent_id:** `str` — The ID of the agent to create subscriptions for
    
</dd>
</dl>

<dl>
<dd>

**event_types:** `typing.List[PostAgentAgentIdWebhookSubscriptionsRequestEventTypesItem]` — Array of event types to subscribe to
    
</dd>
</dl>

<dl>
<dd>

**webhook_id:** `str` — The ID of the webhook to subscribe to
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.webhooks.<a href="src/smallestai/atoms/webhooks/client.py">delete_webhook_subscriptions_for_an_agent</a>(...) -> DeleteAgentAgentIdWebhookSubscriptionsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Deletes **all** webhook subscriptions for the agent, regardless of which webhook they belong to.
If the agent has subscriptions across multiple webhooks, all of them are removed in a single call.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.webhooks.delete_webhook_subscriptions_for_an_agent(
    agent_id="agentId",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**agent_id:** `str` — The ID of the agent to filter subscriptions by
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Atoms Audience
<details><summary><code>client.atoms.audience.<a href="src/smallestai/atoms/audience/client.py">list</a>() -> ListAudienceResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieve all audiences created by the authenticated user. Users can only access audiences they have created.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.audience.list()
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.audience.<a href="src/smallestai/atoms/audience/client.py">create_audience_with_csv_upload</a>(...) -> PostAudienceResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Create a new audience by uploading a CSV file containing phone numbers.
Only CSV text files are accepted — binary files will produce malformed data.

**Additional 400 cases:**
- Duplicate phone numbers in the CSV: `"Some phone numbers in your CSV already exist in this audience. Please remove duplicate entries and try again."`
- Member limit exceeded: `"Audience cannot exceed X members"`
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.audience.create_audience_with_csv_upload(
    file="example_file",
    name="name",
    phone_number_column_name="phoneNumberColumnName",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**name:** `str` — The name of the audience
    
</dd>
</dl>

<dl>
<dd>

**phone_number_column_name:** `str` — The name of the column in the CSV that contains phone numbers
    
</dd>
</dl>

<dl>
<dd>

**file:** `core.File` — CSV file containing phone numbers and identifiers (max 5MB)
    
</dd>
</dl>

<dl>
<dd>

**description:** `typing.Optional[str]` — Optional description of the audience
    
</dd>
</dl>

<dl>
<dd>

**identifier_column_name:** `typing.Optional[str]` — The name of the column in the CSV that contains identifiers (e.g., names)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.audience.<a href="src/smallestai/atoms/audience/client.py">get</a>(...) -> GetAudienceResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieve a specific audience by its ID.
Note: if the audience belongs to a different organization, the API returns 404 (not 403) — ownership is deliberately obscured.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.audience.get(
    id="60d0fe4f5311236168a109ca",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The unique identifier of the audience
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.audience.<a href="src/smallestai/atoms/audience/client.py">delete_audience</a>(...) -> DeleteAudienceIdResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Delete a specific audience by its ID. Users can only delete audiences they created.

**400 is returned if the audience is used by an active campaign:**
`"can't delete audience, campaign with this audience <id> exists"`
Remove the campaign first, then retry deletion.

On success, `data` is always an empty array `[]`.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.audience.delete_audience(
    id="60d0fe4f5311236168a109ca",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The unique identifier of the audience to delete
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.audience.<a href="src/smallestai/atoms/audience/client.py">get_audience_members</a>(...) -> GetAudienceIdMembersResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieve members of a specific audience with pagination support. Users can only access members of audiences they created.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.audience.get_audience_members(
    id="60d0fe4f5311236168a109ca",
    page=1,
    offset=10,
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The unique identifier of the audience
    
</dd>
</dl>

<dl>
<dd>

**page:** `typing.Optional[int]` — Page number for pagination (default is 1)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` 

Number of items per page (default is 5).
Note: this parameter is named "offset", not "limit" — sending ?limit=N is silently ignored.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.audience.<a href="src/smallestai/atoms/audience/client.py">add_audience_members</a>(...) -> PostAudienceIdMembersResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Add new members to an existing audience.

Each member object must include a key matching the audience's `phoneNumberColumnName`.
If it's missing, the API returns 400: `"Each member must have a <phoneNumberColumnName> field"`.
Adding members that would exceed the audience limit also returns 400.

Note: if the audience belongs to a different organization, the API returns 404 (not 403).
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.audience.add_audience_members(
    id="60d0fe4f5311236168a109ca",
    members=[{"phoneNumber": "+1234567890", "name": "John Doe", "email": "john@example.com"}],
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The unique identifier of the audience
    
</dd>
</dl>

<dl>
<dd>

**members:** `typing.List[typing.Dict[str, typing.Any]]` — Array of member objects with dynamic structure based on audience configuration
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.audience.<a href="src/smallestai/atoms/audience/client.py">delete_audience_members</a>(...) -> DeleteAudienceIdMembersResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Remove specific members from an audience by their member IDs. Users can only delete members from audiences they created.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.audience.delete_audience_members(
    id="60d0fe4f5311236168a109ca",
    member_ids=["60d0fe4f5311236168a109cd"],
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The unique identifier of the audience
    
</dd>
</dl>

<dl>
<dd>

**member_ids:** `typing.List[str]` — Array of member IDs to delete
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.audience.<a href="src/smallestai/atoms/audience/client.py">search_audience_members</a>(...) -> GetAudienceIdMembersSearchResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Search for members within a specific audience using flexible search parameters. Users can only search members of audiences they created.

**Search Types:**
- **General Search** (`query`): Searches across all fields in the audience member data
- **Field-Specific Search**: Use any field name as a parameter (e.g., `firstName=john`, `phoneNumber=123456`, `email=test@example.com`)

**Examples:**
- `?query=john` - General search across all fields
- `?firstName=john` - Search specifically in firstName field
- `?phoneNumber=555-1234` - Search specifically in phoneNumber field
- `?firstName=john&lastName=doe` - Search for members matching both criteria

**Note:** When using phoneNumber field, do not use quotes around the phone number. You can use either a general search OR field-specific searches, but not both simultaneously.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.audience.search_audience_members(
    id="60d0fe4f5311236168a109ca",
    query="john",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The unique identifier of the audience
    
</dd>
</dl>

<dl>
<dd>

**query:** `typing.Optional[str]` — General search term that searches across all fields in audience member data
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Atoms AgentVersioningDrafts
<details><summary><code>client.atoms.agent_versioning_drafts.<a href="src/smallestai/atoms/agent_versioning_drafts/client.py">list_active_drafts</a>(...) -> GetAgentIdDraftsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

**Deprecated on the v2 branch model.** Migrate to `GET /agent/{id}/branches (`openDraftId` / `hasOpenDraft`)`. When `ENABLE_BRANCH_MODEL` is on, this endpoint returns `409 versioning_v2_migration_required` with the `Deprecation: true` header. See the [migration guide](/voice-agents/deprecations/agent-versioning-migration).

List all active (non-discarded) drafts for an agent.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.agent_versioning_drafts.list_active_drafts(
    id="id",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The agent ID.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.agent_versioning_drafts.<a href="src/smallestai/atoms/agent_versioning_drafts/client.py">create_draft</a>(...) -> CreateDraftAgentVersioningDraftsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

**Deprecated on the v2 branch model.** Migrate to `PUT /agent/{id}/branches/{branchId}/draft`. When `ENABLE_BRANCH_MODEL` is on, this endpoint returns `409 versioning_v2_migration_required` with the `Deprecation: true` header. See the [migration guide](/voice-agents/deprecations/agent-versioning-migration).

Create a new draft from an existing published version or another draft. At least one of sourceVersionId or sourceDraftId is required (both may be sent simultaneously).
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.agent_versioning_drafts.create_draft(
    id="id",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The agent ID.
    
</dd>
</dl>

<dl>
<dd>

**source_version_id:** `typing.Optional[str]` 

ID of a published version to branch from. Must be a valid MongoDB ObjectId (24-char hex).
Sending a non-ObjectId format returns 400.
    
</dd>
</dl>

<dl>
<dd>

**source_draft_id:** `typing.Optional[str]` — ID of an existing draft to branch from
    
</dd>
</dl>

<dl>
<dd>

**draft_name:** `typing.Optional[str]` — Optional name for the draft (1–100 characters)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.agent_versioning_drafts.<a href="src/smallestai/atoms/agent_versioning_drafts/client.py">get_draft_detail</a>(...) -> GetAgentIdDraftsDraftIdResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

**Deprecated.** By-id reads are kept working during the v1 coexistence window (~1 month). A v1 `draftId` remains resolvable. Migrate to `GET /agent/{id}/branches/{branchId}/draft`. Will be removed at the sunset date.

Returns the latest revision of a draft along with its edit history.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.agent_versioning_drafts.get_draft_detail(
    id="id",
    draft_id="draftId",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The agent ID.
    
</dd>
</dl>

<dl>
<dd>

**draft_id:** `str` — The draft ID
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Max number of edit history entries to return (1-100)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.agent_versioning_drafts.<a href="src/smallestai/atoms/agent_versioning_drafts/client.py">discard_draft</a>(...) -> DiscardDraftAgentVersioningDraftsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

**Deprecated on the v2 branch model.** Migrate to `DELETE /agent/{id}/branches/{branchId}/draft`. When `ENABLE_BRANCH_MODEL` is on, this endpoint returns `409 versioning_v2_migration_required` with the `Deprecation: true` header. See the [migration guide](/voice-agents/deprecations/agent-versioning-migration).

Discard (soft-delete) a draft. Only the draft creator or an admin can discard.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.agent_versioning_drafts.discard_draft(
    id="id",
    draft_id="draftId",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The agent ID.
    
</dd>
</dl>

<dl>
<dd>

**draft_id:** `str` — The draft ID
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.agent_versioning_drafts.<a href="src/smallestai/atoms/agent_versioning_drafts/client.py">rename_draft</a>(...) -> RenameDraftAgentVersioningDraftsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

**Deprecated on the v2 branch model.** Migrate to `PUT /agent/{id}/branches/{branchId}/draft`. When `ENABLE_BRANCH_MODEL` is on, this endpoint returns `409 versioning_v2_migration_required` with the `Deprecation: true` header. See the [migration guide](/voice-agents/deprecations/agent-versioning-migration).

|
Rename a draft. For config changes, use PATCH /agent/{id}/drafts/{draftId}/config instead.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.agent_versioning_drafts.rename_draft(
    id="id",
    draft_id="draftId",
    draft_name="draftName",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The agent ID.
    
</dd>
</dl>

<dl>
<dd>

**draft_id:** `str` — The draft ID
    
</dd>
</dl>

<dl>
<dd>

**draft_name:** `str` — New name for the draft (1–100 characters)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.agent_versioning_drafts.<a href="src/smallestai/atoms/agent_versioning_drafts/client.py">get_draft_diff</a>(...) -> GetAgentIdDraftsDraftIdDiffResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

**Deprecated.** Kept working during the v1 coexistence window (~1 month). Migrate to `GET /agent/{id}/diff?a=<branchId>:draft&b=<revisionId>`. Will be removed at the sunset date.

Compare a draft against its source version or another specified version.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.agent_versioning_drafts.get_draft_diff(
    id="id",
    draft_id="draftId",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The agent ID.
    
</dd>
</dl>

<dl>
<dd>

**draft_id:** `str` — The draft ID
    
</dd>
</dl>

<dl>
<dd>

**compare_to:** `typing.Optional[str]` — Version ID to compare against. If omitted, compares against the source version.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.agent_versioning_drafts.<a href="src/smallestai/atoms/agent_versioning_drafts/client.py">publish_draft</a>(...) -> PublishDraftAgentVersioningDraftsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

**Deprecated on the v2 branch model.** Migrate to `POST /agent/{id}/branches/{branchId}/draft/publish`. When `ENABLE_BRANCH_MODEL` is on, this endpoint returns `409 versioning_v2_migration_required` with the `Deprecation: true` header. See the [migration guide](/voice-agents/deprecations/agent-versioning-migration).

Publish a draft as a new versioned release. Optionally activate it immediately.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.agent_versioning_drafts.publish_draft(
    id="id",
    draft_id="draftId",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The agent ID.
    
</dd>
</dl>

<dl>
<dd>

**draft_id:** `str` — The draft ID
    
</dd>
</dl>

<dl>
<dd>

**label:** `typing.Optional[str]` — Label for the published version
    
</dd>
</dl>

<dl>
<dd>

**description:** `typing.Optional[str]` — Description of the published version
    
</dd>
</dl>

<dl>
<dd>

**activate:** `typing.Optional[bool]` — Whether to immediately activate the version after publishing
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.agent_versioning_drafts.<a href="src/smallestai/atoms/agent_versioning_drafts/client.py">test_call_with_draft_config</a>(...) -> PostAgentIdDraftsDraftIdTestCallResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

**Deprecated.** Test-calls are exempt from the v1 write-block and remain functional. Migrate to `POST /agent/{id}/branches/{branchId}/test-call` with `includeDraft: true`. Will be removed at the sunset date.

Initiate a test call using the draft's resolved configuration.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.agent_versioning_drafts.test_call_with_draft_config(
    id="id",
    draft_id="draftId",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The agent ID.
    
</dd>
</dl>

<dl>
<dd>

**draft_id:** `str` — The draft ID
    
</dd>
</dl>

<dl>
<dd>

**request:** `TestCallRequest` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.agent_versioning_drafts.<a href="src/smallestai/atoms/agent_versioning_drafts/client.py">update_draft_config</a>(...) -> UpdateDraftConfigAgentVersioningDraftsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

**Deprecated on the v2 branch model.** Migrate to `PUT /agent/{id}/branches/{branchId}/draft`. When `ENABLE_BRANCH_MODEL` is on, this endpoint returns `409 versioning_v2_migration_required` with the `Deprecation: true` header. See the [migration guide](/voice-agents/deprecations/agent-versioning-migration).

|
Update the configuration of a draft. This single endpoint is how every
agent-level config field is changed: prompt, tools, voice, language,
**post-call analytics (disposition metrics)**, and more. There is no
standalone post-call-analytics endpoint — it lives here as the
`postCallAnalyticsConfig` body field.

## Post-Call Analytics

Pass a `postCallAnalyticsConfig` object to configure disposition
metrics (STRING, BOOLEAN, INTEGER, ENUM, DATETIME) that are
automatically extracted from each completed call, along with the
`useInternalAnalyticsModel` and `useReasoningModel` flags. See the
[Post-Call Metrics guide](/atoms/atoms-platform/features/post-call-metrics) for a
full Python walkthrough and disposition metric schema reference.

## Full payload

Accepts the full agent-shaped config payload (language, synthesizer,
slmModel, defaultVariables, preCallAPI, etc.) plus two draft-specific
fields:

- `singlePromptConfig` — prompt and tools (end_call, transfer_call,
  api_call, extract_dynamic_variables, knowledge_base_search).
- `postCallAnalyticsConfig` — disposition metrics + analytics/
  reasoning model flags.

Each PATCH increments the draft's revision counter. Config is not
live until the draft is published and activated (see
`/drafts/{draftId}/publish` and `/versions/{versionId}/activate`).
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.agent_versioning_drafts.update_draft_config(
    id="id",
    draft_id="draftId",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The agent ID.
    
</dd>
</dl>

<dl>
<dd>

**draft_id:** `str` — The draft ID
    
</dd>
</dl>

<dl>
<dd>

**single_prompt_config:** `typing.Optional[SinglePromptConfig]` 
    
</dd>
</dl>

<dl>
<dd>

**post_call_analytics_config:** `typing.Optional[PostCallAnalyticsConfig]` 
    
</dd>
</dl>

<dl>
<dd>

**language:** `typing.Optional[typing.Dict[str, typing.Any]]` — Language configuration. See CreateAgentRequest for full shape.
    
</dd>
</dl>

<dl>
<dd>

**synthesizer:** `typing.Optional[typing.Dict[str, typing.Any]]` — Synthesizer (TTS) configuration. See CreateAgentRequest for full shape.
    
</dd>
</dl>

<dl>
<dd>

**slm_model:** `typing.Optional[DraftConfigRequestSlmModel]` — LLM model for this draft
    
</dd>
</dl>

<dl>
<dd>

**transcriber_type:** `typing.Optional[str]` — STT engine to use for this draft
    
</dd>
</dl>

<dl>
<dd>

**custom_llm_web_socket_url:** `typing.Optional[str]` — Custom LLM WebSocket URL (overrides slmModel)
    
</dd>
</dl>

<dl>
<dd>

**widget_config:** `typing.Optional[typing.Dict[str, typing.Any]]` — Widget configuration for chat-mode agents
    
</dd>
</dl>

<dl>
<dd>

**default_variables:** `typing.Optional[typing.Dict[str, typing.Any]]` — Default prompt variables
    
</dd>
</dl>

<dl>
<dd>

**pre_call_api:** `typing.Optional[typing.Dict[str, typing.Any]]` — Pre-call API configuration. See CreateAgentRequest for full shape.
    
</dd>
</dl>

<dl>
<dd>

**global_prompt:** `typing.Optional[str]` — Global prompt for workflow_graph agents (max 4000 characters)
    
</dd>
</dl>

<dl>
<dd>

**global_knowledge_base_id:** `typing.Optional[str]` — Knowledge base ID to attach to this draft
    
</dd>
</dl>

<dl>
<dd>

**first_message:** `typing.Optional[str]` — Opening message for this draft
    
</dd>
</dl>

<dl>
<dd>

**allow_interruptions:** `typing.Optional[bool]` 
    
</dd>
</dl>

<dl>
<dd>

**wait_for_user_to_speak_first:** `typing.Optional[bool]` 
    
</dd>
</dl>

<dl>
<dd>

**mute_user_until_first_bot_response:** `typing.Optional[bool]` 
    
</dd>
</dl>

<dl>
<dd>

**interruption_backoff_timer:** `typing.Optional[float]` 
    
</dd>
</dl>

<dl>
<dd>

**background_sound:** `typing.Optional[DraftConfigRequestBackgroundSound]` 
    
</dd>
</dl>

<dl>
<dd>

**smart_turn_config:** `typing.Optional[typing.Dict[str, typing.Any]]` 
    
</dd>
</dl>

<dl>
<dd>

**voice_detection_config:** `typing.Optional[typing.Dict[str, typing.Any]]` 
    
</dd>
</dl>

<dl>
<dd>

**voice_mail_detection_config:** `typing.Optional[typing.Dict[str, typing.Any]]` 
    
</dd>
</dl>

<dl>
<dd>

**denoising_config:** `typing.Optional[typing.Dict[str, typing.Any]]` 
    
</dd>
</dl>

<dl>
<dd>

**redaction_config:** `typing.Optional[typing.Dict[str, typing.Any]]` 
    
</dd>
</dl>

<dl>
<dd>

**pronunciation_dicts:** `typing.Optional[typing.List[typing.Dict[str, typing.Any]]]` 
    
</dd>
</dl>

<dl>
<dd>

**llm_idle_timeout_config:** `typing.Optional[typing.Dict[str, typing.Any]]` 
    
</dd>
</dl>

<dl>
<dd>

**session_timeout_config:** `typing.Optional[typing.Dict[str, typing.Any]]` 
    
</dd>
</dl>

<dl>
<dd>

**workflow_type:** `typing.Optional[WorkflowType]` 
    
</dd>
</dl>

<dl>
<dd>

**timezone:** `typing.Optional[typing.Dict[str, typing.Any]]` 
    
</dd>
</dl>

<dl>
<dd>

**call_disposition_config:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**enable_style_guide:** `typing.Optional[bool]` 
    
</dd>
</dl>

<dl>
<dd>

**speech_formatting:** `typing.Optional[bool]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Atoms AgentVersioningVersions
<details><summary><code>client.atoms.agent_versioning_versions.<a href="src/smallestai/atoms/agent_versioning_versions/client.py">list_published_versions</a>(...) -> GetAgentIdVersionsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

**Deprecated on the v2 branch model.** Migrate to `GET /agent/{id}/branches/{branchId}/revisions`. When `ENABLE_BRANCH_MODEL` is on, this endpoint returns `409 versioning_v2_migration_required` with the `Deprecation: true` header. See the [migration guide](/voice-agents/deprecations/agent-versioning-migration).

|
List published versions for an agent with pagination and optional pin filter.
The `total` value currently represents the total number of published versions
for the agent, not necessarily the filtered count when `isPinned` is used.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.agent_versioning_versions.list_published_versions(
    id="id",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The agent ID.
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Number of versions to return (1-100, default 20)
    
</dd>
</dl>

<dl>
<dd>

**skip:** `typing.Optional[int]` — Number of versions to skip (default 0)
    
</dd>
</dl>

<dl>
<dd>

**is_pinned:** `typing.Optional[bool]` — Filter by pinned status
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.agent_versioning_versions.<a href="src/smallestai/atoms/agent_versioning_versions/client.py">diff_two_versions</a>(...) -> GetAgentIdVersionsDiffResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

**Deprecated.** Kept working during the v1 coexistence window (~1 month). Migrate to `GET /agent/{id}/diff?a=<revisionId>&b=<revisionId>`. Will be removed at the sunset date.

Compare two version or draft revision records side-by-side by their IDs. The implementation tries published versions first and can fall back to the latest draft revision.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.agent_versioning_versions.diff_two_versions(
    id="id",
    version_a="versionA",
    version_b="versionB",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The agent ID.
    
</dd>
</dl>

<dl>
<dd>

**version_a:** `str` — ID of the first version
    
</dd>
</dl>

<dl>
<dd>

**version_b:** `str` — ID of the second version
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.agent_versioning_versions.<a href="src/smallestai/atoms/agent_versioning_versions/client.py">get_version_detail</a>(...) -> GetAgentIdVersionsVersionIdResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

**Deprecated.** By-id reads are kept working during the v1 coexistence window (~1 month). A v1 `versionId` equals its migrated `revisionId`, so this continues to resolve across branches. Migrate to `GET /agent/{id}/branches/{branchId}/revisions/{revisionId}`. Will be removed at the sunset date.

|
Returns the full detail of a specific published version (read-only).
Published versions are config-immutable — to modify config, create a draft from
this version and publish it as a new version.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.agent_versioning_versions.get_version_detail(
    id="id",
    version_id="versionId",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The agent ID.
    
</dd>
</dl>

<dl>
<dd>

**version_id:** `str` — The published version ID
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.agent_versioning_versions.<a href="src/smallestai/atoms/agent_versioning_versions/client.py">update_version_metadata</a>(...) -> UpdateVersionMetadataAgentVersioningVersionsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

**Deprecated on the v2 branch model.** Migrate to `Metadata edits removed on v2. Set `label` at publish via `POST /agent/{id}/branches/{branchId}/draft/publish`.`. When `ENABLE_BRANCH_MODEL` is on, this endpoint returns `409 versioning_v2_migration_required` with the `Deprecation: true` header. See the [migration guide](/voice-agents/deprecations/agent-versioning-migration).

|
Update a published version's label, description, or pinned status. At least one field is required.
Published versions (both active and inactive) are config-immutable — their agent
configuration cannot be changed. To modify config, create a new draft from the version,
edit the draft, and publish it as a new version.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.agent_versioning_versions.update_version_metadata(
    id="id",
    version_id="versionId",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The agent ID.
    
</dd>
</dl>

<dl>
<dd>

**version_id:** `str` — The published version ID
    
</dd>
</dl>

<dl>
<dd>

**label:** `typing.Optional[str]` — Version label
    
</dd>
</dl>

<dl>
<dd>

**description:** `typing.Optional[str]` — Version description
    
</dd>
</dl>

<dl>
<dd>

**is_pinned:** `typing.Optional[bool]` — Pin or unpin the version
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.agent_versioning_versions.<a href="src/smallestai/atoms/agent_versioning_versions/client.py">activate_version</a>(...) -> ActivateVersionAgentVersioningVersionsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

**Deprecated on the v2 branch model.** Migrate to `POST /agent/{id}/branches/{branchId}/live or POST /agent/{id}/branches/{branchId}/revisions/{revisionId}/restore`. When `ENABLE_BRANCH_MODEL` is on, this endpoint returns `409 versioning_v2_migration_required` with the `Deprecation: true` header. See the [migration guide](/voice-agents/deprecations/agent-versioning-migration).

|
Set a published version as the active version for the agent. The previously
active version is deactivated. This does not modify the version's config — it
only changes which version serves live traffic. Activation is idempotent: if
the version is already active, the endpoint returns that version without
changing config.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.agent_versioning_versions.activate_version(
    id="id",
    version_id="versionId",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The agent ID.
    
</dd>
</dl>

<dl>
<dd>

**version_id:** `str` — The published version ID
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.agent_versioning_versions.<a href="src/smallestai/atoms/agent_versioning_versions/client.py">test_call_with_version_config</a>(...) -> PostAgentIdVersionsVersionIdTestCallResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

**Deprecated.** Test-calls are exempt from the v1 write-block and remain functional. Migrate to `POST /agent/{id}/branches/{branchId}/test-call` with `revisionId`. Will be removed at the sunset date.

|
Initiate a test call using a specific published version's configuration.
The response always includes `conversationId` and `callId`. For `webcall`
and `chat`, it also includes `token`, `roomName`, and `host`. Those fields
are omitted for `telephony`.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.agent_versioning_versions.test_call_with_version_config(
    id="id",
    version_id="versionId",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The agent ID.
    
</dd>
</dl>

<dl>
<dd>

**version_id:** `str` — The published version ID
    
</dd>
</dl>

<dl>
<dd>

**request:** `TestCallRequest` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Atoms AgentVersioningBranches
<details><summary><code>client.atoms.agent_versioning_branches.<a href="src/smallestai/atoms/agent_versioning_branches/client.py">list</a>(...) -> ListAgentVersioningBranchesResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

List all non-archived branches for an agent, with per-branch draft and revision counts.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.agent_versioning_branches.list(
    id="id",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The agent ID.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.agent_versioning_branches.<a href="src/smallestai/atoms/agent_versioning_branches/client.py">create_branch</a>(...) -> CreateBranchAgentVersioningBranchesResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Fork a new branch from an existing branch. The source branch must have at least one committed revision. Branch names are unique per agent; the name `Main` is reserved for the default branch. Creating from a branch whose latest draft is still `scanning` returns `409 source_scanning`.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.agent_versioning_branches.create_branch(
    id="id",
    source_branch_id="sourceBranchId",
    name="name",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The agent ID.
    
</dd>
</dl>

<dl>
<dd>

**source_branch_id:** `str` — Branch to fork from. Its head revision must exist.
    
</dd>
</dl>

<dl>
<dd>

**name:** `str` — New branch name. Unique per agent among active branches. `main` is reserved.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.agent_versioning_branches.<a href="src/smallestai/atoms/agent_versioning_branches/client.py">get</a>(...) -> GetAgentVersioningBranchesResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Return a single branch summary, including draft state (`openDraftId`, `hasOpenDraft`) and head revision.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.agent_versioning_branches.get(
    id="id",
    branch_id="branchId",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The agent ID.
    
</dd>
</dl>

<dl>
<dd>

**branch_id:** `str` — The branch ID.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.agent_versioning_branches.<a href="src/smallestai/atoms/agent_versioning_branches/client.py">rename</a>(...) -> RenameAgentVersioningBranchesResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Rename a non-default, non-archived branch. `Main` cannot be renamed; a name that is already in use on this agent returns `409 branch_name_exists`.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.agent_versioning_branches.rename(
    id="id",
    branch_id="branchId",
    name="name",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The agent ID.
    
</dd>
</dl>

<dl>
<dd>

**branch_id:** `str` — The branch ID.
    
</dd>
</dl>

<dl>
<dd>

**name:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.agent_versioning_branches.<a href="src/smallestai/atoms/agent_versioning_branches/client.py">archive</a>(...) -> ArchiveAgentVersioningBranchesResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Archive a branch. `Main` cannot be archived. The live branch cannot be archived; make another branch live first. Archived branches are hidden from list views but their revisions remain queryable by ID.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.agent_versioning_branches.archive(
    id="id",
    branch_id="branchId",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The agent ID.
    
</dd>
</dl>

<dl>
<dd>

**branch_id:** `str` — The branch ID.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.agent_versioning_branches.<a href="src/smallestai/atoms/agent_versioning_branches/client.py">make_live</a>(...) -> MakeLiveAgentVersioningBranchesResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Make this branch the live branch. Its `headRevisionId` becomes the config that serves production traffic. The previously-live branch becomes not-live automatically. The branch must be non-archived, must have at least one `committed` (security-passed) revision, and its head revision must have passed the security scan.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.agent_versioning_branches.make_live(
    id="id",
    branch_id="branchId",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The agent ID.
    
</dd>
</dl>

<dl>
<dd>

**branch_id:** `str` — The branch ID.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.agent_versioning_branches.<a href="src/smallestai/atoms/agent_versioning_branches/client.py">get_draft</a>(...) -> GetDraftAgentVersioningBranchesResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Return the currently-open draft on this branch, including per-edit history.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.agent_versioning_branches.get_draft(
    id="id",
    branch_id="branchId",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The agent ID.
    
</dd>
</dl>

<dl>
<dd>

**branch_id:** `str` — The branch ID.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.agent_versioning_branches.<a href="src/smallestai/atoms/agent_versioning_branches/client.py">update_draft</a>(...) -> UpdateDraftAgentVersioningBranchesResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Upsert the open draft on this branch. If no draft is open, one is created automatically. The request body is an agent config partial in the same camelCase shape as `GET /agent/{id}` (`globalPrompt`, `firstMessage`, `synthesizer`, `language`, `voiceDetectionConfig`, `smartTurnConfig`, ...) and must contain at least one recognized field; the server merges it into the existing draft and returns the resulting draft as a revision-shaped snapshot.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.agent_versioning_branches.update_draft(
    id="id",
    branch_id="branchId",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The agent ID.
    
</dd>
</dl>

<dl>
<dd>

**branch_id:** `str` — The branch ID.
    
</dd>
</dl>

<dl>
<dd>

**expected_revision:** `typing.Optional[int]` — Optimistic-concurrency control. The `draftRevision` the client's edit was based on. When present, the server runs a field-level conflict check and rejects with `409 DraftConflictError` if the same field was changed by another edit since. Omit for last-write-wins semantics (which is also how a client force-overwrites after a `409`). Referencing a non-existent base revision returns `409 { errors: ["base_revision_unavailable"] }`.
    
</dd>
</dl>

<dl>
<dd>

**global_prompt:** `typing.Optional[str]` — Top-level system prompt shown to the agent every turn.
    
</dd>
</dl>

<dl>
<dd>

**first_message:** `typing.Optional[str]` — The agent's opening line at call start.
    
</dd>
</dl>

<dl>
<dd>

**slm_model:** `typing.Optional[UpdateBranchDraftRequestSlmModel]` — LLM model powering the agent. See `CreateAgentRequest.slmModel` for org-level access notes.
    
</dd>
</dl>

<dl>
<dd>

**background_sound:** `typing.Optional[UpdateBranchDraftRequestBackgroundSound]` — Ambient background sound during calls.
    
</dd>
</dl>

<dl>
<dd>

**timezone:** `typing.Optional[str]` — IANA timezone identifier used for date/time interpretation in prompts and tool calls.
    
</dd>
</dl>

<dl>
<dd>

**global_knowledge_base_id:** `typing.Optional[str]` — Knowledge base attached to the agent for retrieval-augmented responses.
    
</dd>
</dl>

<dl>
<dd>

**mute_user_until_first_bot_response:** `typing.Optional[bool]` 
    
</dd>
</dl>

<dl>
<dd>

**allow_interruptions:** `typing.Optional[bool]` 
    
</dd>
</dl>

<dl>
<dd>

**wait_for_user_to_speak_first:** `typing.Optional[bool]` 
    
</dd>
</dl>

<dl>
<dd>

**interruption_backoff_timer:** `typing.Optional[float]` 
    
</dd>
</dl>

<dl>
<dd>

**enable_style_guide:** `typing.Optional[bool]` 
    
</dd>
</dl>

<dl>
<dd>

**synthesizer:** `typing.Optional[typing.Dict[str, typing.Any]]` — TTS (voice) configuration. Same shape as `CreateAgentRequest.synthesizer`.
    
</dd>
</dl>

<dl>
<dd>

**language:** `typing.Optional[typing.Dict[str, typing.Any]]` — Language configuration. Same shape as `CreateAgentRequest.language`.
    
</dd>
</dl>

<dl>
<dd>

**default_variables:** `typing.Optional[typing.Dict[str, typing.Any]]` — Default variables injected into prompts and tool calls.
    
</dd>
</dl>

<dl>
<dd>

**pre_call_api:** `typing.Optional[typing.Dict[str, typing.Any]]` — Pre-call API webhook config. Same shape as `CreateAgentRequest.preCallAPI`.
    
</dd>
</dl>

<dl>
<dd>

**smart_turn_config:** `typing.Optional[typing.Dict[str, typing.Any]]` 
    
</dd>
</dl>

<dl>
<dd>

**voice_detection_config:** `typing.Optional[typing.Dict[str, typing.Any]]` 
    
</dd>
</dl>

<dl>
<dd>

**voice_mail_detection_config:** `typing.Optional[typing.Dict[str, typing.Any]]` 
    
</dd>
</dl>

<dl>
<dd>

**denoising_config:** `typing.Optional[typing.Dict[str, typing.Any]]` 
    
</dd>
</dl>

<dl>
<dd>

**redaction_config:** `typing.Optional[typing.Dict[str, typing.Any]]` 
    
</dd>
</dl>

<dl>
<dd>

**pronunciation_dicts:** `typing.Optional[typing.Dict[str, typing.Any]]` 
    
</dd>
</dl>

<dl>
<dd>

**llm_idle_timeout_config:** `typing.Optional[typing.Dict[str, typing.Any]]` 
    
</dd>
</dl>

<dl>
<dd>

**session_timeout_config:** `typing.Optional[typing.Dict[str, typing.Any]]` 
    
</dd>
</dl>

<dl>
<dd>

**call_disposition_config:** `typing.Optional[typing.Dict[str, typing.Any]]` 
    
</dd>
</dl>

<dl>
<dd>

**speech_formatting:** `typing.Optional[typing.Dict[str, typing.Any]]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.agent_versioning_branches.<a href="src/smallestai/atoms/agent_versioning_branches/client.py">discard_draft</a>(...) -> DiscardDraftAgentVersioningBranchesResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Discard the open draft on this branch. Any unpublished edits are lost. The last committed revision remains the branch head.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.agent_versioning_branches.discard_draft(
    id="id",
    branch_id="branchId",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The agent ID.
    
</dd>
</dl>

<dl>
<dd>

**branch_id:** `str` — The branch ID.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.agent_versioning_branches.<a href="src/smallestai/atoms/agent_versioning_branches/client.py">publish_draft</a>(...) -> PublishDraftAgentVersioningBranchesResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Publish the open draft on this branch as a new revision.

The response is `200` with `state: "committed"` when the security scan finishes synchronously, and `202` with `state: "scanning"` when the scan is deferred. A `scanning` revision is visible in history but cannot be restored or made live until it becomes `committed`. If the scan fails, the revision is left in `scanning` state and this endpoint returns `409` on subsequent publishes until the scan is retried.

Publishing on the live branch pushes to production immediately.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.agent_versioning_branches.publish_draft(
    id="id",
    branch_id="branchId",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The agent ID.
    
</dd>
</dl>

<dl>
<dd>

**branch_id:** `str` — The branch ID.
    
</dd>
</dl>

<dl>
<dd>

**label:** `typing.Optional[str]` — Optional label saved on the committed revision.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.agent_versioning_branches.<a href="src/smallestai/atoms/agent_versioning_branches/client.py">cancel_publish</a>(...) -> CancelPublishAgentVersioningBranchesResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Cancel a publish that is currently scanning. Idempotent. Returns `200` even if no scan is active.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.agent_versioning_branches.cancel_publish(
    id="id",
    branch_id="branchId",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The agent ID.
    
</dd>
</dl>

<dl>
<dd>

**branch_id:** `str` — The branch ID.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.agent_versioning_branches.<a href="src/smallestai/atoms/agent_versioning_branches/client.py">test_call</a>(...) -> TestCallAgentVersioningBranchesResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Start a test call using the branch's current config. Send `includeDraft: true` to test the open draft, or send `revisionId` to test a specific committed revision on the branch. Sending both is a validation error.

The response always includes `conversationId` and `callId`. For `webcall` and `chat`, it also includes `token`, `roomName`, and `host`. Those fields are omitted for `telephony`.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.agent_versioning_branches.test_call(
    id="id",
    branch_id="branchId",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The agent ID.
    
</dd>
</dl>

<dl>
<dd>

**branch_id:** `str` — The branch ID.
    
</dd>
</dl>

<dl>
<dd>

**include_draft:** `typing.Optional[bool]` — When `true`, the test call uses the branch's open draft. Mutually exclusive with `revisionId`.
    
</dd>
</dl>

<dl>
<dd>

**revision_id:** `typing.Optional[str]` — Test against a specific committed revision on the branch. Mutually exclusive with `includeDraft: true`.
    
</dd>
</dl>

<dl>
<dd>

**mode:** `typing.Optional[TestCallV2RequestMode]` 
    
</dd>
</dl>

<dl>
<dd>

**to_phone:** `typing.Optional[str]` — E.164-formatted number. Required when `mode` is `telephony`. Omit for `webcall` and `chat`.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Atoms AgentVersioningRevisions
<details><summary><code>client.atoms.agent_versioning_revisions.<a href="src/smallestai/atoms/agent_versioning_revisions/client.py">list</a>(...) -> ListAgentVersioningRevisionsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Paginated list of committed and scanning revisions on this branch, newest first.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.agent_versioning_revisions.list(
    id="id",
    branch_id="branchId",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The agent ID.
    
</dd>
</dl>

<dl>
<dd>

**branch_id:** `str` — The branch ID.
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**skip:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.agent_versioning_revisions.<a href="src/smallestai/atoms/agent_versioning_revisions/client.py">get</a>(...) -> GetAgentVersioningRevisionsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Return a single revision plus its `resolvedConfig` (the fully-merged agent config at that revision).
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.agent_versioning_revisions.get(
    id="id",
    branch_id="branchId",
    revision_id="revisionId",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The agent ID.
    
</dd>
</dl>

<dl>
<dd>

**branch_id:** `str` — The branch ID.
    
</dd>
</dl>

<dl>
<dd>

**revision_id:** `str` — The revision ID. Equal to the v1 `versionId` for revisions that were migrated from the v1 model.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.agent_versioning_revisions.<a href="src/smallestai/atoms/agent_versioning_revisions/client.py">get_history</a>(...) -> GetHistoryAgentVersioningRevisionsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Return the publish trail for a revision: who published it, and the ordered list of prior revisions on this branch with the sections that changed at each step.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.agent_versioning_revisions.get_history(
    id="id",
    branch_id="branchId",
    revision_id="revisionId",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The agent ID.
    
</dd>
</dl>

<dl>
<dd>

**branch_id:** `str` — The branch ID.
    
</dd>
</dl>

<dl>
<dd>

**revision_id:** `str` — The revision ID. Equal to the v1 `versionId` for revisions that were migrated from the v1 model.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.agent_versioning_revisions.<a href="src/smallestai/atoms/agent_versioning_revisions/client.py">restore</a>(...) -> RestoreAgentVersioningRevisionsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Republish an older revision as a new revision at the head of this branch. Restore does not overwrite history; the older revision keeps its ID, and a new revision is committed on top.

The response mirrors `POST /agent/{id}/branches/{branchId}/draft/publish`: `200 committed` if the scan is synchronous, `202 scanning` if deferred. Only one publish or restore can be in flight per branch at a time.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.agent_versioning_revisions.restore(
    id="id",
    branch_id="branchId",
    revision_id="revisionId",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The agent ID.
    
</dd>
</dl>

<dl>
<dd>

**branch_id:** `str` — The branch ID.
    
</dd>
</dl>

<dl>
<dd>

**revision_id:** `str` — The revision ID. Equal to the v1 `versionId` for revisions that were migrated from the v1 model.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.agent_versioning_revisions.<a href="src/smallestai/atoms/agent_versioning_revisions/client.py">diff</a>(...) -> DiffAgentVersioningRevisionsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Compare any two references on this agent and return per-section diffs. Each side (`a` and `b`) is either a `revisionId` or the string `<branchId>:draft` to reference the open draft on a branch. Sides may cross branches. Both references must resolve to configs on the same agent.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.agent_versioning_revisions.diff(
    id="id",
    a="a",
    b="b",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The agent ID.
    
</dd>
</dl>

<dl>
<dd>

**a:** `str` — Left-hand side. Either a `revisionId` (24-hex ObjectId) or the token `<branchId>:draft`.
    
</dd>
</dl>

<dl>
<dd>

**b:** `str` — Right-hand side. Either a `revisionId` (24-hex ObjectId) or the token `<branchId>:draft`.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Atoms PromptScoring
<details><summary><code>client.atoms.prompt_scoring.<a href="src/smallestai/atoms/prompt_scoring/client.py">score_a_prompt</a>(...) -> PostPromptScoringScoreResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Scores an agent's prompt across 11 quality dimensions using Gemini-based analysis. Requires the prompt to have changed since the last scoring.

**Input:** Provide exactly one of `versionId` (published agent version) or `draftId` (agent draft). Providing both or neither returns a 400.

**Credit usage:** 1 credit is deducted per successful call.

**Idempotency:** Re-submitting the same prompt without changes returns a 400 — retrieve the cached score via the GET agent endpoint instead.

**Supported agent types:** Only `single_prompt` agents are supported. Workflow-graph agents return a 400.

**Scoring model:** Two sequential Gemini calls — a Platform Analyst pass followed by a Rubric Judge pass.

### Scored Dimensions

| Tier | Dimension | Notes |
|------|-----------|-------|
| 1 | Role & Objective | |
| 1 | Personality & Voice | |
| 1 | Conversation Structure | |
| 1 | Tool Integration | |
| 1 | Constraints & Safety | |
| 2 | Conversational Naturalness | |
| 2 | Failure-Mode Coverage | |
| 3 | Information Integrity | Gating — if Weak/Missing, score capped at 70 |
| 3 | Variable & Tool Hygiene | Gating — if Weak/Missing, score capped at 50 |
| 3 | Internal Consistency | |
| 3 | Density | Computed from token analysis |
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment
from smallestai.atoms.prompt_scoring import PostPromptScoringScoreRequestVersionId

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.prompt_scoring.score_a_prompt(
    request=PostPromptScoringScoreRequestVersionId(
        version_id="6a1589b75e048394eb37bc47",
    ),
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request:** `PostPromptScoringScoreRequest` — Exactly one of `versionId` or `draftId` must be provided.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Analytics
<details><summary><code>client.atoms.analytics.<a href="src/smallestai/atoms/analytics/client.py">get_call_counts_log</a>(...) -> GetCallCountsLogResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Paginated listing of call records for the organization, with optional filtering by agent, campaign, call type, and date range.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.analytics.get_call_counts_log()
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**agent_id:** `typing.Optional[str]` — Comma-separated agent IDs to filter results
    
</dd>
</dl>

<dl>
<dd>

**campaign_id:** `typing.Optional[str]` — Campaign ID to filter results
    
</dd>
</dl>

<dl>
<dd>

**call_type:** `typing.Optional[str]` — Type of call to filter (e.g. `inbound`, `outbound`)
    
</dd>
</dl>

<dl>
<dd>

**date_from:** `typing.Optional[datetime.datetime]` — Start of date range (ISO 8601)
    
</dd>
</dl>

<dl>
<dd>

**date_to:** `typing.Optional[datetime.datetime]` — End of date range (ISO 8601)
    
</dd>
</dl>

<dl>
<dd>

**page:** `typing.Optional[int]` — Page number (default 1)
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Records per page (default 10)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.analytics.<a href="src/smallestai/atoms/analytics/client.py">get_call_counts_by_day</a>(...) -> GetCallCountsByDayResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns call counts aggregated per calendar day, suitable for bar chart visualizations.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.analytics.get_call_counts_by_day()
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**agent_id:** `typing.Optional[str]` — Comma-separated agent IDs to filter results
    
</dd>
</dl>

<dl>
<dd>

**campaign_id:** `typing.Optional[str]` — Campaign ID to filter results
    
</dd>
</dl>

<dl>
<dd>

**call_type:** `typing.Optional[str]` — Type of call to filter (e.g. `inbound`, `outbound`)
    
</dd>
</dl>

<dl>
<dd>

**date_from:** `typing.Optional[datetime.datetime]` — Start of date range (ISO 8601)
    
</dd>
</dl>

<dl>
<dd>

**date_to:** `typing.Optional[datetime.datetime]` — End of date range (ISO 8601)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.analytics.<a href="src/smallestai/atoms/analytics/client.py">get_conversation_details</a>(...) -> GetConversationDetailsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns the full transcript and event stream for a specific call, reconstructed from ClickHouse event data.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.analytics.get_conversation_details(
    call_id="callId",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**call_id:** `str` — Unique identifier for the call
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.analytics.<a href="src/smallestai/atoms/analytics/client.py">get_usage_timeseries</a>(...) -> GetUsageTimeseriesResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns daily credit usage over a date range.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.analytics.get_usage_timeseries()
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**date_from:** `typing.Optional[datetime.datetime]` — Start of date range (ISO 8601)
    
</dd>
</dl>

<dl>
<dd>

**date_to:** `typing.Optional[datetime.datetime]` — End of date range (ISO 8601)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.analytics.<a href="src/smallestai/atoms/analytics/client.py">get_dashboard</a>(...) -> GetDashboardResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Batched endpoint that fetches all dashboard panels in a single request by running six sub-queries in parallel. Equivalent to calling `summary`, `call-volume-timeseries`, `call-outcomes-timeseries`, `pickup-rate-by-number`, `hourly-performance`, and `duration-stats` individually. Each field may be absent if that sub-query failed; partial data is still returned.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.analytics.get_dashboard()
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**agent_id:** `typing.Optional[str]` — Comma-separated agent IDs to filter results
    
</dd>
</dl>

<dl>
<dd>

**campaign_id:** `typing.Optional[str]` — Campaign ID to filter results
    
</dd>
</dl>

<dl>
<dd>

**call_type:** `typing.Optional[str]` — Type of call to filter (e.g. `inbound`, `outbound`)
    
</dd>
</dl>

<dl>
<dd>

**date_from:** `typing.Optional[datetime.datetime]` — Start of date range (ISO 8601)
    
</dd>
</dl>

<dl>
<dd>

**date_to:** `typing.Optional[datetime.datetime]` — End of date range (ISO 8601)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.analytics.<a href="src/smallestai/atoms/analytics/client.py">get_analytics_summary</a>(...) -> GetAnalyticsSummaryResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns high-level KPI metrics with current period value, previous period value, and percent change for trend comparison.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.analytics.get_analytics_summary()
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**agent_id:** `typing.Optional[str]` — Comma-separated agent IDs to filter results
    
</dd>
</dl>

<dl>
<dd>

**campaign_id:** `typing.Optional[str]` — Campaign ID to filter results
    
</dd>
</dl>

<dl>
<dd>

**call_type:** `typing.Optional[str]` — Type of call to filter (e.g. `inbound`, `outbound`)
    
</dd>
</dl>

<dl>
<dd>

**date_from:** `typing.Optional[datetime.datetime]` — Start of date range (ISO 8601)
    
</dd>
</dl>

<dl>
<dd>

**date_to:** `typing.Optional[datetime.datetime]` — End of date range (ISO 8601)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.analytics.<a href="src/smallestai/atoms/analytics/client.py">get_call_volume_timeseries</a>(...) -> GetCallVolumeTimeseriesResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns daily call volume broken down by outcome (answered, no-answer, failed, cancelled) over the selected period.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.analytics.get_call_volume_timeseries()
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**agent_id:** `typing.Optional[str]` — Comma-separated agent IDs to filter results
    
</dd>
</dl>

<dl>
<dd>

**campaign_id:** `typing.Optional[str]` — Campaign ID to filter results
    
</dd>
</dl>

<dl>
<dd>

**call_type:** `typing.Optional[str]` — Type of call to filter (e.g. `inbound`, `outbound`)
    
</dd>
</dl>

<dl>
<dd>

**date_from:** `typing.Optional[datetime.datetime]` — Start of date range (ISO 8601)
    
</dd>
</dl>

<dl>
<dd>

**date_to:** `typing.Optional[datetime.datetime]` — End of date range (ISO 8601)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.analytics.<a href="src/smallestai/atoms/analytics/client.py">get_pickup_rate_by_number</a>(...) -> GetPickupRateByNumberResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns pickup rate and call volume broken down per originating phone number.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.analytics.get_pickup_rate_by_number()
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**agent_id:** `typing.Optional[str]` — Comma-separated agent IDs to filter results
    
</dd>
</dl>

<dl>
<dd>

**campaign_id:** `typing.Optional[str]` — Campaign ID to filter results
    
</dd>
</dl>

<dl>
<dd>

**call_type:** `typing.Optional[str]` — Type of call to filter (e.g. `inbound`, `outbound`)
    
</dd>
</dl>

<dl>
<dd>

**date_from:** `typing.Optional[datetime.datetime]` — Start of date range (ISO 8601)
    
</dd>
</dl>

<dl>
<dd>

**date_to:** `typing.Optional[datetime.datetime]` — End of date range (ISO 8601)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.analytics.<a href="src/smallestai/atoms/analytics/client.py">get_phone_number_trends</a>(...) -> GetPhoneNumberTrendsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns per-phone-number call volume and pickup rate as a daily timeseries, useful for spotting number-level degradation over time.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.analytics.get_phone_number_trends()
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**agent_id:** `typing.Optional[str]` — Comma-separated agent IDs to filter results
    
</dd>
</dl>

<dl>
<dd>

**campaign_id:** `typing.Optional[str]` — Campaign ID to filter results
    
</dd>
</dl>

<dl>
<dd>

**call_type:** `typing.Optional[str]` — Type of call to filter (e.g. `inbound`, `outbound`)
    
</dd>
</dl>

<dl>
<dd>

**date_from:** `typing.Optional[datetime.datetime]` — Start of date range (ISO 8601)
    
</dd>
</dl>

<dl>
<dd>

**date_to:** `typing.Optional[datetime.datetime]` — End of date range (ISO 8601)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.analytics.<a href="src/smallestai/atoms/analytics/client.py">get_hourly_performance</a>(...) -> GetHourlyPerformanceResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns call volume and performance metrics broken down by hour of day (0–23), aggregated across the selected date range.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.analytics.get_hourly_performance()
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**agent_id:** `typing.Optional[str]` — Comma-separated agent IDs to filter results
    
</dd>
</dl>

<dl>
<dd>

**campaign_id:** `typing.Optional[str]` — Campaign ID to filter results
    
</dd>
</dl>

<dl>
<dd>

**call_type:** `typing.Optional[str]` — Type of call to filter (e.g. `inbound`, `outbound`)
    
</dd>
</dl>

<dl>
<dd>

**date_from:** `typing.Optional[datetime.datetime]` — Start of date range (ISO 8601)
    
</dd>
</dl>

<dl>
<dd>

**date_to:** `typing.Optional[datetime.datetime]` — End of date range (ISO 8601)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.analytics.<a href="src/smallestai/atoms/analytics/client.py">get_call_outcomes_timeseries</a>(...) -> GetCallOutcomesTimeseriesResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns a daily breakdown of call outcomes (answered, no-answer, failed, cancelled) over time, plus totals for the entire period.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.analytics.get_call_outcomes_timeseries()
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**agent_id:** `typing.Optional[str]` — Comma-separated agent IDs to filter results
    
</dd>
</dl>

<dl>
<dd>

**campaign_id:** `typing.Optional[str]` — Campaign ID to filter results
    
</dd>
</dl>

<dl>
<dd>

**call_type:** `typing.Optional[str]` — Type of call to filter (e.g. `inbound`, `outbound`)
    
</dd>
</dl>

<dl>
<dd>

**date_from:** `typing.Optional[datetime.datetime]` — Start of date range (ISO 8601)
    
</dd>
</dl>

<dl>
<dd>

**date_to:** `typing.Optional[datetime.datetime]` — End of date range (ISO 8601)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.analytics.<a href="src/smallestai/atoms/analytics/client.py">get_duration_stats</a>(...) -> GetDurationStatsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns call duration statistics including average, median, p90, p95 percentiles, and the proportion of short vs. long calls.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.analytics.get_duration_stats()
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**agent_id:** `typing.Optional[str]` — Comma-separated agent IDs to filter results
    
</dd>
</dl>

<dl>
<dd>

**campaign_id:** `typing.Optional[str]` — Campaign ID to filter results
    
</dd>
</dl>

<dl>
<dd>

**call_type:** `typing.Optional[str]` — Type of call to filter (e.g. `inbound`, `outbound`)
    
</dd>
</dl>

<dl>
<dd>

**date_from:** `typing.Optional[datetime.datetime]` — Start of date range (ISO 8601)
    
</dd>
</dl>

<dl>
<dd>

**date_to:** `typing.Optional[datetime.datetime]` — End of date range (ISO 8601)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.analytics.<a href="src/smallestai/atoms/analytics/client.py">get_weekly_trends</a>(...) -> GetWeeklyTrendsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns per-week call performance metrics including volume, pickup rate, and duration percentiles (p50, p90). Each week starts on Monday.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.analytics.get_weekly_trends()
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**agent_id:** `typing.Optional[str]` — Comma-separated agent IDs to filter results
    
</dd>
</dl>

<dl>
<dd>

**campaign_id:** `typing.Optional[str]` — Campaign ID to filter results
    
</dd>
</dl>

<dl>
<dd>

**call_type:** `typing.Optional[str]` — Type of call to filter (e.g. `inbound`, `outbound`)
    
</dd>
</dl>

<dl>
<dd>

**date_from:** `typing.Optional[datetime.datetime]` — Start of date range (ISO 8601)
    
</dd>
</dl>

<dl>
<dd>

**date_to:** `typing.Optional[datetime.datetime]` — End of date range (ISO 8601)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.analytics.<a href="src/smallestai/atoms/analytics/client.py">get_agent_performance</a>(...) -> GetAgentPerformanceResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns per-agent call performance metrics. Supports sorting and limiting results.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.analytics.get_agent_performance()
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**agent_id:** `typing.Optional[str]` — Comma-separated agent IDs to filter results
    
</dd>
</dl>

<dl>
<dd>

**campaign_id:** `typing.Optional[str]` — Campaign ID to filter results
    
</dd>
</dl>

<dl>
<dd>

**call_type:** `typing.Optional[str]` — Type of call to filter (e.g. `inbound`, `outbound`)
    
</dd>
</dl>

<dl>
<dd>

**date_from:** `typing.Optional[datetime.datetime]` — Start of date range (ISO 8601)
    
</dd>
</dl>

<dl>
<dd>

**date_to:** `typing.Optional[datetime.datetime]` — End of date range (ISO 8601)
    
</dd>
</dl>

<dl>
<dd>

**sort_by:** `typing.Optional[str]` — Field to sort by (e.g. `totalCalls`, `pickupRate`, `avgDuration`)
    
</dd>
</dl>

<dl>
<dd>

**sort_order:** `typing.Optional[GetAgentPerformanceRequestSortOrder]` — Sort direction
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Maximum number of agents to return
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.analytics.<a href="src/smallestai/atoms/analytics/client.py">get_analytics_concurrency</a>(...) -> GetAnalyticsConcurrencyResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns minute-by-minute concurrent call counts for a specific day. Optionally broken down per agent.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment
import datetime

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.analytics.get_analytics_concurrency(
    date=datetime.date.fromisoformat("2023-01-15"),
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**date:** `datetime.date` — Date to query (YYYY-MM-DD)
    
</dd>
</dl>

<dl>
<dd>

**agent_id:** `typing.Optional[str]` — Filter to a specific agent
    
</dd>
</dl>

<dl>
<dd>

**include_agents:** `typing.Optional[GetAnalyticsConcurrencyRequestIncludeAgents]` — Pass `true` to include a per-agent breakdown in the response
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.analytics.<a href="src/smallestai/atoms/analytics/client.py">get_call_start_distribution</a>(...) -> GetCallStartDistributionResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns the distribution of call start times as minute-level buckets for a specific day, showing when calls were initiated throughout the day.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment
import datetime

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.analytics.get_call_start_distribution(
    date=datetime.date.fromisoformat("2023-01-15"),
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**date:** `datetime.date` — Date to query (YYYY-MM-DD)
    
</dd>
</dl>

<dl>
<dd>

**agent_id:** `typing.Optional[str]` — Filter to a specific agent
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.analytics.<a href="src/smallestai/atoms/analytics/client.py">get_daily_call_summary</a>(...) -> GetDailyCallSummaryResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns an aggregate call summary for a specific day. Live in-progress and in-queue counts are merged from real-time data on top of the historical data.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment
import datetime

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.analytics.get_daily_call_summary(
    date=datetime.date.fromisoformat("2023-01-15"),
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**date:** `datetime.date` — Date to query (YYYY-MM-DD)
    
</dd>
</dl>

<dl>
<dd>

**agent_id:** `typing.Optional[str]` — Filter to a specific agent
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.analytics.<a href="src/smallestai/atoms/analytics/client.py">get_attempt_cohort</a>(...) -> GetAttemptCohortResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns cohort analysis of call attempt numbers, showing how pickup rate changes across the 1st, 2nd, 3rd (etc.) attempts to reach the same number, including cumulative rates and marginal gain per additional attempt.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.analytics.get_attempt_cohort()
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**agent_id:** `typing.Optional[str]` — Comma-separated agent IDs to filter results
    
</dd>
</dl>

<dl>
<dd>

**campaign_id:** `typing.Optional[str]` — Campaign ID to filter results
    
</dd>
</dl>

<dl>
<dd>

**call_type:** `typing.Optional[str]` — Type of call to filter (e.g. `inbound`, `outbound`)
    
</dd>
</dl>

<dl>
<dd>

**date_from:** `typing.Optional[datetime.datetime]` — Start of date range (ISO 8601)
    
</dd>
</dl>

<dl>
<dd>

**date_to:** `typing.Optional[datetime.datetime]` — End of date range (ISO 8601)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Call Actions
<details><summary><code>client.atoms.call_actions.<a href="src/smallestai/atoms/call_actions/client.py">list_call_actions</a>(...) -> ListCallActionsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns a paginated list of call actions for the organization, filtered by agent. Optionally filter by category or provider.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.call_actions.list_call_actions(
    agent_id="agentId",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**agent_id:** `str` — Filter by agent (ObjectId)
    
</dd>
</dl>

<dl>
<dd>

**page:** `typing.Optional[int]` — Page number (default 1)
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Records per page (default 10)
    
</dd>
</dl>

<dl>
<dd>

**category:** `typing.Optional[ListCallActionsRequestCategory]` — Filter by category
    
</dd>
</dl>

<dl>
<dd>

**provider:** `typing.Optional[str]` — Filter by provider name
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.call_actions.<a href="src/smallestai/atoms/call_actions/client.py">create_call_action</a>(...) -> CreateCallActionResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Creates a new call action for an agent. Call actions define automated behaviors that fire at specific points in a call lifecycle.

- **`trigger`** actions fire to initiate an outbound call and require `config.phoneNumberFieldName`.
- **`post-call`** actions fire after a call ends (e.g. to update a CRM record).
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment
from smallestai.atoms.call_actions import CreateCallActionRequestConfig

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.call_actions.create_call_action(
    agent_id="agentId",
    category="trigger",
    provider="provider",
    config=CreateCallActionRequestConfig(),
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**agent_id:** `str` — Agent this action belongs to (ObjectId)
    
</dd>
</dl>

<dl>
<dd>

**category:** `CreateCallActionRequestCategory` — When the action fires
    
</dd>
</dl>

<dl>
<dd>

**provider:** `str` — Integration provider (e.g. `hubspot`, `salesforce`)
    
</dd>
</dl>

<dl>
<dd>

**config:** `CreateCallActionRequestConfig` 
    
</dd>
</dl>

<dl>
<dd>

**action_type:** `typing.Optional[CreateCallActionRequestActionType]` — The operation to perform on the provider object
    
</dd>
</dl>

<dl>
<dd>

**object:** `typing.Optional[str]` — Provider object type to act on (e.g. `contact`, `deal`)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.call_actions.<a href="src/smallestai/atoms/call_actions/client.py">get_call_action</a>(...) -> GetCallActionResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns a single call action by ID. Scoped to the authenticated organization.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.call_actions.get_call_action(
    id="id",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — Call action ObjectId
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.call_actions.<a href="src/smallestai/atoms/call_actions/client.py">update_call_action</a>(...) -> UpdateCallActionResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Updates an existing call action. All body fields are optional — only provided fields are updated.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.call_actions.update_call_action(
    id="id",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — Call action ObjectId
    
</dd>
</dl>

<dl>
<dd>

**category:** `typing.Optional[UpdateCallActionRequestCategory]` — Change when the action fires
    
</dd>
</dl>

<dl>
<dd>

**provider:** `typing.Optional[str]` — Change the integration provider
    
</dd>
</dl>

<dl>
<dd>

**action_type:** `typing.Optional[UpdateCallActionRequestActionType]` — Change the operation type
    
</dd>
</dl>

<dl>
<dd>

**object:** `typing.Optional[str]` — Change the provider object type
    
</dd>
</dl>

<dl>
<dd>

**config:** `typing.Optional[UpdateCallActionRequestConfig]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.call_actions.<a href="src/smallestai/atoms/call_actions/client.py">delete_call_action</a>(...) -> DeleteCallActionResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Permanently deletes a call action. Scoped to the authenticated organization.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.call_actions.delete_call_action(
    id="id",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — Call action ObjectId
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Integrations
<details><summary><code>client.atoms.integrations.<a href="src/smallestai/atoms/integrations/client.py">modify_web_engage_integration</a>(...) -> ModifyWebEngageIntegrationResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Creates or updates the WebEngage integration for the organization. Replaces the existing integration configuration with the provided credential set(s).

**Note:** This endpoint returns a direct JSON response — not the standard `{ success, data }` wrapper used by other endpoints.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment
from smallestai.atoms import WebEngageIntegrationSet

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.integrations.modify_web_engage_integration(
    integration_sets=[
        WebEngageIntegrationSet(
            license_code="licenseCode",
            environment="environment",
            api_key="apiKey",
        )
    ],
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**integration_sets:** `typing.List[WebEngageIntegrationSet]` — One or more WebEngage credential sets
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.integrations.<a href="src/smallestai/atoms/integrations/client.py">get_web_engage_details</a>() -> GetWebEngageDetailsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns the current WebEngage integration configuration for the organization.

**Note:** This endpoint returns a direct JSON response — not the standard `{ success, data }` wrapper used by other endpoints.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.integrations.get_web_engage_details()
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Concurrency
<details><summary><code>client.atoms.concurrency.<a href="src/smallestai/atoms/concurrency/client.py">get_concurrency</a>() -> GetConcurrencyResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns the organization's overall concurrency limit, how much is reserved across all agents, the remaining unreserved pool, and the per-agent reservation breakdown per call channel.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.concurrency.get_concurrency()
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.concurrency.<a href="src/smallestai/atoms/concurrency/client.py">update_concurrency_reservations</a>(...) -> UpdateConcurrencyReservationsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Updates concurrency reservations for one or more agents in a single request. Replaces the existing reservation values for each specified agent. **Admin role required.**
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment
from smallestai.atoms.concurrency import UpdateConcurrencyReservationsRequestReservationsItem

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.concurrency.update_concurrency_reservations(
    reservations=[
        UpdateConcurrencyReservationsRequestReservationsItem(
            agent_id="agentId",
            webcall=1,
            outbound=1,
            inbound=1,
            chat=1,
        )
    ],
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**reservations:** `typing.List[UpdateConcurrencyReservationsRequestReservationsItem]` — Array of agent reservations to update
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Disposition Metric Templates
<details><summary><code>client.atoms.disposition_metric_templates.<a href="src/smallestai/atoms/disposition_metric_templates/client.py">list_disposition_metric_templates</a>() -> ListDispositionMetricTemplatesResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns all available disposition metric templates. These reusable definitions are used to populate the post-call analytics metric picker when configuring an agent's `postCallAnalyticsConfig`. Only a user token is required — no organization context needed.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.disposition_metric_templates.list_disposition_metric_templates()
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Atoms Dnc
<details><summary><code>client.atoms.dnc.<a href="src/smallestai/atoms/dnc/client.py">list</a>(...) -> ListDncResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Lists Do-Not-Call entries for the caller's organization with pagination, search,
and sort. Optionally scope to a single agent via `agentId`.

Each entry records a phone number that was flagged (via call outcome or manual
upload) as not-to-be-called for either the org or a specific agent.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.dnc.list()
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**agent_id:** `typing.Optional[str]` 

Optional 24-character hex agent ID. When present, restricts results to entries
for this agent. Returns 400/404 if the ID isn't valid or doesn't belong to
the caller's org.
    
</dd>
</dl>

<dl>
<dd>

**search:** `typing.Optional[str]` — Free-text search across phone numbers.
    
</dd>
</dl>

<dl>
<dd>

**sort_field:** `typing.Optional[ListDncRequestSortField]` 
    
</dd>
</dl>

<dl>
<dd>

**sort_order:** `typing.Optional[ListDncRequestSortOrder]` 
    
</dd>
</dl>

<dl>
<dd>

**page:** `typing.Optional[str]` — Page number (string-encoded positive integer, ≥ 1).
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[str]` — Page size (string-encoded; server clamps to 1–500).
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Atoms Billing
<details><summary><code>client.atoms.billing.<a href="src/smallestai/atoms/billing/client.py">get_balance</a>() -> BillingBalanceResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns the organization's current credit balance in USD plus the
current plan identifier. Organization is resolved from the API key,
so no `X-Organization-Id` header is required.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.billing.get_balance()
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.billing.<a href="src/smallestai/atoms/billing/client.py">get_ledger</a>(...) -> BillingLedgerResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Paginated credit-ledger transaction history. Ledger reads are served
from ClickHouse; a rare storage-tier outage returns an empty
`transactions` array rather than a 5xx.

**Window rules**

- `from` defaults to `to - 7 days`, `to` defaults to now.
- The span between `from` and `to` cannot exceed **90 days**. A wider
  span returns 400. Page through longer periods by making multiple
  calls with shifted `from`/`to`.
- `from` cannot be earlier than **2026-03-02T00:00:00Z**. Older
  historical data is not available via API; contact support for bulk
  exports.
- `from > to` returns 400.

**Filters**

- `type` filters to a single transaction type. `PAYMENTS` is a
  virtual filter that returns both `CREDIT_PURCHASE` and
  `AUTO_RELOAD` rows.
- `scope` filters `USAGE_DEDUCTION` rows by product category.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment
import datetime

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.billing.get_ledger(
    from_=datetime.datetime.fromisoformat("2026-07-01T00:00:00+00:00"),
    to=datetime.datetime.fromisoformat("2026-07-28T00:00:00+00:00"),
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page size (1–100).
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Offset for pagination.
    
</dd>
</dl>

<dl>
<dd>

**from:** `typing.Optional[datetime.datetime]` — Lower bound of the query window (ISO 8601, `Z`-suffixed UTC recommended). Defaults to seven days before `to`. Cannot be earlier than `2026-03-02T00:00:00Z`.
    
</dd>
</dl>

<dl>
<dd>

**to:** `typing.Optional[datetime.datetime]` — Upper bound of the query window (ISO 8601, `Z`-suffixed UTC recommended). Defaults to now.
    
</dd>
</dl>

<dl>
<dd>

**type:** `typing.Optional[GetLedgerBillingRequestType]` — Filter to a single transaction type. `PAYMENTS` is a virtual filter that returns purchase-related rows (`CREDIT_PURCHASE` + `AUTO_RELOAD`).
    
</dd>
</dl>

<dl>
<dd>

**scope:** `typing.Optional[GetLedgerBillingRequestScope]` — Filter by spend category. Applies only to `USAGE_DEDUCTION` rows.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.billing.<a href="src/smallestai/atoms/billing/client.py">get_usage_breakdown</a>() -> BillingUsageBreakdownResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Total credits spent so far, split across the three product scopes.
The window is a cumulative snapshot from **2026-03-02T00:00:00Z**
(the platform's usage-tracking start date) up to the current
instant. Served from ClickHouse. No query parameters.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.billing.get_usage_breakdown()
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.billing.<a href="src/smallestai/atoms/billing/client.py">list_invoices</a>() -> BillingInvoiceListResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns up to 20 of the most recent Stripe invoices for the caller's
organization. Each item is the raw Stripe `Invoice` object; use the
canonical Stripe reference at
[stripe.com/docs/api/invoices/object](https://stripe.com/docs/api/invoices/object)
for field-level semantics.

Organizations that have never been charged (free-tier only) return
an empty array.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.billing.list_invoices()
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.atoms.billing.<a href="src/smallestai/atoms/billing/client.py">get_invoice_pdf</a>(...) -> BillingInvoicePdfResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns a Stripe-hosted PDF URL for the invoice. The URL is
short-lived; fetch fresh when you need to hand it to a user.

Requesting an invoice that does not belong to the caller's
organization returns 404 (not 403), so a foreign invoice ID cannot
be confirmed to exist.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.billing.get_invoice_pdf(
    invoice_id="invoiceId",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**invoice_id:** `str` — Stripe invoice ID (e.g. `in_1THiCSRwh8g1U6dfOcUtTdq9`).
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Waves
<details><summary><code>client.waves.<a href="src/smallestai/waves/client.py">get_pronunciation_dicts</a>() -> typing.List[PronunciationDict]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieve all pronunciation dictionaries for the authenticated user
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.waves.get_pronunciation_dicts()
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.waves.<a href="src/smallestai/waves/client.py">create_pronunciation_dict</a>(...) -> PronunciationDict</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Create a new pronunciation dictionary for the authenticated user
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment
from smallestai.waves import PronunciationItem

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.waves.create_pronunciation_dict(
    items=[
        PronunciationItem(
            word="mysql",
            pronunciation="my-sequel",
        )
    ],
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**items:** `typing.List[PronunciationItem]` — List of word-pronunciation pairs to create
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.waves.<a href="src/smallestai/waves/client.py">update_pronunciation_dict</a>(...) -> UpdatePronunciationDictResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Update an existing pronunciation dictionary for the authenticated user
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment
from smallestai.waves import PronunciationItem

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.waves.update_pronunciation_dict(
    id="64f1234567890abcdef12345",
    items=[
        PronunciationItem(
            word="mysql",
            pronunciation="my-sequel",
        )
    ],
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — ID of the pronunciation dictionary to update
    
</dd>
</dl>

<dl>
<dd>

**items:** `typing.List[PronunciationItem]` — Updated list of word-pronunciation pairs
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.waves.<a href="src/smallestai/waves/client.py">delete_pronunciation_dict</a>(...) -> DeletePronunciationDictResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Delete an existing pronunciation dictionary for the authenticated user
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.waves.delete_pronunciation_dict(
    id="64f1234567890abcdef12345",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — ID of the pronunciation dictionary to delete
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.waves.<a href="src/smallestai/waves/client.py">synthesize_lightning</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Get speech for given text using the Waves API
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.waves.synthesize_lightning()
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**output_format:** `typing.Optional[SynthesizeLightningWavesRequestOutputFormat]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.waves.<a href="src/smallestai/waves/client.py">synthesize_lightning_large</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Get speech for given text using the Waves API
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.waves.synthesize_lightning_large()
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**output_format:** `typing.Optional[SynthesizeLightningLargeWavesRequestOutputFormat]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.waves.<a href="src/smallestai/waves/client.py">synthesize_sse_lightning_large</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

The Lightning-Large SSE API provides real-time text-to-speech streaming capabilities with high-quality voice synthesis. This API uses Server-Sent Events (SSE) to deliver audio chunks as they're generated, enabling low-latency audio playback without waiting for the entire audio file to process.

## When to Use

- **Interactive Applications**: Perfect for chatbots, virtual assistants, and other applications requiring immediate voice responses
- **Long-Form Content**: Efficiently stream audio for articles, stories, or other long-form content without buffering delays
- **Voice User Interfaces**: Create natural-sounding voice interfaces with minimal perceived latency
- **Accessibility Solutions**: Provide real-time audio versions of written content for users with visual impairments

## How It Works

1. **Make a POST Request**: Send your text and voice settings to the API endpoint
2. **Receive Audio Chunks**: The API processes your text and streams audio back as base64-encoded chunks with 1024 byte size
3. **Process the Stream**: Handle the SSE events to decode and play audio chunks sequentially
4. **End of Stream**: The API sends a completion event when all audio has been delivered
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.waves.synthesize_sse_lightning_large()
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**output_format:** `typing.Optional[SynthesizeSseLightningLargeWavesRequestOutputFormat]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.waves.<a href="src/smallestai/waves/client.py">synthesize_lightning_v2</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Get speech for given text using the Waves API
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.waves.synthesize_lightning_v2()
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**output_format:** `typing.Optional[SynthesizeLightningV2WavesRequestOutputFormat]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.waves.<a href="src/smallestai/waves/client.py">synthesize_sse_lightning_v2</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

The Lightning v2 SSE API provides real-time text-to-speech streaming capabilities with high-quality voice synthesis. This API uses Server-Sent Events (SSE) to deliver audio chunks as they're generated, enabling low-latency audio playback without waiting for the entire audio file to process.
For an end-to-end example of how to use the Lightning v2 SSE API, check out [Text to Speech (SSE) Example](https://github.com/smallest-inc/waves-examples/blob/main/lightning_v2/http_streaming/http_streaming_api.py)

## When to Use

- **Interactive Applications**: Perfect for chatbots, virtual assistants, and other applications requiring immediate voice responses
- **Long-Form Content**: Efficiently stream audio for articles, stories, or other long-form content without buffering delays
- **Voice User Interfaces**: Create natural-sounding voice interfaces with minimal perceived latency
- **Accessibility Solutions**: Provide real-time audio versions of written content for users with visual impairments

## How It Works

1. **Make a POST Request**: Send your text and voice settings to the API endpoint
2. **Receive Audio Chunks**: The API processes your text and streams audio back as base64-encoded chunks with 1024 byte size
3. **Process the Stream**: Handle the SSE events to decode and play audio chunks sequentially
4. **End of Stream**: The API sends a completion event when all audio has been delivered
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.waves.synthesize_sse_lightning_v2()
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**output_format:** `typing.Optional[SynthesizeSseLightningV2WavesRequestOutputFormat]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.waves.<a href="src/smallestai/waves/client.py">get_voices</a>(...) -> GetVoicesWavesResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

List voices available for Lightning v3.1. The response is the union of the standard and Pro voice catalogs — the API does not return a per-voice "is Pro" flag, so consult the [Lightning v3.1 Pro](/models/model-cards/text-to-speech/lightning-v-3-1-pro) and [Lightning v3.1](/models/model-cards/text-to-speech/lightning-v-3-1) model cards for the canonical per-pool voice lists. Use the `voice_id` from this response together with `"model": "lightning_v3.1"` (default) or `"model": "lightning_v3.1_pro"` on the unified `/waves/v1/tts` route to pick the pool.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.waves.get_voices(
    model="lightning-v3.1",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**model:** `GetVoicesWavesRequestModel` — The catalog to query. Currently only `lightning-v3.1` is supported — the response returns the union of standard Lightning v3.1 voices and Lightning v3.1 Pro voices. The API does not include a per-voice Pro flag; consult the model cards for the canonical per-pool catalogs.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.waves.<a href="src/smallestai/waves/client.py">synthesize_tts</a>(...) -> typing.Iterator[bytes]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Synthesize speech from text in a single request. Pass `text` + `voice_id`, get back binary audio.

Pick the model with the `model` body parameter: default `lightning_v3.1`, or `lightning_v3.1_pro` for the Pro pool. Other request parameters are identical across models.

**Language behaviour on `lightning_v3.1_pro`:** pass `language: en` for UK + American accented English, pass `language: hi` for Indian accented English + Hindi (code-switching), or omit `language` to default to `en + hi` (mixed Indian + Western English coverage). Pro supports 31 languages total (10 Indic, 8 Asian & Middle Eastern, 13 European including Dutch and Swedish). Pass the matching ISO 639-1 code (e.g. `ta`, `de`, `ja`) with a Pro voice from that language, or use `auto` to route across all supported languages with any English or Hindi voice. See the [Lightning v3.1 Pro model card](/models/model-cards/text-to-speech/lightning-v-3-1-pro#supported-languages) for the full list. On `lightning_v3.1` the model accepts 20 language codes (10 European + 10 Indic) plus `auto`; the trained voice catalog covers 12 of those directly.

## When to use this

- **Use this** for short utterances you can render before playback (notifications, prompts, batch jobs, audio file generation).
- **Use `/waves/v1/tts/live`** when you want playback to start before the full audio is ready (long passages, latency-sensitive apps).
- **Use `/waves/v1/tts/live`** (WebSocket) when text arrives incrementally (LLM token streams, live captioning).

## Key features

- 44 kHz natural, expressive synthesis
- Model selectable per request via `model` body parameter
- Cloned voice IDs (`voice_*`) work on `lightning_v3.1` — same param as catalog voices
- 20 accepted language codes on `lightning_v3.1` (12 with trained voices, 8 additional routed via English/Hindi voices). On `lightning_v3.1_pro`: 31 languages with dedicated voices (10 Indic, 8 Asian & Middle Eastern, 13 European); `language: en` → UK + American accented English; `language: hi` → Indian accented English + Hindi; omit `language` → defaults to `en + hi`. Both models accept `language: auto` for cross-language routing.
- Output formats: `pcm`, `mp3`, `wav`, `ulaw`, `alaw`
- Sample rates: 8 kHz – 44.1 kHz
- Speed: 0.5× – 2×
- Per-call pronunciation dictionaries via `pronunciation_dicts`

## Examples

**cURL — Lightning v3.1 (default)**
```bash
curl -X POST "https://api.smallest.ai/waves/v1/tts" \
  -H "Authorization: Bearer $SMALLEST_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept: audio/wav" \
  -d '{
    "text": "Hello from Waves TTS.",
    "voice_id": "magnus",
    "sample_rate": 24000,
    "output_format": "wav"
  }' --output speech.wav
```

**cURL — Lightning v3.1 Pro (omit `language` → defaults to `en + hi`)**
```bash
curl -X POST "https://api.smallest.ai/waves/v1/tts" \
  -H "Authorization: Bearer $SMALLEST_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept: audio/wav" \
  -d '{
    "text": "Hello from the Lightning v3.1 Pro pool.",
    "voice_id": "meher",
    "model": "lightning_v3.1_pro",
    "sample_rate": 24000,
    "output_format": "wav"
  }' --output speech.wav
```

**cURL — Lightning v3.1 Pro with explicit `language: en` (UK + American accented English)**
```bash
curl -X POST "https://api.smallest.ai/waves/v1/tts" \
  -H "Authorization: Bearer $SMALLEST_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept: audio/wav" \
  -d '{
    "text": "Good morning, this is a Pro voice speaking.",
    "voice_id": "meher",
    "model": "lightning_v3.1_pro",
    "language": "en",
    "sample_rate": 24000,
    "output_format": "wav"
  }' --output speech.wav
```

**cURL — Lightning v3.1 Pro with explicit `language: hi` (Indian accented English + Hindi)**
```bash
curl -X POST "https://api.smallest.ai/waves/v1/tts" \
  -H "Authorization: Bearer $SMALLEST_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept: audio/wav" \
  -d '{
    "text": "Namaste, this is an Indian-accented Pro voice.",
    "voice_id": "meher",
    "model": "lightning_v3.1_pro",
    "language": "hi",
    "sample_rate": 24000,
    "output_format": "wav"
  }' --output speech.wav
```

## Common gotchas

- **Set `Accept: audio/wav`.** Omitting it can return an empty or unplayable response.
- **Pair voice IDs with the right model.** Voice catalogs differ between `lightning_v3.1` and `lightning_v3.1_pro`. The API does not reject mismatched pairings, but using a Pro-only `voice_id` with `model=lightning_v3.1` (or omitting `model`) can return wrong or hallucinated audio. Pair Pro voices with `model=lightning_v3.1_pro`; standard catalog voices with `model=lightning_v3.1` (the default).
- **Cloned voices** (`voice_*` from `add_voice`) work with `lightning_v3.1` only; voice cloning is not available on `lightning_v3.1_pro`.
- **44.1 kHz output** is supported but most playback environments are happy with 24 kHz — drop the sample rate if bandwidth matters.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.waves.synthesize_tts(
    text="Hello from Waves TTS.",
    voice_id="magnus",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**accept:** `typing.Literal` — Must be `audio/wav` to receive binary audio. Required for proper playback.
    
</dd>
</dl>

<dl>
<dd>

**request:** `TtsRequest` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.waves.<a href="src/smallestai/waves/client.py">synthesize_sse_tts</a>(...) -> typing.Iterator[bytes]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Synthesize speech and stream the audio back over Server-Sent Events. Same body as `/waves/v1/tts` — the only difference is the response is a stream of base64-encoded PCM chunks instead of one binary blob.

Pick the model with the `model` body parameter, same as the sync route.

<Note>
  **The same URL serves the WebSocket endpoint.** `wss://api.smallest.ai/waves/v1/tts/live` accepts a WebSocket upgrade for streaming-text scenarios (LLM token streams, live captioning). The HTTP `POST` documented on this page returns SSE; use `wss://` to use the WebSocket protocol instead. See the [WebSocket reference](/models/api-reference/text-to-speech/stream-speech-web-socket).
</Note>

## When to use this

- **Use this** when you want playback to start before synthesis is complete — long passages, latency-sensitive UI, live narration.
- **Use sync `/waves/v1/tts`** when total latency doesn't matter and you'd rather get one buffer.
- **Use `/waves/v1/tts/live`** (WebSocket) when the *text* arrives incrementally (LLM token stream). SSE assumes you have the full text up front.

## How it works

1. POST your text + voice settings — same payload as `/waves/v1/tts`, plus optional `model`.
2. The response is `Content-Type: text/event-stream`. Each chunk frame is `event: audio\n` followed by `data: {"audio": "<base64-pcm>"}\n\n`.
3. Decode each chunk's `audio` field with base64 and feed the PCM bytes to your audio pipeline (browser `MediaSource`, ffmpeg pipe, raw PCM player, etc.).
4. A final `data: {"done": true}\n\n` frame marks end of stream.

## Examples

**cURL**
```bash
curl -N -X POST "https://api.smallest.ai/waves/v1/tts/live" \
  -H "Authorization: Bearer $SMALLEST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Streaming this paragraph chunk by chunk so playback can start sooner.",
    "voice_id": "magnus",
    "sample_rate": 24000,
    "output_format": "pcm"
  }'
```

## Common gotchas

- **Use a streaming-friendly client.** `curl -N`, Python `iter_lines`, or a `fetch` `ReadableStream` reader. Buffering clients will hide the latency win.
- **Audio is base64 inside the event payload**, not the raw event bytes. Decode the `data.audio` field per event.
- **`output_format=pcm`** gives the lowest overhead for streaming playback. `wav`/`mp3` work but add per-chunk framing bytes.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.waves.synthesize_sse_tts(
    text="text",
    voice_id="voice_id",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request:** `TtsRequest` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.waves.<a href="src/smallestai/waves/client.py">list_voice_clones</a>() -> ListVoiceClonesWavesResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieve all voice clones in your organization.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.waves.list_voice_clones()
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.waves.<a href="src/smallestai/waves/client.py">create_voice_clone</a>(...) -> CreateVoiceCloneWavesResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Create an instant voice clone in a single call. Defaults to `lightning-v3.1`.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.waves.create_voice_clone(
    file="example_file",
    display_name="displayName",
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**display_name:** `str` — Human-readable name for the voice clone.
    
</dd>
</dl>

<dl>
<dd>

**file:** `core.File` 

Audio file to clone from. Supported MIME types:
`audio/mpeg`, `audio/mpeg-3`, `audio/wav`, `audio/wave`,
`audio/webm`, `video/webm`, `audio/mp4`, `video/mp4`.
Maximum size: 5 MB.
    
</dd>
</dl>

<dl>
<dd>

**description:** `typing.Optional[str]` — Optional longer description for the voice clone.
    
</dd>
</dl>

<dl>
<dd>

**accent:** `typing.Optional[str]` — Optional accent tag (e.g. "general", "indian").
    
</dd>
</dl>

<dl>
<dd>

**tags:** `typing.Optional[str]` 

Optional comma-separated list of tags. Server splits on
commas and trims whitespace (`"en, tone-test"` → `["en", "tone-test"]`).
    
</dd>
</dl>

<dl>
<dd>

**language:** `typing.Optional[str]` 

Primary language the clone will be used for. Optional, but
**strongly recommended** — set it to the language of your
reference audio. The TTS request's `language` should also
match this code; setting it now avoids silent language
mismatches at inference time.

Must be one of the languages supported by `lightning-v3.1`
(e.g. `en`, `hi`). The server validates and rejects
unsupported codes with a 400.
    
</dd>
</dl>

<dl>
<dd>

**model:** `typing.Optional[CreateVoiceCloneWavesRequestModel]` 

Voice cloning model. Defaults to `lightning-v3.1`.
`lightning-v2` is accepted by the schema for historical
reasons but is deprecated — the server returns 400 with
`"Voice cloning for lightning-v2 is deprecated. Please use lightning-v3.1"`.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Waves SpeechToText
<details><summary><code>client.waves.speech_to_text.<a href="src/smallestai/waves/speech_to_text/client.py">transcribe</a>(...) -> TranscribeResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Transcribe an audio file. The model is chosen via `?model=`:

- `?model=pulse-pro`: English-only, leaderboard-ranked accuracy. Raw bytes only; pass `webhook_url` to receive transcription asynchronously on long files.
- `?model=pulse`: multilingual transcription (21 streaming + 26 pre-recorded languages), supports both raw bytes and audio-by-URL.

## When to use this

Use this endpoint when you have a complete audio file (call recording, voicemail, podcast episode) and want the transcript back in one response. For live transcription as audio arrives, use the realtime WebSocket endpoint (`WS /waves/v1/stt/live`) instead.

Pulse Pro has no streaming worker today; calls to `WS /waves/v1/stt/live?model=pulse-pro` return `400` before the WebSocket upgrades.

## Input methods

- **Raw bytes**: `Content-Type: application/octet-stream` with the audio in the body. All knobs are query parameters.
- **URL (`?model=pulse` only)**: `Content-Type: application/json` with `{"url": "..."}` in the body.

## Examples

**cURL**: Pulse Pro, sync
```bash
curl -X POST "https://api.smallest.ai/waves/v1/stt/?model=pulse-pro&language=en&word_timestamps=true" \
  -H "Authorization: Bearer $SMALLEST_API_KEY" \
  -H "Content-Type: application/octet-stream" \
  --data-binary "@./call.wav"
```

**cURL**: Pulse Pro, async via webhook
```bash
curl -X POST "https://api.smallest.ai/waves/v1/stt/?model=pulse-pro&language=en&webhook_url=https://your.app/cb" \
  -H "Authorization: Bearer $SMALLEST_API_KEY" \
  -H "Content-Type: application/octet-stream" \
  --data-binary "@./call.wav"
```
Returns `200 { "status": "processing", "request_id": "..." }` immediately. The webhook receives the full transcription when ready.

**cURL**: Pulse, audio-by-URL
```bash
curl -X POST "https://api.smallest.ai/waves/v1/stt/?model=pulse&language=en" \
  -H "Authorization: Bearer $SMALLEST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://your-bucket.s3.amazonaws.com/call.wav"}'
```

**Python**
```python
import requests

with open("./call.wav", "rb") as f:
    audio = f.read()

r = requests.post(
    "https://api.smallest.ai/waves/v1/stt/",
    params={"model": "pulse-pro", "language": "en", "word_timestamps": "true"},
    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/octet-stream"},
    data=audio,
)
r.raise_for_status()
print(r.json()["transcription"])
```

**JavaScript / TypeScript**
```typescript
import { readFileSync } from "node:fs";

const audio = readFileSync("./call.wav");
const params = new URLSearchParams({ model: "pulse-pro", language: "en", word_timestamps: "true" });

const res = await fetch(`https://api.smallest.ai/waves/v1/stt/?${params}`, {
  method: "POST",
  headers: { Authorization: `Bearer ${process.env.SMALLEST_API_KEY}`, "Content-Type": "application/octet-stream" },
  body: audio,
});
console.log((await res.json()).transcription);
```

## Common gotchas

- **`model` is required.** Missing or invalid values return `400` with an enum-validation error.
- **Pulse Pro is English only.** Pass `language=en`. Other language codes are accepted at the wire level but produce unpredictable output.
- **Pulse Pro does not support audio-by-URL.** Send raw bytes or use `?model=pulse` for the URL flow.
- **Async (webhook) mode is Pulse Pro only.** Pulse runs sync only on this endpoint.
- **Max payload 250 MB.** Larger requests return `413`. Compress to mono 16 kHz PCM if you are close to the limit; quality is unaffected.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
client.waves.speech_to_text.transcribe(...)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**model:** `TranscribeRequestModel` 

Selects which ASR model handles the request. Required; missing or invalid values return `400`.

- `pulse-pro`: English only, leaderboard-ranked accuracy, raw bytes only; supports async via `webhook_url`.
- `pulse`: multilingual (39 languages), raw bytes OR URL.
    
</dd>
</dl>

<dl>
<dd>

**language:** `TranscribeRequestLanguage` 

Language of the audio file. This endpoint is **Pre-Recorded (HTTP)** — for streaming, switch to `WSS /waves/v1/stt/live` (different supported language set).

**26 single-language codes:** `en`, `hi`, `de`, `es`, `ru`, `it`, `fr`, `nl`, `pt`, `uk`, `pl`, `cs`, `sk`, `lv`, `et`, `ro`, `fi`, `sv`, `bg`, `hu`, `da`, `lt`, `mt`, `zh`, `ja`, `ko`.

**Regional auto-detect aggregators** for unknown audio:
- `multi-eu` — auto-detects across all 21 European codes plus `en`.
- `multi-asian` — auto-detects across `zh`, `ko`, `ja`, `en`.
- `multi-indic`: auto-detects across `en`, `hi`, `gu`, `mr`, `bn`, `or`. India region only.

- **Pulse Pro**: pass `en`.
- **Pulse**: pass any of the single-language codes above, or use the `multi-eu` / `multi-asian` / `multi-indic` aggregator for unknown audio. See the [Pulse model card](/models/model-cards/speech-to-text/pulse) for the full table with language names.
    
</dd>
</dl>

<dl>
<dd>

**request:** `typing.Union[bytes, typing.Iterator[bytes], typing.AsyncIterator[bytes]]` 
    
</dd>
</dl>

<dl>
<dd>

**word_timestamps:** `typing.Optional[bool]` — Include the per-word `words[]` array in the response — each entry carries the recognized `word`, its `start`/`end` timestamps, and a per-word `confidence` score (0.0–1.0). With `diarize=true`, entries also include `speaker`. On Pulse Pro this costs roughly one-third of throughput.
    
</dd>
</dl>

<dl>
<dd>

**diarize:** `typing.Optional[bool]` — Multi-speaker identification; adds per-word and per-utterance speaker labels.
    
</dd>
</dl>

<dl>
<dd>

**webhook_url:** `typing.Optional[str]` — Pulse Pro only. If set, the response is `200` with `{"status": "processing", "request_id": "..."}` immediately, and the full transcription is delivered to this URL when ready. Use for long files where you do not want to hold an HTTP connection open.
    
</dd>
</dl>

<dl>
<dd>

**webhook_method:** `typing.Optional[TranscribeRequestWebhookMethod]` — HTTP method to use when calling the webhook. Pulse Pro only.
    
</dd>
</dl>

<dl>
<dd>

**webhook_extra:** `typing.Optional[str]` — Arbitrary metadata returned to the webhook in addition to the transcription payload. Pulse Pro only.
    
</dd>
</dl>

<dl>
<dd>

**redact_pii:** `typing.Optional[TranscribeRequestRedactPii]` 

Redact personally identifiable information from the transcript.
Names → `[FIRSTNAME_*]` / `[LASTNAME_*]`, phone numbers →
`[PHONENUMBER_*]`, addresses → `[ADDRESS_*]`, etc. The redaction
tokens use sequential indices so multiple occurrences of the same
entity get distinct labels (`[FIRSTNAME_1]`, `[FIRSTNAME_2]`).

**Language support:** currently effective only on `en` and `hi`.
Setting `redact_pii=true` on other language codes is accepted
but does not redact.
    
</dd>
</dl>

<dl>
<dd>

**redact_pci:** `typing.Optional[TranscribeRequestRedactPci]` 

Redact payment card information (credit-card numbers, CVV, account
numbers, etc.). Replaces matches with `[ACCOUNTNUMBER_*]` tokens.
Use alongside `redact_pii=true` for full PCI-compliant transcript
handling.

**Language support:** currently effective only on `en` and `hi`.
Setting `redact_pci=true` on other language codes is accepted
but does not redact.
    
</dd>
</dl>

<dl>
<dd>

**emotion_detection:** `typing.Optional[TranscribeRequestEmotionDetection]` 

When `true`, the response adds an `emotions` object mapping detected
emotion labels to confidence scores. Useful for voice-of-customer
analytics on call recordings.
    
</dd>
</dl>

<dl>
<dd>

**gender_detection:** `typing.Optional[TranscribeRequestGenderDetection]` 

When `true`, the response adds a `gender` field with the detected
speaker gender label. Pulse pre-recorded only.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Waves Electron
<details><summary><code>client.waves.electron.<a href="src/smallestai/waves/electron/client.py">complete</a>(...) -> ChatCompletion</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Generate a chat completion with Electron. OpenAI-compatible
request/response shape — point any OpenAI SDK at
`https://api.smallest.ai/waves/v1` and it just works.

Set `stream: true` to receive tokens via Server-Sent Events. With
`stream_options: { include_usage: true }`, the final SSE chunk
carries the `usage` block so token accounting is exact even on
client disconnects.

Tool calling follows OpenAI's `tools` array convention. When you
provide a voice-agent-style system prompt, Electron emits a short
filler phrase in the assistant message `content` field alongside
`tool_calls` — see the [Tool Calling guide](/models/documentation/llm-electron/tool-function-calling)
for the voice-agent pattern.

## Examples

**cURL**
```bash
curl -X POST "https://api.smallest.ai/waves/v1/chat/completions" \
  -H "Authorization: Bearer $SMALLEST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "electron",
    "messages": [
      {"role": "user", "content": "Write one sentence about why the sky is blue."}
    ]
  }'
```

**Python** (`pip install openai`)
```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://api.smallest.ai/waves/v1",
    api_key=os.environ["SMALLEST_API_KEY"],
)

response = client.chat.completions.create(
    model="electron",
    messages=[{"role": "user", "content": "Write one sentence about why the sky is blue."}],
)

print(response.choices[0].message.content)
```

**JavaScript / TypeScript** (`npm install openai`)
```typescript
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "https://api.smallest.ai/waves/v1",
  apiKey: process.env.SMALLEST_API_KEY,
});

const response = await client.chat.completions.create({
  model: "electron",
  messages: [
    { role: "user", content: "Write one sentence about why the sky is blue." },
  ],
});

console.log(response.choices[0].message.content);
```

**Streaming with usage** (Python)
```python
stream = client.chat.completions.create(
    model="electron",
    messages=[{"role": "user", "content": "Tell me a one-sentence fun fact."}],
    stream=True,
    stream_options={"include_usage": True},
)
for chunk in stream:
    if chunk.choices and chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
    if chunk.usage:
        print(f"\n\nTokens: {chunk.usage.total_tokens}")
```

## Common gotchas

- **Base URL is `/waves/v1`**, not `/v1`. The OpenAI SDK appends `/chat/completions` for you.
- **`stream_options.include_usage: true`** is required for exact token accounting on streaming calls — the final SSE chunk carries the `usage` block.
- **`n > 1` and `prompt_logprobs` are rejected.** Use multiple requests if you need parallel completions.
- **Auth header is `Authorization: Bearer $SMALLEST_API_KEY`** — get the key from the [Smallest AI Console](https://app.smallest.ai/dashboard/api-keys).
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment
from smallestai.waves import ElectronMessage

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.waves.electron.complete(
    model="electron",
    messages=[
        ElectronMessage(
            role="user",
            content="Hello!",
        )
    ],
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**model:** `str` — Model ID. Currently only `"electron"`.
    
</dd>
</dl>

<dl>
<dd>

**messages:** `typing.List[ElectronMessage]` — Chat history. Standard OpenAI message array.
    
</dd>
</dl>

<dl>
<dd>

**temperature:** `typing.Optional[float]` — Sampling temperature.
    
</dd>
</dl>

<dl>
<dd>

**top_p:** `typing.Optional[float]` — Nucleus sampling.
    
</dd>
</dl>

<dl>
<dd>

**max_tokens:** `typing.Optional[int]` 

Maximum output tokens. Combined input + output context ceiling
is 32,768.
    
</dd>
</dl>

<dl>
<dd>

**stream:** `typing.Optional[bool]` 

When true, response is `text/event-stream`. See the
[Streaming guide](/models/documentation/llm-electron/streaming).
    
</dd>
</dl>

<dl>
<dd>

**stream_options:** `typing.Optional[ChatCompletionRequestStreamOptions]` 
    
</dd>
</dl>

<dl>
<dd>

**tools:** `typing.Optional[typing.List[typing.Dict[str, typing.Any]]]` 

Tool / function calling definitions. Forwarded verbatim to the
OpenAI-compatible upstream, so the standard OpenAI shape
(`{type: "function", function: {name, description, parameters}}`)
is the recommended form and is what the examples below use.
The wire schema is permissive (`array<object>`) — any tools payload
the upstream accepts will work. See [Tool Calling](/models/documentation/llm-electron/tool-function-calling)
for details.
    
</dd>
</dl>

<dl>
<dd>

**tool_choice:** `typing.Optional[ChatCompletionRequestToolChoice]` 
    
</dd>
</dl>

<dl>
<dd>

**response_format:** `typing.Optional[ChatCompletionRequestResponseFormat]` — Output shape. `{type: "text"}` (default) or `{type: "json_object"}`.
    
</dd>
</dl>

<dl>
<dd>

**stop:** `typing.Optional[ChatCompletionRequestStop]` 
    
</dd>
</dl>

<dl>
<dd>

**seed:** `typing.Optional[int]` — Best-effort determinism.
    
</dd>
</dl>

<dl>
<dd>

**logit_bias:** `typing.Optional[typing.Dict[str, float]]` 
    
</dd>
</dl>

<dl>
<dd>

**logprobs:** `typing.Optional[bool]` 
    
</dd>
</dl>

<dl>
<dd>

**top_logprobs:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**presence_penalty:** `typing.Optional[float]` 
    
</dd>
</dl>

<dl>
<dd>

**frequency_penalty:** `typing.Optional[float]` 
    
</dd>
</dl>

<dl>
<dd>

**user:** `typing.Optional[str]` — Opaque end-user identifier. Not interpreted by Electron.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

