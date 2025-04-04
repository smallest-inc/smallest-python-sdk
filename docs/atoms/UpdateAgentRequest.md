# UpdateAgentRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**language** | [**UpdateAgentRequestLanguage**](UpdateAgentRequestLanguage.md) |  | [optional] 
**synthesizer** | [**UpdateAgentRequestSynthesizer**](UpdateAgentRequestSynthesizer.md) |  | [optional] 
**global_knowledge_base_id** | **str** |  | [optional] 
**slm_model** | **str** |  | [optional] [default to 'atoms-slm-v1']
**default_variables** | **object** | The default variables to use for the agent. These variables will be used if no variables are provided when initiating a conversation with the agent. | [optional] 
**telephony_product_id** | **str** | The telephony product ID of the agent. This is the product ID of the telephony product that will be used to make the outbound call. You can buy telephone number and assign it to the agent. | [optional] 

## Example

```python
from smallestai.atoms_client.models.update_agent_request import UpdateAgentRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateAgentRequest from a JSON string
update_agent_request_instance = UpdateAgentRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateAgentRequest.to_json())

# convert the object into a dict
update_agent_request_dict = update_agent_request_instance.to_dict()
# create an instance of UpdateAgentRequest from a dict
update_agent_request_from_dict = UpdateAgentRequest.from_dict(update_agent_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


