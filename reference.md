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

<details><summary><code>client.atoms.user.<a href="src/smallestai/atoms/user/client.py">get_subscription</a>() -> GetSubscriptionUserResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns the caller's subscription details (plan ID + plan-tier limits) and
feature-flag map. Useful for client-side gating of paid features.

**`limits` is omitted** for the `ENTERPRISE` plan (and for unknown plan IDs) —
only `features` is returned in those cases.
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

client.atoms.user.get_subscription()

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

<details><summary><code>client.atoms.organization.<a href="src/smallestai/atoms/organization/client.py">get_account_details</a>() -> GetAccountDetailsOrganizationResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns the authenticated user's profile and the organizations they belong to.

**Response envelope is non-standard** — this endpoint returns the account object
directly (no `{status, data}` wrapper).
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

client.atoms.organization.get_account_details()

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

<details><summary><code>client.atoms.organization.<a href="src/smallestai/atoms/organization/client.py">update_name</a>(...) -> UpdateNameOrganizationResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Update the display name of the caller's current organization. Requires admin role.

**Response envelope is non-standard** — returns `{success: true, name}` instead
of the usual `{status, data}` wrapper.
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

client.atoms.organization.update_name(
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

**name:** `str` — New organization name (trimmed).
    
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

## Atoms Agents
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

Synthesizer (TTS) configuration for the agent.
Models `waves`, `waves_lightning_large`, `waves_lightning_v2`, and `waves_lightning_v3_1`
validate `voiceId` against the Waves API. All other models accept any voiceId.
Cloned voices are regular voiceIds — use them with any compatible Waves model.
    
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

**400 is also returned when:**
- The agent is locked (`"Agent is locked, please unlock it to update"`)
- Cross-field constraint violated (e.g. `north_indic` language requires `transcriberType: pulse`)

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

<details><summary><code>client.atoms.agents.<a href="src/smallestai/atoms/agents/client.py">get_agent_workflow</a>(...) -> GetAgentIdWorkflowResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

**Deprecated** — prefer `GET /agent/{id}` (config is resolved into `_resolvedConfig`
including prompt, tools, and post-call analytics).

Returns the active version's prompt and tools for single-prompt agents, or the
workflow graph data for workflow_graph agents. Customers still rely on this to
fetch their current prompt + tools — endpoint is kept live for now.

**Caveat:** the `versionId` query param (if passed) is silently ignored.
The response always reflects the currently-active version. To inspect a
non-active version, use `GET /agent/{id}/versions/{versionId}`.
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

client.atoms.agents.get_agent_workflow(
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

**id:** `str` — The ID of the agent
    
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

<details><summary><code>client.atoms.agents.<a href="src/smallestai/atoms/agents/client.py">update_workflow_configuration</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

**Deprecated** — use `PATCH /agent/{id}/drafts/{draftId}/config` instead.

Directly mutates the legacy workflow document for an agent. This write path
bypasses the versioning system entirely: the change is not captured as a
new version, and future version activations may overwrite the legacy doc
back to whatever the version snapshot contains.

⚠ **Writing here on a versioned agent can silently wipe tools, prompt, or
other fields that were missing from the PATCH payload.** Only use this if
you know the agent is not using versioning, or if you are intentionally
hot-patching the legacy doc.
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

client.atoms.agents.update_workflow_configuration(
    id="60d0fe4f5311236168a109ca",
    type="workflow_graph",
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

**id:** `str` — The workflow ID (found at `agent.workflowId` on the agent document).
    
</dd>
</dl>

<dl>
<dd>

**type:** `WorkflowType` 
    
</dd>
</dl>

<dl>
<dd>

**workflow_graph:** `typing.Optional[UpdateWorkflowConfigurationAgentsRequestWorkflowGraph]` — Required when `type = workflow_graph`. Exactly one of `workflowGraph` or `singlePromptConfig` must be provided.
    
</dd>
</dl>

<dl>
<dd>

**single_prompt_config:** `typing.Optional[SinglePromptConfig]` 
    
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

<details><summary><code>client.atoms.agents.<a href="src/smallestai/atoms/agents/client.py">create_with_ai</a>(...) -> CreateWithAiAgentsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Create a new single-prompt agent from a natural-language brief or structured
question/answer pairs. Atoms generates the system prompt for you.

Provide either `description` (free-form brief) or a non-empty `questions` array,
but not both. The `emotiveToggle`, `voiceId`, and `voiceModel` fields must be
supplied as a 3-tuple or omitted entirely.
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

client.atoms.agents.create_with_ai()

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

**name:** `typing.Optional[str]` — Agent name (trimmed). Auto-generated when omitted.
    
</dd>
</dl>

<dl>
<dd>

**description:** `typing.Optional[str]` 

Free-form natural-language description of what the agent should do.
Atoms turns this into the system prompt. Use this OR `questions`, not both.
    
</dd>
</dl>

<dl>
<dd>

**questions:** `typing.Optional[typing.List[CreateWithAiAgentsRequestQuestionsItem]]` 

Structured question/answer pairs. Atoms uses these to compose the
system prompt. Use this OR `description`, not both.
    
</dd>
</dl>

<dl>
<dd>

**type:** `typing.Optional[CreateWithAiAgentsRequestType]` — Currently the only supported agent type.
    
</dd>
</dl>

<dl>
<dd>

**emotive_toggle:** `typing.Optional[bool]` — Enable emotive synthesis. Must be paired with `voiceId` + `voiceModel`.
    
</dd>
</dl>

<dl>
<dd>

**voice_id:** `typing.Optional[str]` — Voice ID for synthesis. Must be paired with `emotiveToggle` + `voiceModel`.
    
</dd>
</dl>

<dl>
<dd>

**voice_model:** `typing.Optional[CreateWithAiAgentsRequestVoiceModel]` — Synthesizer to use. Must be paired with `emotiveToggle` + `voiceId`.
    
</dd>
</dl>

<dl>
<dd>

**knowledge_base_id:** `typing.Optional[str]` — Optional knowledge-base ID to attach to the new agent.
    
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

<details><summary><code>client.atoms.agents.<a href="src/smallestai/atoms/agents/client.py">list_call_logs</a>(...) -> ListCallLogsAgentsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns paginated conversation logs (calls) for a specific agent in the caller's
organization. Use `GET /conversation` for cross-agent log listing; use this when
you already have an agent ID.
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

client.atoms.agents.list_call_logs(
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

**id:** `str` — The agent ID
    
</dd>
</dl>

<dl>
<dd>

**page:** `typing.Optional[str]` — Page number (string-encoded positive integer).
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[str]` — Page size (string-encoded positive integer).
    
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

<details><summary><code>client.atoms.agents.<a href="src/smallestai/atoms/agents/client.py">get_widget_config</a>(...) -> GetWidgetConfigAgentsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns the embeddable web widget configuration for the agent (theme, copy,
consent prompts, branding, voice/chat mode, allowlist). The response merges the
stored config with `assistantId: <agentId>` injected.
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

client.atoms.agents.get_widget_config(
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

**id:** `str` — The agent ID
    
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

<details><summary><code>client.atoms.agents.<a href="src/smallestai/atoms/agents/client.py">update_widget_config</a>(...) -> UpdateWidgetConfigAgentsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Merge updates into the agent's embeddable widget config. Only the fields in the
request body are overwritten; everything else is preserved. Returns the full
widget config after merge.
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
from smallestai.atoms import WidgetConfig

client = SmallestAI(
    api_key="<token>",
    environment=SmallestAIEnvironment.PRODUCTION,
)

client.atoms.agents.update_widget_config(
    id="60d0fe4f5311236168a109ca",
    widget_config=WidgetConfig(),
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

**id:** `str` — The agent ID
    
</dd>
</dl>

<dl>
<dd>

**widget_config:** `WidgetConfig` 
    
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

<details><summary><code>client.atoms.agents.<a href="src/smallestai/atoms/agents/client.py">get_prompt_config</a>() -> GetPromptConfigAgentsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns the canonical question definitions, option choices, and example labels
used by the agent-builder UI when collecting input for `POST /agent/with-ai`.

Use this to programmatically discover what questions to ask end-users when
building agent-creation UIs.
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

client.atoms.agents.get_prompt_config()

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
    call_ids=[
        "CALL-1737000000000-abc123",
        "CALL-1737000000001-def456"
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

<details><summary><code>client.atoms.campaigns.<a href="src/smallestai/atoms/campaigns/client.py">export_logs</a>(...) -> typing.List[ExportLogsCampaignsResponseItem]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Streams a JSON file containing every call log for a campaign.

Response is a **file download** (`Content-Disposition: attachment`), not the
standard `{status, data}` envelope. Body is a raw JSON array of log objects.
When the relay-service is configured and reachable, each row also includes an
`events` array; otherwise the field is omitted.
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

client.atoms.campaigns.export_logs(
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

**id:** `str` — Campaign ID.
    
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
    urls=[
        "https://example.com/pricing",
        "https://example.com/faq"
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
    sip_termination_url="sip:trunk.your-provider.com",
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

**sip_termination_url:** `str` — The SIP URI where calls should be routed to your infrastructure
    
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
    event_types=[
        "pre-conversation"
    ],
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
    members=[
        {
            "phoneNumber": "+1234567890",
            "name": "John Doe",
            "email": "john@example.com"
        }
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
    member_ids=[
        "60d0fe4f5311236168a109cd"
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

**id:** `str` — The agent ID
    
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

**id:** `str` — The agent ID
    
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
    id="60d0fe4f5311236168a109ca",
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

**id:** `str` — The agent ID
    
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
    id="60d0fe4f5311236168a109ca",
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

**id:** `str` — The agent ID
    
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
    id="60d0fe4f5311236168a109ca",
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

**id:** `str` — The agent ID
    
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
    id="60d0fe4f5311236168a109ca",
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

**id:** `str` — The agent ID
    
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
    id="60d0fe4f5311236168a109ca",
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

**id:** `str` — The agent ID
    
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
    id="60d0fe4f5311236168a109ca",
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

**id:** `str` — The agent ID
    
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
    id="60d0fe4f5311236168a109ca",
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

**id:** `str` — The agent ID
    
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

**id:** `str` — The agent ID
    
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
    id="60d0fe4f5311236168a109ca",
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

**id:** `str` — The agent ID
    
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

<details><summary><code>client.atoms.agent_versioning_versions.<a href="src/smallestai/atoms/agent_versioning_versions/client.py">compare_version_metrics</a>(...) -> CompareVersionMetricsAgentVersioningVersionsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Compare analytics/call metrics between two published versions over an optional date range.
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

client.atoms.agent_versioning_versions.compare_version_metrics(
    id="60d0fe4f5311236168a109ca",
    version_a="versionA",
    version_b="versionB",
    date_from=datetime.date.fromisoformat("2026-05-01"),
    date_to=datetime.date.fromisoformat("2026-05-31"),
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

**id:** `str` — The agent ID
    
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

**date_from:** `typing.Optional[datetime.date]` — Start date for the comparison range in YYYY-MM-DD format.
    
</dd>
</dl>

<dl>
<dd>

**date_to:** `typing.Optional[datetime.date]` — End date for the comparison range in YYYY-MM-DD format.
    
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
    id="60d0fe4f5311236168a109ca",
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

**id:** `str` — The agent ID
    
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
    id="60d0fe4f5311236168a109ca",
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

**id:** `str` — The agent ID
    
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
    id="60d0fe4f5311236168a109ca",
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

**id:** `str` — The agent ID
    
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
    id="60d0fe4f5311236168a109ca",
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

**id:** `str` — The agent ID
    
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

<details><summary><code>client.waves.<a href="src/smallestai/waves/client.py">synthesize_lightning</a>(...) -> typing.Iterator[bytes]</code></summary>
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

client.waves.synthesize_lightning(
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

**text:** `str` — The text to convert to speech.
    
</dd>
</dl>

<dl>
<dd>

**voice_id:** `str` — The voice identifier to use for speech generation.
    
</dd>
</dl>

<dl>
<dd>

**sample_rate:** `typing.Optional[int]` — The sample rate for the generated audio.
    
</dd>
</dl>

<dl>
<dd>

**speed:** `typing.Optional[float]` — The speed of the generated speech.
    
</dd>
</dl>

<dl>
<dd>

**language:** `typing.Optional[LightningRequestLanguage]` — Determines how numbers are spelled out. If set to 'en', numbers will be read as individual digits in English. If set to 'hi', numbers will be read as individual digits in Hindi.
    
</dd>
</dl>

<dl>
<dd>

**output_format:** `typing.Optional[LightningRequestOutputFormat]` — The format of the output audio.
    
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

<details><summary><code>client.waves.<a href="src/smallestai/waves/client.py">synthesize_lightning_large</a>(...) -> typing.Iterator[bytes]</code></summary>
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

client.waves.synthesize_lightning_large(
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

**request:** `LightningLargeRequest` 
    
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

<details><summary><code>client.waves.<a href="src/smallestai/waves/client.py">synthesize_lightning_v2</a>(...) -> typing.Iterator[bytes]</code></summary>
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

client.waves.synthesize_lightning_v2(
    text="Hey i am your a text to speech model",
    voice_id="malcom",
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

**request:** `Lightningv2Request` 
    
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

<details><summary><code>client.waves.<a href="src/smallestai/waves/client.py">synthesize_sse_lightning_large</a>(...) -> typing.Iterator[bytes]</code></summary>
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

client.waves.synthesize_sse_lightning_large(
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

**request:** `LightningLargeRequest` 
    
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

<details><summary><code>client.waves.<a href="src/smallestai/waves/client.py">synthesize_sse_lightning_v2</a>(...) -> typing.Iterator[bytes]</code></summary>
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

client.waves.synthesize_sse_lightning_v2(
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

**request:** `Lightningv2Request` 
    
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

List voices available for Lightning v3.1. The response is the union of the standard and Pro voice catalogs — the API does not return a per-voice "is Pro" flag, so consult the [Lightning v3.1 Pro](/waves/model-cards/text-to-speech/lightning-v-3-1-pro) and [Lightning v3.1](/waves/model-cards/text-to-speech/lightning-v-3-1) model cards for the canonical per-pool voice lists. Use the `voice_id` from this response together with `"model": "lightning_v3.1"` (default) or `"model": "lightning_v3.1_pro"` on the unified `/waves/v1/tts` route to pick the pool.
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

<details><summary><code>client.waves.<a href="src/smallestai/waves/client.py">add_voice</a>(...) -> AddVoiceWavesResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

**Deprecated** — use `POST /waves/v1/voice-cloning` instead. The new
endpoint defaults to `lightning-v3.1`, supports optional metadata,
and returns pre-generated sample clips. This endpoint only clones
onto `lightning-large` and the resulting voices do not work on
`lightning-v3.1` (returns an empty WAV). Kept live for backward
compatibility; new integrations should migrate.
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

client.waves.add_voice(
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

**display_name:** `str` — Display name for the voice clone.
    
</dd>
</dl>

<dl>
<dd>

**file:** `core.File` — Audio file to create voice clone from.
    
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

<details><summary><code>client.waves.<a href="src/smallestai/waves/client.py">get_cloned_voices</a>() -> GetClonedVoicesWavesResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

**Deprecated** — use `GET /waves/v1/voice-cloning` instead. The new
list endpoint returns the same data plus a `modelIds` array per
clone. Kept live for backward compatibility.
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

client.waves.get_cloned_voices()

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

<details><summary><code>client.waves.<a href="src/smallestai/waves/client.py">delete_voice</a>(...) -> DeleteVoiceWavesResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Delete a voice clone by `voiceId`. Despite the `/lightning-large/`
path, this endpoint deletes any voice clone on the organization,
including clones created via `POST /waves/v1/voice-cloning`.
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

client.waves.delete_voice(
    voice_id="voiceId",
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

**voice_id:** `str` — The unique identifier of the voice clone to delete.
    
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

**Language behaviour on `lightning_v3.1_pro`:** pass `language: en` for UK + American accented English, pass `language: hi` for Indian accented English + Hindi (code-switching), or omit `language` to default to `en + hi` (mixed Indian + Western English coverage). On `lightning_v3.1` the full 12-language catalog applies (see voice catalog).

## When to use this

- **Use this** for short utterances you can render before playback (notifications, prompts, batch jobs, audio file generation).
- **Use `/waves/v1/tts/live`** when you want playback to start before the full audio is ready (long passages, latency-sensitive apps).
- **Use `/waves/v1/tts/live`** (WebSocket) when text arrives incrementally (LLM token streams, live captioning).

## Key features

- 44 kHz natural, expressive synthesis
- Model selectable per request via `model` body parameter
- Cloned voice IDs (`voice_*`) work on `lightning_v3.1` — same param as catalog voices
- 12 documented languages on `lightning_v3.1`. On `lightning_v3.1_pro`: `language: en` → UK + American accented English; `language: hi` → Indian accented English + Hindi; omit `language` → defaults to `en + hi`.
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
  **The same URL serves the WebSocket endpoint.** `wss://api.smallest.ai/waves/v1/tts/live` accepts a WebSocket upgrade for streaming-text scenarios (LLM token streams, live captioning). The HTTP `POST` documented on this page returns SSE; use `wss://` to use the WebSocket protocol instead. See the [WebSocket reference](/waves/api-reference/api-reference/text-to-speech/tts).
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

<details><summary><code>client.waves.<a href="src/smallestai/waves/client.py">synthesize_lightning_v31</a>(...) -> typing.Iterator[bytes]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

<Warning>**Endpoint scheduled for retirement.** This URL will stop accepting requests **60 days from the Lightning v3.1 Pro launch (2026-05-15)** — i.e. on **2026-07-14**. The Lightning v3.1 model itself is current and stays. Migrate to [`POST /waves/v1/tts`](/waves/api-reference/api-reference/text-to-speech/synthesize-speech) and select Lightning v3.1 via the `model` body field (default).</Warning>

Synthesize speech from text in a single request. The simplest way to get audio when you have the full text up front — pass `text` + `voice_id`, get back binary audio.

## When to use this

- **Use this** for short utterances you can render before playback (notifications, prompts, batch jobs, audio file generation).
- **Use the SSE streaming endpoint** when you want playback to start before the full audio is ready (long passages, latency-sensitive apps).
- **Use the WebSocket endpoint** when text arrives incrementally (LLM token streams, live captioning).

## Key features

- 44 kHz natural, expressive synthesis
- Cloned voice IDs (`voice_*`) work — same param as catalog voices
- 12 documented languages — see the model card for the full list
- Output formats: `pcm`, `mp3`, `wav`, `ulaw`, `alaw`
- Sample rates: 8 kHz – 44.1 kHz
- Speed: 0.5× – 2×
- Per-call pronunciation dictionaries via `pronunciation_dicts`

## Examples

**cURL**
```bash
curl -X POST "https://api.smallest.ai/waves/v1/lightning-v3.1/get_speech" \
  -H "Authorization: Bearer $SMALLEST_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept: audio/wav" \
  -d '{
    "text": "Hello from Lightning v3.1.",
    "voice_id": "magnus",
    "sample_rate": 24000,
    "output_format": "wav"
  }' --output speech.wav
```

**Python** (`pip install smallestai>=4.4.0`)
```python
from smallestai import SmallestAI

client = SmallestAI(api_key="YOUR_API_KEY")

with open("speech.wav", "wb") as f:
    for chunk in client.waves.synthesize_lightning_v3_1(
        text="Hello from Lightning v3.1.",
        voice_id="magnus",
        sample_rate=24000,
        output_format="wav",
        # Optional: cloned voice support
        # voice_id="voice_FlPKRWI7DX",
        # Optional: pin pronunciations for specific words
        # pronunciation_dicts=["<your dict id>"],
    ):
        f.write(chunk)
```

**JavaScript / TypeScript** (using `fetch`)
```typescript
const res = await fetch("https://api.smallest.ai/waves/v1/lightning-v3.1/get_speech", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${process.env.SMALLEST_API_KEY}`,
    "Content-Type": "application/json",
    Accept: "audio/wav",
  },
  body: JSON.stringify({
    text: "Hello from Lightning v3.1.",
    voice_id: "magnus",
    sample_rate: 24000,
    output_format: "wav",
  }),
});
const audio = Buffer.from(await res.arrayBuffer());
require("node:fs").writeFileSync("speech.wav", audio);
```

## Common gotchas

- **Set `Accept: audio/wav`.** Omitting it can return an empty or unplayable response.
- **Cloned voices** (`voice_*` from `add_voice`) work on this endpoint and support `pronunciation_dicts`.
- **`pronunciation_dicts` validates IDs at request time.** Passing an unknown ID returns `Invalid input data` — create the dict first via the pronunciation-dicts endpoint and save the returned `id`.
- **Pronunciation matching is case-sensitive.** Add both `Synopsis` and `synopsis` if your text uses both casings.
- **44.1 kHz output** is supported but most playback environments are happy with 24 kHz — drop the sample rate if bandwidth matters.
- **JavaScript / TypeScript**: the official `smallestai` npm package predates Lightning v3.1, so call this endpoint with `fetch` or `axios` as shown above.
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

client.waves.synthesize_lightning_v31(
    text="Hey i am your a text to speech model",
    voice_id="daniel",
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

**request:** `LightningV31Request` 
    
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

<details><summary><code>client.waves.<a href="src/smallestai/waves/client.py">synthesize_sse_lightning_v31</a>(...) -> typing.Iterator[bytes]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

<Warning>**Endpoint scheduled for retirement.** This URL will stop accepting requests **60 days from the Lightning v3.1 Pro launch (2026-05-15)** — i.e. on **2026-07-14**. The Lightning v3.1 model itself is current and stays. Migrate to [`POST /waves/v1/tts/live`](/waves/api-reference/api-reference/text-to-speech/synthesize-speech-sse) and select Lightning v3.1 via the `model` body field (default).</Warning>

Synthesize speech and stream the audio back over Server-Sent Events. The body and parameters are identical to the sync `/get_speech` endpoint — the difference is the response is a stream of base64-encoded PCM chunks instead of one binary blob.

## When to use this

- **Use this** when you want playback to start before synthesis is complete — long passages, latency-sensitive UI, live narration.
- **Use sync `/get_speech`** when total latency doesn't matter and you'd rather get one buffer.
- **Use the WebSocket endpoint** when the *text* arrives incrementally (LLM token stream). SSE assumes you have the full text up front.

## How it works

1. POST your text + voice settings — same payload as `/get_speech`.
2. The response is `Content-Type: text/event-stream`. Each chunk frame is `event: audio\n` followed by `data: {"audio": "<base64-pcm>"}\n\n`.
3. Decode each chunk's `audio` field with base64 and feed the PCM bytes to your audio pipeline (browser `MediaSource`, ffmpeg pipe, raw PCM player, etc.).
4. A final `data: {"done": true}\n\n` frame marks end of stream.

## Examples

**cURL**
```bash
curl -N -X POST "https://api.smallest.ai/waves/v1/lightning-v3.1/stream" \
  -H "Authorization: Bearer $SMALLEST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Streaming this paragraph chunk by chunk so playback can start sooner.",
    "voice_id": "magnus",
    "sample_rate": 24000,
    "output_format": "pcm"
  }'
```

**Python** (`pip install smallestai>=4.4.0`)
```python
import base64
from smallestai import SmallestAI

client = SmallestAI(api_key="YOUR_API_KEY")

with open("stream.pcm", "wb") as f:
    for chunk in client.waves.synthesize_sse_lightning_v3_1(
        text="Streaming this paragraph chunk by chunk so playback can start sooner.",
        voice_id="magnus",
        sample_rate=24000,
        output_format="pcm",
    ):
        # Each chunk is `{"audio": "<base64-encoded PCM>"}`.
        # Decode and pipe to your audio pipeline.
        if chunk.get("audio"):
            f.write(base64.b64decode(chunk["audio"]))
```

**JavaScript / TypeScript** (using `fetch` + a reader)
```typescript
const res = await fetch("https://api.smallest.ai/waves/v1/lightning-v3.1/stream", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${process.env.SMALLEST_API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    text: "Streaming this paragraph chunk by chunk so playback can start sooner.",
    voice_id: "magnus",
    sample_rate: 24000,
    output_format: "pcm",
  }),
});

const reader = res.body!.getReader();
const decoder = new TextDecoder();
let buf = "";
let finished = false;
while (!finished) {
  const { value, done } = await reader.read();
  if (done) break;
  buf += decoder.decode(value);
  const events = buf.split("\n\n");
  buf = events.pop() ?? "";
  for (const ev of events) {
    // SSE frames are "event: audio\ndata: {json}" or just "data: {json}".
    // We only care about the data line — pull it out and parse.
    const dataLine = ev.split("\n").find((l) => l.startsWith("data:"));
    if (!dataLine) continue;
    const payload = JSON.parse(dataLine.slice(5).trim());
    if (payload.done) { finished = true; break; }
    if (payload.audio) {
      const pcm = Buffer.from(payload.audio, "base64");
      // … hand pcm to your audio pipeline
    }
  }
}
```

## Common gotchas

- **Use a streaming-friendly client.** `curl -N`, Python `iter_lines`, or a `fetch` `ReadableStream` reader. Buffering clients will hide the latency win.
- **Audio is base64 inside the event payload**, not the raw event bytes. Decode the `data.audio` field per event.
- **`output_format=pcm`** gives the lowest overhead for streaming playback. `wav`/`mp3` work but add per-chunk framing bytes.
- **First-chunk latency** depends on model warm-up + network distance. Use `output_format=pcm` and a streaming-friendly client to minimize what you can control.
- **JavaScript / TypeScript**: the official `smallestai` npm package predates Lightning v3.1, so call this endpoint with `fetch` as shown above.
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

client.waves.synthesize_sse_lightning_v31(
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

**request:** `LightningV31Request` 
    
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

<details><summary><code>client.waves.<a href="src/smallestai/waves/client.py">transcribe_pulse</a>(...) -> TranscribePulseWavesResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Transcribe an audio file to text using the Pulse model. The fastest way to get a transcript when you already have a recording — pass either the raw bytes or a URL.

## When to use this

Use this endpoint when you have a complete audio file (call recording, voicemail, podcast episode) and want the transcript back in one response. For live transcription as audio arrives, use the realtime WebSocket endpoint (`WSS /waves/v1/pulse/get_text`) instead.

## Input methods

Send the audio in one of two ways:

1. **Raw bytes** — `Content-Type: application/octet-stream` with the audio in the body. All knobs (`language`, `word_timestamps`, etc.) are query parameters.
2. **URL** — `Content-Type: application/json` with `{"url": "..."}` in the body. Useful when the audio already lives in object storage. Same query parameters apply.

Pulse autodetects the language across 30+ supported locales. Pass `language` explicitly when you already know it — detection is fast but skipping it is faster.

## Examples

**cURL** (raw bytes)
```bash
curl -X POST "https://api.smallest.ai/waves/v1/pulse/get_text?language=en&word_timestamps=true" \
  -H "Authorization: Bearer $SMALLEST_API_KEY" \
  -H "Content-Type: application/octet-stream" \
  --data-binary "@./call.wav"
```

**cURL** (URL)
```bash
curl -X POST "https://api.smallest.ai/waves/v1/pulse/get_text?language=en" \
  -H "Authorization: Bearer $SMALLEST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://your-bucket.s3.amazonaws.com/call.wav"}'
```

**Python** (`pip install smallestai>=4.4.0`)
```python
from smallestai import SmallestAI

client = SmallestAI(api_key="YOUR_API_KEY")
with open("./call.wav", "rb") as f:
    result = client.waves.transcribe_pulse(
        request=f.read(),
        language="en",
        word_timestamps=True,
        diarize=True,
    )
print(result.status)         # "success"
print(result.transcription)  # the transcript string
```

**JavaScript / TypeScript** (using `fetch`)
```typescript
import { readFileSync } from "node:fs";

const audio = readFileSync("./call.wav");
const params = new URLSearchParams({ language: "en", word_timestamps: "true", diarize: "true" });

const res = await fetch(`https://api.smallest.ai/waves/v1/pulse/get_text?${params}`, {
  method: "POST",
  headers: {
    Authorization: `Bearer ${process.env.SMALLEST_API_KEY}`,
    "Content-Type": "application/octet-stream",
  },
  body: audio,
});
const result = await res.json();
console.log(result.transcription);
```

## Common gotchas

- **Max file size is 250 MB.** Larger files return HTTP `400` with `{errors: "Audio data too large", status: "error", message: "Error handling audio data"}`. Compress to mono 16 kHz PCM if you're close to the limit; quality is unaffected.
- **Formatting flags (`format`, `punctuate`, `capitalize`)** are accepted at the wire level and exposed in the Python SDK as of `smallestai>=4.4.0`. Today they currently return the same transcript regardless of value — pass them in your integration so it works as the behavior changes.
- **Webhook-driven flow**: pass `webhook_url` to receive the transcript asynchronously. The endpoint returns immediately; the transcript hits your webhook when ready. Useful for long files where you don't want to hold an HTTP connection open.
- **Speaker diarization** (`diarize=true`) adds latency. Skip it if you only need the words.
- **JavaScript / TypeScript**: the official `smallestai` npm package predates the Pulse model, so call this endpoint with `fetch` or `axios` as shown above.
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
client.waves.transcribe_pulse(...)
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

**request:** `typing.Union[bytes, typing.Iterator[bytes], typing.AsyncIterator[bytes]]` 
    
</dd>
</dl>

<dl>
<dd>

**language:** `typing.Optional[TranscribePulseWavesRequestLanguage]` 

Language of the audio file. Set explicitly to the known language for best accuracy.

**26 single-language codes** on this endpoint: `en`, `hi`, `de`, `es`, `ru`, `it`, `fr`, `nl`, `pt`, `uk`, `pl`, `cs`, `sk`, `lv`, `et`, `ro`, `fi`, `sv`, `bg`, `hu`, `da`, `lt`, `mt`, `zh`, `ja`, `ko`.

**Regional auto-detect aggregators** for unknown audio:
- `multi-eu` (default) — auto-detects across all 21 European codes above plus `en`.
- `multi-asian` — auto-detects across `zh`, `ko`, `ja`, `en`.

Omitting `language` routes to `multi-eu`. See the [Pulse model card](/waves/model-cards/speech-to-text/pulse) for the full table.
    
</dd>
</dl>

<dl>
<dd>

**encoding:** `typing.Optional[TranscribePulseWavesRequestEncoding]` 

Audio encoding of the bytes you upload. Mirrors the `encoding`
parameter on the realtime WS endpoint.

- `linear16`, `linear32` — raw PCM (16-bit and 32-bit)
- `alaw`, `mulaw` — 8 kHz telephony codecs
- `opus`, `ogg_opus` — Opus compressed audio (raw and Ogg container)

When omitted, the server detects the format from the file's
container header (works for `.wav`, `.mp3`, `.flac`, `.ogg`,
`.m4a`, `.webm`).
    
</dd>
</dl>

<dl>
<dd>

**webhook_url:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**webhook_extra:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**word_timestamps:** `typing.Optional[bool]` — Whether to include word and utterance level timestamps in the response
    
</dd>
</dl>

<dl>
<dd>

**diarize:** `typing.Optional[bool]` — Whether to perform speaker diarization
    
</dd>
</dl>

<dl>
<dd>

**gender_detection:** `typing.Optional[TranscribePulseWavesRequestGenderDetection]` — Whether to predict the gender of the speaker
    
</dd>
</dl>

<dl>
<dd>

**emotion_detection:** `typing.Optional[TranscribePulseWavesRequestEmotionDetection]` — Whether to predict speaker emotions
    
</dd>
</dl>

<dl>
<dd>

**format:** `typing.Optional[TranscribePulseWavesRequestFormat]` 

Master formatting switch for the transcript. When `false`, forces
`punctuate=false`, `capitalize=false`, and also disables Inverse
Text Normalization (ITN) so it cannot silently reintroduce
punctuation or casing.

When `true`, the `punctuate` and `capitalize` params take effect
independently. Leave `format=true` and use those two to fine-tune.
    
</dd>
</dl>

<dl>
<dd>

**punctuate:** `typing.Optional[TranscribePulseWavesRequestPunctuate]` 

When `false`, strips end-of-sentence punctuation (`.`, `,`, `?`, `!`)
from the transcript, `words[].word`, and
`utterances[].transcript`. Does not affect casing — use
`capitalize` for that. Overridden to `false` when `format=false`.
    
</dd>
</dl>

<dl>
<dd>

**capitalize:** `typing.Optional[TranscribePulseWavesRequestCapitalize]` 

When `false`, lowercases the entire transcript output (transcript,
`words[].word`, and `utterances[].transcript`). Does not affect
punctuation — use `punctuate` for that. Overridden to `false`
when `format=false`.
    
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

