# AgentGet200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**data** | [**AgentGet200ResponseData**](AgentGet200ResponseData.md) |  | [optional] 

## Example

```python
from atoms.models.agent_get200_response import AgentGet200Response

# TODO update the JSON string below
json = "{}"
# create an instance of AgentGet200Response from a JSON string
agent_get200_response_instance = AgentGet200Response.from_json(json)
# print the JSON string representation of the object
print(AgentGet200Response.to_json())

# convert the object into a dict
agent_get200_response_dict = agent_get200_response_instance.to_dict()
# create an instance of AgentGet200Response from a dict
agent_get200_response_from_dict = AgentGet200Response.from_dict(agent_get200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


