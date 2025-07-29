# AgentAgentIdWebhookSubscriptionsPostRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**event_types** | **List[str]** | Array of event types to subscribe to | 
**webhook_id** | **str** | The ID of the webhook to subscribe to | 

## Example

```python
from atoms.models.agent_agent_id_webhook_subscriptions_post_request import AgentAgentIdWebhookSubscriptionsPostRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AgentAgentIdWebhookSubscriptionsPostRequest from a JSON string
agent_agent_id_webhook_subscriptions_post_request_instance = AgentAgentIdWebhookSubscriptionsPostRequest.from_json(json)
# print the JSON string representation of the object
print(AgentAgentIdWebhookSubscriptionsPostRequest.to_json())

# convert the object into a dict
agent_agent_id_webhook_subscriptions_post_request_dict = agent_agent_id_webhook_subscriptions_post_request_instance.to_dict()
# create an instance of AgentAgentIdWebhookSubscriptionsPostRequest from a dict
agent_agent_id_webhook_subscriptions_post_request_from_dict = AgentAgentIdWebhookSubscriptionsPostRequest.from_dict(agent_agent_id_webhook_subscriptions_post_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


