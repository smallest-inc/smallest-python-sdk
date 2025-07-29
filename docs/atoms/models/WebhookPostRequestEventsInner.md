# WebhookPostRequestEventsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**agent_id** | **str** | The ID of the agent | [optional] 
**event_type** | **str** | The type of event to subscribe to | [optional] 

## Example

```python
from atoms.models.webhook_post_request_events_inner import WebhookPostRequestEventsInner

# TODO update the JSON string below
json = "{}"
# create an instance of WebhookPostRequestEventsInner from a JSON string
webhook_post_request_events_inner_instance = WebhookPostRequestEventsInner.from_json(json)
# print the JSON string representation of the object
print(WebhookPostRequestEventsInner.to_json())

# convert the object into a dict
webhook_post_request_events_inner_dict = webhook_post_request_events_inner_instance.to_dict()
# create an instance of WebhookPostRequestEventsInner from a dict
webhook_post_request_events_inner_from_dict = WebhookPostRequestEventsInner.from_dict(webhook_post_request_events_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


