# WebhookPost201Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**data** | **str** | The ID of the created webhook | [optional] 

## Example

```python
from atoms.models.webhook_post201_response import WebhookPost201Response

# TODO update the JSON string below
json = "{}"
# create an instance of WebhookPost201Response from a JSON string
webhook_post201_response_instance = WebhookPost201Response.from_json(json)
# print the JSON string representation of the object
print(WebhookPost201Response.to_json())

# convert the object into a dict
webhook_post201_response_dict = webhook_post201_response_instance.to_dict()
# create an instance of WebhookPost201Response from a dict
webhook_post201_response_from_dict = WebhookPost201Response.from_dict(webhook_post201_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


