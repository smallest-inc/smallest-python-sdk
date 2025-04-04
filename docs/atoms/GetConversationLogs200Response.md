# GetConversationLogs200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**data** | [**GetConversationLogs200ResponseData**](GetConversationLogs200ResponseData.md) |  | [optional] 

## Example

```python
from smallestai.atoms.models.get_conversation_logs200_response import GetConversationLogs200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetConversationLogs200Response from a JSON string
get_conversation_logs200_response_instance = GetConversationLogs200Response.from_json(json)
# print the JSON string representation of the object
print(GetConversationLogs200Response.to_json())

# convert the object into a dict
get_conversation_logs200_response_dict = get_conversation_logs200_response_instance.to_dict()
# create an instance of GetConversationLogs200Response from a dict
get_conversation_logs200_response_from_dict = GetConversationLogs200Response.from_dict(get_conversation_logs200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


