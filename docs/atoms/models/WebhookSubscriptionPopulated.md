# WebhookSubscriptionPopulated


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The unique identifier for the subscription | [optional] 
**webhook_id** | **str** | The ID of the webhook | [optional] 
**agent_id** | [**WebhookAgent**](WebhookAgent.md) |  | [optional] 
**event_type** | **str** | The type of event subscribed to | [optional] 
**created_at** | **datetime** | The date and time when the subscription was created | [optional] 
**updated_at** | **datetime** | The date and time when the subscription was last updated | [optional] 

## Example

```python
from atoms.models.webhook_subscription_populated import WebhookSubscriptionPopulated

# TODO update the JSON string below
json = "{}"
# create an instance of WebhookSubscriptionPopulated from a JSON string
webhook_subscription_populated_instance = WebhookSubscriptionPopulated.from_json(json)
# print the JSON string representation of the object
print(WebhookSubscriptionPopulated.to_json())

# convert the object into a dict
webhook_subscription_populated_dict = webhook_subscription_populated_instance.to_dict()
# create an instance of WebhookSubscriptionPopulated from a dict
webhook_subscription_populated_from_dict = WebhookSubscriptionPopulated.from_dict(webhook_subscription_populated_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


