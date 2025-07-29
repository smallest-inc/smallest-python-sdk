# WebhookSubscription


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The unique identifier for the subscription | [optional] 
**webhook_id** | **str** | The ID of the webhook | [optional] 
**agent_id** | **str** | The ID of the agent | [optional] 
**event_type** | **str** | The type of event subscribed to | [optional] 
**created_at** | **datetime** | The date and time when the subscription was created | [optional] 
**updated_at** | **datetime** | The date and time when the subscription was last updated | [optional] 

## Example

```python
from atoms.models.webhook_subscription import WebhookSubscription

# TODO update the JSON string below
json = "{}"
# create an instance of WebhookSubscription from a JSON string
webhook_subscription_instance = WebhookSubscription.from_json(json)
# print the JSON string representation of the object
print(WebhookSubscription.to_json())

# convert the object into a dict
webhook_subscription_dict = webhook_subscription_instance.to_dict()
# create an instance of WebhookSubscription from a dict
webhook_subscription_from_dict = WebhookSubscription.from_dict(webhook_subscription_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


