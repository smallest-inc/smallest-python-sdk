# ConversationOutboundPost200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**data** | [**ConversationOutboundPost200ResponseData**](ConversationOutboundPost200ResponseData.md) |  | [optional] 

## Example

```python
from atoms.models.conversation_outbound_post200_response import ConversationOutboundPost200Response

# TODO update the JSON string below
json = "{}"
# create an instance of ConversationOutboundPost200Response from a JSON string
conversation_outbound_post200_response_instance = ConversationOutboundPost200Response.from_json(json)
# print the JSON string representation of the object
print(ConversationOutboundPost200Response.to_json())

# convert the object into a dict
conversation_outbound_post200_response_dict = conversation_outbound_post200_response_instance.to_dict()
# create an instance of ConversationOutboundPost200Response from a dict
conversation_outbound_post200_response_from_dict = ConversationOutboundPost200Response.from_dict(conversation_outbound_post200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


