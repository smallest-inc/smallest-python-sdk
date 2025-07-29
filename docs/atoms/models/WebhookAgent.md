# WebhookAgent


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The ID of the agent | [optional] 
**name** | **str** | The name of the agent | [optional] 
**description** | **str** | The description of the agent | [optional] 

## Example

```python
from atoms.models.webhook_agent import WebhookAgent

# TODO update the JSON string below
json = "{}"
# create an instance of WebhookAgent from a JSON string
webhook_agent_instance = WebhookAgent.from_json(json)
# print the JSON string representation of the object
print(WebhookAgent.to_json())

# convert the object into a dict
webhook_agent_dict = webhook_agent_instance.to_dict()
# create an instance of WebhookAgent from a dict
webhook_agent_from_dict = WebhookAgent.from_dict(webhook_agent_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


