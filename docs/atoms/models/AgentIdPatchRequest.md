# AgentIdPatchRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**language** | [**AgentIdPatchRequestLanguage**](AgentIdPatchRequestLanguage.md) |  | [optional] 
**synthesizer** | [**AgentIdPatchRequestSynthesizer**](AgentIdPatchRequestSynthesizer.md) |  | [optional] 
**global_knowledge_base_id** | **str** |  | [optional] 
**slm_model** | **str** |  | [optional] [default to 'electron']
**default_variables** | **object** | The default variables to use for the agent. These variables will be used if no variables are provided when initiating a conversation with the agent. | [optional] 
**global_prompt** | **str** | Set global instructions for your agent&#39;s personality, role, and behavior throughout conversations | [optional] 
**telephony_product_id** | **str** | The telephony product ID of the agent. This is the product ID of the telephony product that will be used to make the outbound call. You can buy telephone number and assign it to the agent. | [optional] 

## Example

```python
from atoms.models.agent_id_patch_request import AgentIdPatchRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AgentIdPatchRequest from a JSON string
agent_id_patch_request_instance = AgentIdPatchRequest.from_json(json)
# print the JSON string representation of the object
print(AgentIdPatchRequest.to_json())

# convert the object into a dict
agent_id_patch_request_dict = agent_id_patch_request_instance.to_dict()
# create an instance of AgentIdPatchRequest from a dict
agent_id_patch_request_from_dict = AgentIdPatchRequest.from_dict(agent_id_patch_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


