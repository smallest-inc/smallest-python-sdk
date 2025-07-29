# WebhookPostRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**endpoint** | **str** | The webhook endpoint URL | 
**description** | **str** | The description of the webhook | 
**events** | [**List[WebhookPostRequestEventsInner]**](WebhookPostRequestEventsInner.md) | Array of events to subscribe to | 

## Example

```python
from atoms.models.webhook_post_request import WebhookPostRequest

# TODO update the JSON string below
json = "{}"
# create an instance of WebhookPostRequest from a JSON string
webhook_post_request_instance = WebhookPostRequest.from_json(json)
# print the JSON string representation of the object
print(WebhookPostRequest.to_json())

# convert the object into a dict
webhook_post_request_dict = webhook_post_request_instance.to_dict()
# create an instance of WebhookPostRequest from a dict
webhook_post_request_from_dict = WebhookPostRequest.from_dict(webhook_post_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


