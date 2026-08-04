# Agents

Single-prompt agents are a prompt plus a set of tools. Create and inspect them
through `client.atoms.agents`; configure prompt/tools through the versioning flow.

## Create

```python
agent_id = client.atoms.agents.create_agent(
    name="Front desk",
    workflow_type="single_prompt",
    first_message="Hi, thanks for calling. How can I help?",
).data
```

Useful create kwargs: `first_message`, `global_prompt`, `description`,
`allow_inbound_call`, `language`, `synthesizer`, `slm_model`. (Setting the prompt
body and tools happens through the versioning flow — see below.)

## Inspect / list

```python
from smallestai.atoms.helpers import as_page

page = as_page(client.atoms.agents.list_agents())
for a in page.items:
    print(getattr(a, "id", None) or getattr(a, "_id", None), a.name)

agent = client.atoms.agents.get_agent(id=agent_id).data
```

## Prompt & tools live in versions

Atoms runs on the **branch/revision** versioning model. Serving reads the live
branch's head revision. So prompt/tool changes go through:

```
open a draft -> publish (security scan) -> make the revision live
```

Do **not** write the legacy workflow doc (`PATCH /workflow/{id}`) — the branch
model ignores it on live calls, and the v1 drafts/versions endpoints are
deprecated (return 409).

For tools specifically (transfer_call, end_call, ...), use the helper — it does the
whole branch flow for you:

```python
from smallestai.atoms.helpers import AgentTools

tools = AgentTools(api_key=api_key)
tools.add_transfer_call(agent_id, number="+15551234567", transfer_type="cold_transfer")
```

See [Transfer calls](transfer-call.md) for the full tool story, and
`client.atoms.agent_versioning_branches` for direct branch/revision access.

## CLI

```bash
smallestai agents list
smallestai agents get <agent_id>
smallestai agents create "Front desk" --first-message "Hi!"
smallestai agents call <agent_id> --to +15559990000 --from-product-id <id>
```
