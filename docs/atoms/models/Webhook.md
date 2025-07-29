# Webhook


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The unique identifier for the webhook | [optional] 
**url** | **str** | The webhook endpoint URL | [optional] 
**description** | **str** | The description of the webhook | [optional] 
**status** | **str** | The status of the webhook | [optional] 
**organization_id** | **str** | The organization ID | [optional] 
**created_by** | **str** | The user ID who created the webhook | [optional] 
**subscriptions** | [**List[WebhookSubscriptionPopulated]**](WebhookSubscriptionPopulated.md) | A list of subscriptions for the webhook with populated agent details. | [optional] 
**decrypted_secret_key** | **str** | The decrypted signing secret for the webhook. This is only returned when fetching a single webhook by ID. | [optional] 
**created_at** | **datetime** | The date and time when the webhook was created | [optional] 
**updated_at** | **datetime** | The date and time when the webhook was last updated | [optional] 

## Example

```python
from atoms.models.webhook import Webhook

# TODO update the JSON string below
json = "{}"
# create an instance of Webhook from a JSON string
webhook_instance = Webhook.from_json(json)
# print the JSON string representation of the object
print(Webhook.to_json())

# convert the object into a dict
webhook_dict = webhook_instance.to_dict()
# create an instance of Webhook from a dict
webhook_from_dict = Webhook.from_dict(webhook_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


