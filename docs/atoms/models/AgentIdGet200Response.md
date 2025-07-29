# AgentIdGet200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**data** | [**AgentDTO**](AgentDTO.md) |  | [optional] 

## Example

```python
from atoms.models.agent_id_get200_response import AgentIdGet200Response

# TODO update the JSON string below
json = "{}"
# create an instance of AgentIdGet200Response from a JSON string
agent_id_get200_response_instance = AgentIdGet200Response.from_json(json)
# print the JSON string representation of the object
print(AgentIdGet200Response.to_json())

# convert the object into a dict
agent_id_get200_response_dict = agent_id_get200_response_instance.to_dict()
# create an instance of AgentIdGet200Response from a dict
agent_id_get200_response_from_dict = AgentIdGet200Response.from_dict(agent_id_get200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


