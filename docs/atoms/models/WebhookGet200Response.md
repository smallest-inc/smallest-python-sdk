# WebhookGet200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**data** | [**WebhookGet200ResponseData**](WebhookGet200ResponseData.md) |  | [optional] 

## Example

```python
from atoms.models.webhook_get200_response import WebhookGet200Response

# TODO update the JSON string below
json = "{}"
# create an instance of WebhookGet200Response from a JSON string
webhook_get200_response_instance = WebhookGet200Response.from_json(json)
# print the JSON string representation of the object
print(WebhookGet200Response.to_json())

# convert the object into a dict
webhook_get200_response_dict = webhook_get200_response_instance.to_dict()
# create an instance of WebhookGet200Response from a dict
webhook_get200_response_from_dict = WebhookGet200Response.from_dict(webhook_get200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


