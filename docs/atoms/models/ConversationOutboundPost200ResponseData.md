# ConversationOutboundPost200ResponseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**conversation_id** | **str** | The ID of the initiated call | [optional] 

## Example

```python
from atoms.models.conversation_outbound_post200_response_data import ConversationOutboundPost200ResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of ConversationOutboundPost200ResponseData from a JSON string
conversation_outbound_post200_response_data_instance = ConversationOutboundPost200ResponseData.from_json(json)
# print the JSON string representation of the object
print(ConversationOutboundPost200ResponseData.to_json())

# convert the object into a dict
conversation_outbound_post200_response_data_dict = conversation_outbound_post200_response_data_instance.to_dict()
# create an instance of ConversationOutboundPost200ResponseData from a dict
conversation_outbound_post200_response_data_from_dict = ConversationOutboundPost200ResponseData.from_dict(conversation_outbound_post200_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


