# WebhookGet200ResponseData


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
from atoms.models.webhook_get200_response_data import WebhookGet200ResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of WebhookGet200ResponseData from a JSON string
webhook_get200_response_data_instance = WebhookGet200ResponseData.from_json(json)
# print the JSON string representation of the object
print(WebhookGet200ResponseData.to_json())

# convert the object into a dict
webhook_get200_response_data_dict = webhook_get200_response_data_instance.to_dict()
# create an instance of WebhookGet200ResponseData from a dict
webhook_get200_response_data_from_dict = WebhookGet200ResponseData.from_dict(webhook_get200_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


