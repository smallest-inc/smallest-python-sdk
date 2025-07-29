# WebhookIdDelete404Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**errors** | **List[str]** |  | [optional] 

## Example

```python
from atoms.models.webhook_id_delete404_response import WebhookIdDelete404Response

# TODO update the JSON string below
json = "{}"
# create an instance of WebhookIdDelete404Response from a JSON string
webhook_id_delete404_response_instance = WebhookIdDelete404Response.from_json(json)
# print the JSON string representation of the object
print(WebhookIdDelete404Response.to_json())

# convert the object into a dict
webhook_id_delete404_response_dict = webhook_id_delete404_response_instance.to_dict()
# create an instance of WebhookIdDelete404Response from a dict
webhook_id_delete404_response_from_dict = WebhookIdDelete404Response.from_dict(webhook_id_delete404_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


