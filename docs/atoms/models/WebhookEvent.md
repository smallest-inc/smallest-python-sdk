# WebhookEvent


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The unique identifier for the event | [optional] 
**webhook_id** | **str** | The ID of the webhook | [optional] 
**event_type** | **str** | The type of event | [optional] 
**payload** | **object** | The event payload | [optional] 
**status** | **str** | The status of the event | [optional] 
**created_at** | **datetime** | The date and time when the event was created | [optional] 

## Example

```python
from atoms.models.webhook_event import WebhookEvent

# TODO update the JSON string below
json = "{}"
# create an instance of WebhookEvent from a JSON string
webhook_event_instance = WebhookEvent.from_json(json)
# print the JSON string representation of the object
print(WebhookEvent.to_json())

# convert the object into a dict
webhook_event_dict = webhook_event_instance.to_dict()
# create an instance of WebhookEvent from a dict
webhook_event_from_dict = WebhookEvent.from_dict(webhook_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


