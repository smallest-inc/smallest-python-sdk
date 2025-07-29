# ConversationOutboundPostRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**agent_id** | **str** | The ID of the agent initiating the conversation | 
**phone_number** | **str** | The phone number to call | 

## Example

```python
from atoms.models.conversation_outbound_post_request import ConversationOutboundPostRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ConversationOutboundPostRequest from a JSON string
conversation_outbound_post_request_instance = ConversationOutboundPostRequest.from_json(json)
# print the JSON string representation of the object
print(ConversationOutboundPostRequest.to_json())

# convert the object into a dict
conversation_outbound_post_request_dict = conversation_outbound_post_request_instance.to_dict()
# create an instance of ConversationOutboundPostRequest from a dict
conversation_outbound_post_request_from_dict = ConversationOutboundPostRequest.from_dict(conversation_outbound_post_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


