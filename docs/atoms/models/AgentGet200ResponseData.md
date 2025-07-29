# AgentGet200ResponseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**agents** | [**List[AgentDTO]**](AgentDTO.md) |  | [optional] 
**total** | **float** | Total number of agents | [optional] 

## Example

```python
from atoms.models.agent_get200_response_data import AgentGet200ResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of AgentGet200ResponseData from a JSON string
agent_get200_response_data_instance = AgentGet200ResponseData.from_json(json)
# print the JSON string representation of the object
print(AgentGet200ResponseData.to_json())

# convert the object into a dict
agent_get200_response_data_dict = agent_get200_response_data_instance.to_dict()
# create an instance of AgentGet200ResponseData from a dict
agent_get200_response_data_from_dict = AgentGet200ResponseData.from_dict(agent_get200_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


