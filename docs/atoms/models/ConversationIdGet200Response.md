# ConversationIdGet200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**data** | [**ConversationIdGet200ResponseData**](ConversationIdGet200ResponseData.md) |  | [optional] 

## Example

```python
from atoms.models.conversation_id_get200_response import ConversationIdGet200Response

# TODO update the JSON string below
json = "{}"
# create an instance of ConversationIdGet200Response from a JSON string
conversation_id_get200_response_instance = ConversationIdGet200Response.from_json(json)
# print the JSON string representation of the object
print(ConversationIdGet200Response.to_json())

# convert the object into a dict
conversation_id_get200_response_dict = conversation_id_get200_response_instance.to_dict()
# create an instance of ConversationIdGet200Response from a dict
conversation_id_get200_response_from_dict = ConversationIdGet200Response.from_dict(conversation_id_get200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


