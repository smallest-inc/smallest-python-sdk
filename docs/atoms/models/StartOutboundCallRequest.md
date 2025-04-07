# StartOutboundCallRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**agent_id** | **str** | The ID of the agent initiating the conversation | 
**phone_number** | **str** | The phone number to call | 

## Example

```python
from smallestai.atoms.models.start_outbound_call_request import StartOutboundCallRequest

# TODO update the JSON string below
json = "{}"
# create an instance of StartOutboundCallRequest from a JSON string
start_outbound_call_request_instance = StartOutboundCallRequest.from_json(json)
# print the JSON string representation of the object
print(StartOutboundCallRequest.to_json())

# convert the object into a dict
start_outbound_call_request_dict = start_outbound_call_request_instance.to_dict()
# create an instance of StartOutboundCallRequest from a dict
start_outbound_call_request_from_dict = StartOutboundCallRequest.from_dict(start_outbound_call_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


